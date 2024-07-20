import pandas as pd
import sqlite3
import requests
import io
import json
from datetime import datetime

# Step 1: Data Extraction
def download_csv(url):
    response = requests.get(url)
    if response.status_code == 200:
        return pd.read_csv(io.StringIO(response.text))
    else:
        print("Error: Unable to download the CSV file.")
        exit()

# Step 2: Data Transformation
def transform_data(data):
    # Clean and standardize data
    data.columns = [col.strip().lower().replace(" ", "_") for col in data.columns]

    # Rename columns for consistency
    data.rename(columns={'delayed_payment': 'days_past_due'}, inplace=True)

    # Convert relevant columns to numeric and handle errors
    for column in ['loan_amount', 'emi', 'loan_term', 'interest_rate']:
        data[column] = pd.to_numeric(data[column], errors='coerce')

    # Handle 'days_past_due' conversion
    data['days_past_due'] = data['days_past_due'].apply(lambda x: 6 if x == 'Yes' else 0)

    # Extract relevant info from 'repayment_history'
    def is_good_repayment(history):
        try:
            payments = json.loads(history.replace("'", "\""))
            for payment in payments:
                payment_date = datetime.strptime(payment['Payment Date'], '%Y-%m-%d').date()
                if payment_date < datetime.now().date() and payment['Payment Mode'] == 'Delayed':
                    return False
            return True
        except:
            return False

    data['good_repayment_history'] = data['repayment_history'].apply(is_good_repayment)

    # Handle missing values
    data = data.dropna(subset=['loan_amount', 'days_past_due', 'emi', 'loan_term', 'interest_rate'])

    # Calculate outstanding_balance (simplified example)
    data['outstanding_balance'] = data['loan_amount'] * (1 + data['interest_rate'] / 100) - data['emi']
    
    # Print the DataFrame after transformation
    print("Transformed Data Sample:\n", data.head())

    return data

# Step 3: Data Loading
def load_data_to_sqlite(data, db_name):
    conn = sqlite3.connect(db_name)
    data.to_sql('borrowers', conn, if_exists='replace', index=False)
    conn.close()
    print("Data loaded successfully into the 'borrowers' table.")

# Function to execute a query and fetch the results
def execute_query(connection, query):
    cursor = connection.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    return pd.DataFrame(result, columns=columns)

def main():
    url = "https://drive.google.com/uc?export=download&id=1asq7yzvFpkmDUMZQtK7AJ16_XZbQCZmc"
    db_name = 'borrowers.db'
    
    # Extract data
    data = download_csv(url)
    
    # Transform data
    data = transform_data(data)
    
    # Load data into SQLite
    load_data_to_sqlite(data, db_name)
    
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)

    # Define the queries
    queries = {
        'a': """
            SELECT AVG(loan_amount) AS average_loan_amount
            FROM borrowers
            WHERE days_past_due > 5;
        """,
        'b': """
            SELECT name, outstanding_balance
            FROM borrowers
            ORDER BY outstanding_balance DESC
            LIMIT 10;
        """,
        'c': """
            SELECT name, loan_amount, emi, loan_term, interest_rate, outstanding_balance
            FROM borrowers
            WHERE good_repayment_history = 1;
        """,
        'd': """
            SELECT loan_type, COUNT(*) AS count, AVG(loan_amount) AS average_loan_amount
            FROM borrowers
            GROUP BY loan_type;
        """
    }

    # Execute the queries and print the results
    results = {}
    for key, query in queries.items():
        results[key] = execute_query(conn, query)
        print(f"\n{key}. Query results:")
        print(results[key])

    # Save results to analysis_results.txt
    with open('analysis_results.txt', 'w') as f:
        f.write("### Analysis Results\n")
        f.write("\n#### a. Average loan amount for borrowers who are more than 5 days past due:\n")
        f.write(results['a'].to_string(index=False))
        f.write("\n\n#### b. Top 10 borrowers with the highest outstanding balance:\n")
        f.write(results['b'].to_string(index=False))
        f.write("\n\n#### c. List of all borrowers with good repayment history:\n")
        f.write(results['c'].to_string(index=False))
        f.write("\n\n#### d. Brief analysis with respect to loan type:\n")
        f.write(results['d'].to_string(index=False))

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()

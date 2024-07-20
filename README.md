# Debt Collection ETL

## Objective
Perform a basic ETL (Extract, Transform, Load) process on a CSV file containing borrower data, load it into a SQL database, and conduct simple analysis for debt collection purposes.

## Files in this Repository
- `etl_script.py`: Python script for the ETL process (extraction, transformation, and loading)
- `analysis_queries.sql`: SQL script containing the queries for the basic analysis
- `analysis_results.txt`: A brief report with the results of the analysis
- `README.md`: Instructions for running the ETL process and the analysis

## Instructions for Running the ETL Process

1. **Clone the Repository**
    ```sh
    git clone https://github.com/YourUsername/Tripathi_Atul_DebtCollectionETL.git
    cd Tripathi_Atul_DebtCollectionETL
    ```

2. **Ensure you have the required libraries installed**
    ```sh
    pip install pandas requests
    ```

3. **Run the ETL Script**
    ```sh
    python etl_script.py
    ```

This will download the data, transform it, load it into a SQLite database, and perform the basic analysis. The results of the analysis will be saved to `analysis_results.txt`.

## Uploading to GitHub

1. **Create Repository on GitHub**
   - Go to GitHub and create a new repository named `Tripathi_Atul_DebtCollectionETL`.

2. **Clone the Repository**
   ```sh
   git clone https://github.com/YourUsername/Tripathi_Atul_DebtCollectionETL.git
   cd Tripathi_Atul_DebtCollectionETL

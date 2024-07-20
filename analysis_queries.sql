-- a. What is the average loan amount for borrowers who are more than 5 days past due?
SELECT AVG(loan_amount) AS average_loan_amount
FROM borrowers
WHERE days_past_due > 5;

-- b. Who are the top 10 borrowers with the highest outstanding balance?
SELECT name, outstanding_balance
FROM borrowers
ORDER BY outstanding_balance DESC
LIMIT 10;

-- c. List of all borrowers with good repayment history
SELECT name, loan_amount, emi, loan_term, interest_rate, outstanding_balance
FROM borrowers
WHERE good_repayment_history = 1;

-- d. Brief analysis with respect to loan type
SELECT loan_type, COUNT(*) AS count, AVG(loan_amount) AS average_loan_amount
FROM borrowers
GROUP BY loan_type;

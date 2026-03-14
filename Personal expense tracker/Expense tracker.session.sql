-- @block
CREATE TABLE IF NOT EXISTS Expenses (
    id SERIAL PRIMARY KEY AUTO_INCREMENT,
    amount DECIMAL(10, 2) NOT NULL,
    description TEXT,
    date DATE NOT NULL
);
-- @block
INSERT INTO Expenses (amount, description, date)
VALUES (50.00, 'Groceries', '2024-06-01'),
    (20.00, 'Transport', '2024-06-02'),
    (100.00, 'Utilities', '2024-06-03');
-- @block
SELECT *
FROM Expenses;
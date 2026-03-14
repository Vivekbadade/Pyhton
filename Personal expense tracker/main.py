from datetime import date
import sqlite3
from tkinter import messagebox
import matplotlib.pyplot as plt
import tkinter as tk

# Main function to run the application
def main():
    # Change button state based on checkbox
    def change_buttton_state():
        if confirm_state.get() == 1:
            button_add.config(state=tk.NORMAL)
        else:
            button_add.config(state=tk.DISABLED)
            
    # Refresh the app after adding an expense to show the updated list of expenses
    def refresh_app():
        app.destroy()
        main()
        
    # Plot expenses by description or date
    def plot_expenses():
        # print("Pie chart by desription or bar chart by date? (pie/bar)")
        
        if chart_type.get() == "pie":
            connect = sqlite3.connect("expense.db")
            mycursor = connect.cursor()
            mycursor.execute("SELECT description, SUM(amount) FROM expenses GROUP BY description")
            data = mycursor.fetchall()
            total_amount = sum(row[1] for row in data)
            descriptions = [row[0] for row in data]
            amounts = [row[1] for row in data]
            plt.pie(amounts, labels=descriptions, autopct='%1.1f%%')
            plt.title('Expenses by Description')
            # make visible axis
            plt.axis('on')
            plt.text(0, -1.1, f"Total: ${total_amount:.2f}", fontsize=10, ha='center')
            plt.axis('equal')
            plt.show()
        
        elif chart_type.get() == "bar":
            connect = sqlite3.connect("expense.db")
            mycursor = connect.cursor()
            mycursor.execute("SELECT date, SUM(amount) FROM expenses GROUP BY date")
            data = mycursor.fetchall()
            dates = [row[0] for row in data]
            amounts = [row[1] for row in data]
            plt.bar(dates, amounts)
            plt.xlabel('Date')
            plt.ylabel('Total Expenses')
            plt.title('Expenses Over Time')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

    # Add expense to database
    def add_expense(amount=None, description=None, date=None):
            connect = sqlite3.connect("expense.db")
            mycursor = connect.cursor()
            mycursor.execute("INSERT INTO expenses (amount, description, date) VALUES (?, ?, ?)", (amount, description.capitalize(), date))
            connect.commit()
            #Showing a popup message to confirm that the expense was added successfully
            messagebox.showinfo("Success", f"Expense added successfully amount: {amount}, description: {description}, date: {date}")
            refresh_app()
            connect.close()


    # Create the main application window 
    app = tk.Tk()

    #Connect to the SQLite database (or create it if it doesn't exist)
    connect = sqlite3.connect(
        "expense.db"
    );

    # Create a cursor object to interact with the database
    mycursor = connect.cursor()

    #Create the expenses table if it doesn't exist
    mycursor.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT,amount DECIMAL(10, 2) NOT NULL, description TEXT,date DATE NOT NULL)");

    #App title
    app.title("Expense Tracker")

    label = tk.Label(app, text="Welcome to the Expense Tracker!", font=("Arial", 16))
    label.pack(pady=20)

    # Create a frame to hold the expense entries as grid layout
    entryframe=tk.Frame(app)
    entryframe.columnconfigure(0, weight=1)
    entryframe.columnconfigure(1, weight=1)
    entryframe.columnconfigure(2, weight=1)
    entryframe.columnconfigure(3, weight=1)

    data=mycursor.execute("SELECT * FROM expenses")
    i=0
    for expense in data:
        for j in range(len(expense)):
            e=tk.Entry(entryframe, width=20, fg='blue',justify=tk.CENTER)
            e.grid(row=i, column=j,sticky="ew")
            e.insert(tk.END, expense[j])
        i+=1

    entryframe.pack(pady=10, fill=tk.X)

    # Create a frame to hold the input fields for adding new expenses as grid layout
    labelframe = tk.Frame(app)
    labelframe.columnconfigure(0, weight=1)
    labelframe.columnconfigure(1, weight=1)

    label_amount = tk.Label(labelframe, text="Amount:")
    label_amount.grid(row=0, column=0, pady=5, sticky="e")

    entry_amount = tk.Entry(labelframe)
    entry_amount.grid(row=0, column=1, pady=5,sticky="w")

    label_description = tk.Label(labelframe, text="Description:")
    label_description.grid(row=1, column=0, pady=5, sticky="e")

    entry_description = tk.Entry(labelframe, name="description")
    entry_description.grid(row=1, column=1, pady=5, sticky="w")

    label_date = tk.Label(labelframe, text="Date (YYYY-MM-DD):")
    label_date.grid(row=2, column=0, pady=5, sticky="e")

    entry_date = tk.Entry(labelframe, name="date")
    entry_date.grid(row=2, column=1, pady=5, sticky="w")

    labelframe.pack(pady=20, fill=tk.X)

    confirm_state=tk.IntVar(value=0)
    check_confirm = tk.Checkbutton(app, text="Confirm Add", variable=confirm_state, command=change_buttton_state)
    check_confirm.pack(pady=5)

    buttonframe = tk.Frame(app)
    buttonframe.columnconfigure(0, weight=1)
    buttonframe.columnconfigure(1, weight=1)

    # Create buttons for adding expenses and showing expenses
    button_add = tk.Button(buttonframe, state=tk.DISABLED, text="Add Expense", command=lambda: add_expense(entry_amount.get(), entry_description.get(), entry_date.get()))
    button_add.grid(row=0, column=0, pady=10, padx=10, sticky="ew")

    button_show = tk.Button(buttonframe, text="Show Expenses", command=plot_expenses)
    button_show.grid(row=0, column=1, pady=10, padx=10 ,sticky="ew")

    # Create radio buttons for selecting chart type (pie or bar)
    pie_radiobutton = tk.Radiobutton(buttonframe, text="Pie Chart", value="pie",)
    pie_radiobutton.grid(row=1, column=0, pady=5, padx=10, sticky="ew")

    bar_radiobutton = tk.Radiobutton(buttonframe, text="Bar Chart", value="bar")
    bar_radiobutton.grid(row=1, column=1, pady=5, padx=10, sticky="ew")

    # Set the default chart type to "pie" and link the radio buttons to the chart_type variable
    chart_type = tk.StringVar(value="pie")
    pie_radiobutton.config(variable=chart_type)
    bar_radiobutton.config(variable=chart_type)

    buttonframe.pack(pady=20, fill=tk.X)

    #For closing the app
    closwindow = tk.Button(app, text="Close", command=app.destroy)
    closwindow.pack(pady=10)
    app.mainloop()

if __name__ == "__main__":
    main()
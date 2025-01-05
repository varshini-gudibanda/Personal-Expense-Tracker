import os
import time
import csv
from datetime import datetime
from tabulate import tabulate
from matplotlib import pyplot as plt
from collections import defaultdict
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# File paths
BASE_DIR = os.path.dirname(os.path.abspath(r"C:\Users\ADMIN\Documents\G J VARSHINI\Project\Personal Expense Tracker\expenses.txt"))
DEFAULT_FILE = os.path.join(BASE_DIR, "expenses.txt")
USER_FILE_TEMPLATE = os.path.join(BASE_DIR, "{}_expenses.txt")

# Global variables
current_user = "default"
current_file = DEFAULT_FILE
monthly_budget = {}

# Utility functions
def load_expenses(file_path):
    expenses = []
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Create file if it doesn't exist
    with open(file_path, 'r') as file:
        for line in file:
            if line.strip():
                category, amount, date = line.strip().split(",")
                expenses.append({"category": category, "amount": float(amount), "date": date})
    return expenses

def save_expense(file_path, category, amount, date):
    with open(file_path, 'a') as file:
        file.write(f"{category},{amount},{date}\n")

def get_monthly_summary(expenses, month_year):
    total = 0
    category_totals = defaultdict(float)
    for expense in expenses:
        # Extract MM-YYYY from the expense's date
        expense_month_year = datetime.strptime(expense["date"], "%Y-%m-%d").strftime("%m-%Y")
        if month_year == expense_month_year:
            total += expense["amount"]
            category_totals[expense["category"]] += expense["amount"]
    return total, category_totals

def display_pie_chart(data, title):
    if data:
        categories = list(data.keys())
        amounts = list(data.values())
        plt.pie(amounts, labels=categories, autopct="%1.1f%%")
        plt.title(title)
        plt.show()
    else:
        print(Fore.RED + "No data to display.")

# Core functions
#Function to add an expense by category
def add_expense():
    print(Style.BRIGHT + Fore.GREEN + "\nAdding a new expense:")
    category = input(Fore.YELLOW + "Enter category (e.g., Food, Travel): ").strip()
    amount = float(input(Fore.YELLOW + "Enter amount: ").strip())
    date = input(Fore.YELLOW + "Enter date (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(date, "%Y-%m-%d")
        save_expense(current_file, category, amount, date)
        print(Fore.GREEN + "Expense added successfully!")
    except ValueError:
        print(Fore.RED + "Invalid date format. Please use YYYY-MM-DD.")

#Function to veiw expenses
def view_expenses():
    print(Style.BRIGHT + Fore.BLUE + "\nViewing all expenses:")
    expenses = load_expenses(current_file)
    if not expenses:
        print(Fore.RED + "No expenses recorded.")
        return
    categorized_expenses = defaultdict(list)
    for expense in expenses:
        categorized_expenses[expense["category"]].append(expense)
    
    for category, items in categorized_expenses.items():
        print(Fore.YELLOW + f"\n{category}:")
        for i, expense in enumerate(items, start=1):
            print(Fore.CYAN + f"  {i}. Amount: {expense['amount']}, Date: {expense['date']}")
    print()

#Function to display monthly summary
def monthly_summary():
    month_year = input(Fore.YELLOW + "Enter month and year (MM-YYYY): ").strip()
    expenses = load_expenses(current_file)
    total, category_totals = get_monthly_summary(expenses, month_year)
    if total > 0:
        print(Fore.GREEN + f"\nMonthly Summary for {month_year}:")
        print(Fore.CYAN + f"Total Expenses: {total:.2f}")
        print(Fore.MAGENTA + "\nBy Category:")
        print(Fore.WHITE + tabulate(category_totals.items(), headers=["Category", "Amount"], tablefmt="grid"))
        if monthly_budget.get(month_year):
            budget = monthly_budget[month_year]
            if total > budget:
                print(Fore.RED + f"Alert: You have exceeded your budget by {total - budget:.2f}!")
        display_pie_chart(category_totals, f"Expenses for {month_year}")
    else:
        print(Fore.RED + f"No expenses recorded for {month_year}.")

#Fuction to Edit or Delete expense
def edit_or_delete_expense():
    print(Style.BRIGHT + Fore.YELLOW + "\nEditing or Deleting an Expense:")
    expenses = load_expenses(current_file)
    if not expenses:
        print(Fore.RED + "No expenses to edit or delete.")
        return

    print(Fore.BLUE + "\nExpenses:")
    for i, expense in enumerate(expenses, start=1):
        print(Fore.CYAN + f"{i}. Category: {expense['category']}, Amount: {expense['amount']}, Date: {expense['date']}")

    choice = input(Fore.YELLOW + "\nChoose an expense to edit/delete (Enter index): ").strip()
    if not choice.isdigit() or int(choice) < 1 or int(choice) > len(expenses):
        print(Fore.RED + "Invalid choice.")
        return

    index = int(choice) - 1
    print(Fore.GREEN + "\n1. Edit")
    print(Fore.RED + "2. Delete")
    action = input(Fore.YELLOW + "Choose an action: ").strip()
    if action == "1":
        category = input(Fore.YELLOW + "Enter new category: ").strip()
        amount = float(input(Fore.YELLOW + "Enter new amount: ").strip())
        date = input(Fore.YELLOW + "Enter new date (YYYY-MM-DD): ").strip()
        expenses[index] = {"category": category, "amount": amount, "date": date}
        print(Fore.GREEN + "Expense updated successfully!")
    elif action == "2":
        expenses.pop(index)
        print(Fore.GREEN + "Expense deleted successfully!")
    else:
        print(Fore.RED + "Invalid action.")
        return

    with open(current_file, 'w') as file:
        for expense in expenses:
            file.write(f"{expense['category']},{expense['amount']},{expense['date']}\n")

#Function to set budget for a month
def set_budget():
    print(Style.BRIGHT + Fore.GREEN + "\nSetting a monthly budget:")
    month_year = input(Fore.YELLOW + "Enter month and year for budget (MM-YYYY): ").strip()
    budget = float(input(Fore.YELLOW + f"Enter budget for {month_year}: ").strip())
    monthly_budget[month_year] = budget
    print(Fore.GREEN + f"Budget for {month_year} set to {budget:.2f}")

#Function to search an expense
def search_expenses():
    print(Style.BRIGHT + Fore.CYAN + "\nSearching for expenses:")
    expenses = load_expenses(current_file)
    print(Fore.YELLOW + "\nSearch by:")
    print(Fore.GREEN + "1. Category")
    print(Fore.GREEN + "2. Date")
    print(Fore.GREEN + "3. Date Range")
    choice = input(Fore.YELLOW + "Enter your choice: ").strip()

    if choice == "1":
        category = input(Fore.YELLOW + "Enter category: ").strip()
        results = [e for e in expenses if e["category"].lower() == category.lower()]
    elif choice == "2":
        date = input(Fore.YELLOW + "Enter date (YYYY-MM-DD): ").strip()
        results = [e for e in expenses if e["date"] == date]
    elif choice == "3":
        start_date = input(Fore.YELLOW + "Enter start date (YYYY-MM-DD): ").strip()
        end_date = input(Fore.YELLOW + "Enter end date (YYYY-MM-DD): ").strip()
        results = [e for e in expenses if start_date <= e["date"] <= end_date]
    else:
        print(Fore.RED + "Invalid choice.")
        return

    if results:
        print(Fore.GREEN + "\nSearch Results:")
        print(Fore.WHITE + tabulate(results, headers="keys", tablefmt="grid"))
    else:
        print(Fore.RED + "No matching expenses found.")

#Function to display Advanced Analytics like Highest expense category and Average expense in that category
def advanced_analytics():
    expenses = load_expenses(current_file)
    if not expenses:
        print(Fore.RED + "No expenses recorded.")
        return

    category_totals = defaultdict(float)
    for expense in expenses:
        category_totals[expense["category"]] += expense["amount"]

    highest_category = max(category_totals, key=category_totals.get)
    average_expense = sum(category_totals.values()) / len(category_totals)

    print(Fore.CYAN + "\nAdvanced Analytics:")
    print(Fore.GREEN + f"  Highest Spending Category: {highest_category} ({category_totals[highest_category]:.2f})")
    print(Fore.GREEN + f"  Average Monthly Expense: {average_expense:.2f}")

#Export data function
def export_data():
    print(Style.BRIGHT + Fore.YELLOW + "\nExporting data to CSV:")
    csv_file = input(Fore.YELLOW + "Enter filename to export (e.g., expenses_summary.csv): ").strip()
    expenses = load_expenses(current_file)
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Category", "Amount", "Date"])
        for expense in expenses:
            writer.writerow([expense["category"], expense["amount"], expense["date"]])
    print(Fore.GREEN + f"Data exported successfully to {csv_file}")

#Switch user function
def switch_user():
    global current_user, current_file
    print(Style.BRIGHT + Fore.CYAN + "\nSwitching user:")
    username = input(Fore.YELLOW + "Enter username: ").strip()
    current_user = username
    current_file = USER_FILE_TEMPLATE.format(username)
    print(Fore.GREEN + f"Switched to user: {username}")

# Main menu
def main():
    while True:
        print(Fore.MAGENTA + "\n" + "=" * 35)
        print(Fore.WHITE + Style.BRIGHT + f"  PERSONAL EXPENSE TRACKER ({current_user})")
        print(Fore.MAGENTA + "=" * 35)
        print(Fore.CYAN + "1. Add Expense")
        print(Fore.CYAN + "2. View Expenses")
        print(Fore.CYAN + "3. Monthly Summary (with Pie Chart)")
        print(Fore.CYAN + "4. Edit/Delete Expense")
        print(Fore.CYAN + "5. Set Monthly Budget")
        print(Fore.CYAN + "6. Search Expenses")
        print(Fore.CYAN + "7. Advanced Analytics")
        print(Fore.CYAN + "8. Export Data")
        print(Fore.CYAN + "9. Switch User")
        print(Fore.CYAN + "10. Exit")
        print(Fore.MAGENTA + "=" * 35)
        
        choice = input(Fore.YELLOW + "Enter your choice: ").strip()
        
        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            monthly_summary()
        elif choice == "4":
            edit_or_delete_expense()
        elif choice == "5":
            set_budget()
        elif choice == "6":
            search_expenses()
        elif choice == "7":
            advanced_analytics()
        elif choice == "8":
            export_data()
        elif choice == "9":
            switch_user()
        elif choice == "10":
            print(Fore.GREEN + "Exiting the tracker. Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

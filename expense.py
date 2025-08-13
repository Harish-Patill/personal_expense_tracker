import csv
import os
from datetime import datetime

FILE_NAME = os.path.join(os.path.dirname(__file__), "expenses.csv")

CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Entertainment", "Other"]

# Create the file with headers if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount", "Description"])

def choose_category(default=None):
    print("\nChoose a category (or 'B' to go back):")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"{i}. {cat}")
    if default:
        choice = input(f"Enter number (default {default}): ")
        if choice.strip().lower() == "b":
            return None
        if choice.strip() == "":
            return default
    else:
        choice = input("Enter number: ")
        if choice.strip().lower() == "b":
            return None

    try:
        choice = int(choice)
        if 1 <= choice <= len(CATEGORIES):
            return CATEGORIES[choice - 1]
    except ValueError:
        pass
    print("❌ Invalid choice, defaulting to 'Other'")
    return "Other"

def add_expense():
    print("\n--- Add Expense (type 'B' to go back) ---")
    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date.strip().lower() == "b":
        return
    if date.strip() == "":
        date = datetime.now().strftime("%Y-%m-%d")

    category = choose_category()
    if category is None:
        return

    amount = input("Enter amount: ")
    if amount.strip().lower() == "b":
        return

    description = input("Enter description: ")
    if description.strip().lower() == "b":
        return

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount, description])

    print("✅ Expense added successfully!")

def view_expenses():
    print("\n--- All Expenses (press Enter to go back) ---")
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        for idx, row in enumerate(reader):
            print(f"{idx}. " + "\t".join(row))
    input("\nPress Enter to return to main menu...")

def total_expenses():
    print("\n--- Total Expenses ---")
    total = 0
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            try:
                total += float(row[2])
            except ValueError:
                pass
    print(f"💰 Total Expenses: {total}")
    input("\nPress Enter to return to main menu...")

def delete_expense():
    with open(FILE_NAME, mode="r") as file:
        rows = list(csv.reader(file))

    print("\n--- Delete Expense (type 'B' to go back) ---")
    view_expenses()
    choice = input("Enter the index of the expense to delete: ")
    if choice.strip().lower() == "b":
        return

    try:
        choice = int(choice)
        if choice == 0:
            print("❌ You cannot delete the header row!")
            return
        removed = rows.pop(choice)
        print(f"🗑 Deleted: {removed}")
    except (ValueError, IndexError):
        print("❌ Invalid index!")
        return

    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def edit_expense():
    with open(FILE_NAME, mode="r") as file:
        rows = list(csv.reader(file))

    print("\n--- Edit Expense (type 'B' to go back) ---")
    view_expenses()
    choice = input("Enter the index of the expense to edit: ")
    if choice.strip().lower() == "b":
        return

    try:
        choice = int(choice)
        if choice == 0:
            print("❌ You cannot edit the header row!")
            return
        expense = rows[choice]
    except (ValueError, IndexError):
        print("❌ Invalid index!")
        return

    print("Press Enter to keep the current value.")
    date = input(f"Date ({expense[0]}): ")
    if date.strip().lower() == "b":
        return
    date = date or expense[0]

    category = choose_category(default=expense[1])
    if category is None:
        return

    amount = input(f"Amount ({expense[2]}): ")
    if amount.strip().lower() == "b":
        return
    amount = amount or expense[2]

    description = input(f"Description ({expense[3]}): ")
    if description.strip().lower() == "b":
        return
    description = description or expense[3]

    rows[choice] = [date, category, amount, description]
    print("✏ Expense updated successfully!")

    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def main():
    while True:
        print("\n Personal Expense Tracker")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Total Expenses")
        print("4. Delete Expense")
        print("5. Edit Expense")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            total_expenses()
        elif choice == "4":
            delete_expense()
        elif choice == "5":
            edit_expense()
        elif choice == "6":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice, please try again.")

if __name__ == "__main__":
    main()

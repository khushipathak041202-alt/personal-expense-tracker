"""Simple Expense Tracker — beginner-friendly Python project.

Run with: python expense_tracker.py
Data is saved locally in expenses.csv.
"""
import csv
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]


def load_expenses():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def add_expense():
    category = input("Category (e.g. Food, Travel): ").strip()
    description = input("Description: ").strip()
    try:
        amount = float(input("Amount (INR): ").strip())
        if amount <= 0:
            print("Amount must be greater than zero.")
            return
    except ValueError:
        print("Please enter a valid number.")
        return

    file_exists = DATA_FILE.exists()
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        if not file_exists:
            writer.writeheader()
        writer.writerow({
            "date": date.today().isoformat(),
            "category": category or "Other",
            "description": description or "-",
            "amount": f"{amount:.2f}",
        })
    print("Expense saved.")


def show_expenses():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    print("\nDate        | Category      | Description                 | Amount (INR)")
    print("-" * 78)
    for item in expenses:
        print(
            f"{item['date']:<11}| {item['category']:<14}| "
            f"{item['description'][:27]:<28}| ₹{float(item['amount']):>10.2f}"
        )


def show_summary():
    expenses = load_expenses()
    if not expenses:
        print("No expenses recorded yet.")
        return
    total = sum(float(item["amount"]) for item in expenses)
    by_category = {}
    for item in expenses:
        by_category[item["category"]] = (
            by_category.get(item["category"], 0.0) + float(item["amount"])
        )
    print(f"\nTotal expenses: ₹{total:.2f}")
    print("By category:")
    for category, amount in sorted(by_category.items()):
        print(f"  {category}: ₹{amount:.2f}")


def main():
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Show summary")
        print("4. Exit")
        choice = input("Choose 1-4: ").strip()
        if choice == "1":
            add_expense()
        elif choice == "2":
            show_expenses()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Goodbye!")
            break
        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()

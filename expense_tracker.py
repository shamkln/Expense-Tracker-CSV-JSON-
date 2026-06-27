"""
╔══════════════════════════════════════════════════════════════╗
║           EXPENSE TRACKER - CODTECH IT SOLUTIONS            ║
║                  Internship Project Task                     ║
╠══════════════════════════════════════════════════════════════╣
║  Name    : [Your Name]                                       ║
║  Company : CODTECH IT SOLUTIONS                             ║
║  ID      : [Your Intern ID]                                  ║
║  Domain  : Python Programming                               ║
║  Duration: [Internship Duration]                            ║
║  Mentor  : [Mentor Name]                                     ║
╚══════════════════════════════════════════════════════════════╝
"""

import csv
import json
import os
import sys
from datetime import datetime

# ─── File Paths ───────────────────────────────────────────────
CSV_FILE  = "expenses.csv"
JSON_FILE = "expenses.json"

# ─── CSV Fieldnames ───────────────────────────────────────────
FIELDNAMES = ["ID", "Date", "Category", "Description", "Amount"]

CATEGORIES = [
    "Food & Dining",
    "Transportation",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Education",
    "Bills & Utilities",
    "Travel",
    "Personal Care",
    "Others",
]

# ══════════════════════════════════════════════════════════════
#  HELPER UTILITIES
# ══════════════════════════════════════════════════════════════

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line(char="═", width=60):
    print(char * width)


def header(title: str):
    clear()
    line()
    print(f"{'EXPENSE TRACKER':^60}")
    print(f"{'CODTECH IT SOLUTIONS':^60}")
    line()
    print(f"  ► {title}")
    line("─")


def pause():
    input("\n  Press ENTER to continue...")


def get_next_id(expenses: list) -> int:
    if not expenses:
        return 1
    return max(int(e["ID"]) for e in expenses) + 1


def fmt_amount(amount) -> str:
    return f"₹{float(amount):,.2f}"


def fmt_row(exp: dict) -> str:
    return (
        f"  {str(exp['ID']).ljust(4)} "
        f"{exp['Date'].ljust(12)} "
        f"{exp['Category'][:18].ljust(19)} "
        f"{exp['Description'][:14].ljust(15)} "
        f"{fmt_amount(exp['Amount']).rjust(10)}"
    )


# ══════════════════════════════════════════════════════════════
#  CSV OPERATIONS
# ══════════════════════════════════════════════════════════════

def load_csv() -> list:
    """Load expenses from CSV file."""
    if not os.path.exists(CSV_FILE):
        return []
    with open(CSV_FILE, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_csv(expenses: list):
    """Save all expenses to CSV file."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(expenses)


# ══════════════════════════════════════════════════════════════
#  JSON OPERATIONS
# ══════════════════════════════════════════════════════════════

def load_json() -> list:
    """Load expenses from JSON file."""
    if not os.path.exists(JSON_FILE):
        return []
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_json(expenses: list):
    """Save all expenses to JSON file."""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(expenses, f, indent=4, ensure_ascii=False)


# ══════════════════════════════════════════════════════════════
#  SYNC — keep CSV & JSON in sync always
# ══════════════════════════════════════════════════════════════

def load_expenses() -> list:
    """Load expenses (prefer CSV as primary source)."""
    csv_data  = load_csv()
    json_data = load_json()
    # Use whichever has more records (safety net)
    return csv_data if len(csv_data) >= len(json_data) else json_data


def save_expenses(expenses: list):
    """Save to both CSV and JSON."""
    save_csv(expenses)
    save_json(expenses)
    print("\n  ✔  Saved to expenses.csv  and  expenses.json")


# ══════════════════════════════════════════════════════════════
#  FEATURE 1 — ADD EXPENSE
# ══════════════════════════════════════════════════════════════

def add_expense():
    header("ADD NEW EXPENSE")

    # Date
    today = datetime.now().strftime("%Y-%m-%d")
    date_input = input(f"  Date (YYYY-MM-DD) [default: {today}]: ").strip()
    if not date_input:
        date_input = today
    else:
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            print("  ✖  Invalid date format. Using today's date.")
            date_input = today

    # Category
    print("\n  CATEGORIES:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"    {i:>2}. {cat}")
    while True:
        try:
            cat_choice = int(input("\n  Select category (1-10): ").strip())
            if 1 <= cat_choice <= len(CATEGORIES):
                category = CATEGORIES[cat_choice - 1]
                break
            print("  ✖  Enter a number between 1 and 10.")
        except ValueError:
            print("  ✖  Please enter a valid number.")

    # Description
    description = input("  Description: ").strip()
    if not description:
        description = "No description"

    # Amount
    while True:
        try:
            amount = float(input("  Amount (₹): ").strip())
            if amount <= 0:
                print("  ✖  Amount must be greater than 0.")
                continue
            break
        except ValueError:
            print("  ✖  Please enter a valid number.")

    expenses = load_expenses()
    new_id    = get_next_id(expenses)

    new_expense = {
        "ID"         : new_id,
        "Date"       : date_input,
        "Category"   : category,
        "Description": description,
        "Amount"     : round(amount, 2),
    }

    expenses.append(new_expense)
    save_expenses(expenses)

    line("─")
    print(f"\n  ✔  Expense #{new_id} added successfully!")
    print(f"     {category} — {description} — {fmt_amount(amount)}")
    pause()


# ══════════════════════════════════════════════════════════════
#  FEATURE 2 — VIEW ALL EXPENSES
# ══════════════════════════════════════════════════════════════

def view_expenses():
    header("ALL EXPENSES")
    expenses = load_expenses()

    if not expenses:
        print("  No expenses recorded yet.")
        pause()
        return

    print(f"  {'ID':<4} {'Date':<12} {'Category':<19} {'Description':<15} {'Amount':>10}")
    line("─")
    for exp in expenses:
        print(fmt_row(exp))

    line("─")
    total = sum(float(e["Amount"]) for e in expenses)
    print(f"  {'TOTAL':>52} {fmt_amount(total):>10}")
    print(f"\n  Total records: {len(expenses)}")
    pause()


# ══════════════════════════════════════════════════════════════
#  FEATURE 3 — DELETE EXPENSE
# ══════════════════════════════════════════════════════════════

def delete_expense():
    header("DELETE EXPENSE")
    expenses = load_expenses()

    if not expenses:
        print("  No expenses to delete.")
        pause()
        return

    view_expenses()
    header("DELETE EXPENSE")

    try:
        del_id = int(input("  Enter Expense ID to delete: ").strip())
    except ValueError:
        print("  ✖  Invalid ID.")
        pause()
        return

    found = [e for e in expenses if int(e["ID"]) == del_id]
    if not found:
        print(f"  ✖  No expense found with ID {del_id}.")
        pause()
        return

    print(f"\n  Record to delete:")
    print(fmt_row(found[0]))
    confirm = input("\n  Are you sure? (y/n): ").strip().lower()
    if confirm != "y":
        print("  Cancelled.")
        pause()
        return

    expenses = [e for e in expenses if int(e["ID"]) != del_id]
    save_expenses(expenses)
    print(f"\n  ✔  Expense #{del_id} deleted successfully!")
    pause()


# ══════════════════════════════════════════════════════════════
#  FEATURE 4 — SEARCH & FILTER
# ══════════════════════════════════════════════════════════════

def search_expenses():
    header("SEARCH & FILTER EXPENSES")
    expenses = load_expenses()

    if not expenses:
        print("  No expenses recorded yet.")
        pause()
        return

    print("  Search by:")
    print("    1. Category")
    print("    2. Date (YYYY-MM or YYYY-MM-DD)")
    print("    3. Description keyword")
    choice = input("\n  Select (1-3): ").strip()

    results = []

    if choice == "1":
        print("\n  CATEGORIES:")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"    {i:>2}. {cat}")
        cat_no = input("\n  Select category (1-10): ").strip()
        try:
            cat_no = int(cat_no)
            category = CATEGORIES[cat_no - 1]
            results = [e for e in expenses if e["Category"] == category]
        except (ValueError, IndexError):
            print("  ✖  Invalid choice.")
            pause()
            return

    elif choice == "2":
        date_q = input("  Enter date/month (e.g. 2025-06 or 2025-06-15): ").strip()
        results = [e for e in expenses if e["Date"].startswith(date_q)]

    elif choice == "3":
        keyword = input("  Enter keyword: ").strip().lower()
        results = [e for e in expenses if keyword in e["Description"].lower()]

    else:
        print("  ✖  Invalid option.")
        pause()
        return

    line("─")
    if not results:
        print("  No matching records found.")
    else:
        print(f"  {'ID':<4} {'Date':<12} {'Category':<19} {'Description':<15} {'Amount':>10}")
        line("─")
        for exp in results:
            print(fmt_row(exp))
        line("─")
        total = sum(float(e["Amount"]) for e in results)
        print(f"  Found {len(results)} record(s) | Total: {fmt_amount(total)}")

    pause()


# ══════════════════════════════════════════════════════════════
#  FEATURE 5 — SUMMARY / STATISTICS
# ══════════════════════════════════════════════════════════════

def summary():
    header("EXPENSE SUMMARY & STATISTICS")
    expenses = load_expenses()

    if not expenses:
        print("  No expenses recorded yet.")
        pause()
        return

    totals = {}
    for e in expenses:
        cat = e["Category"]
        totals[cat] = totals.get(cat, 0) + float(e["Amount"])

    grand_total = sum(totals.values())

    print(f"\n  {'CATEGORY':<25} {'AMOUNT':>12}  {'SHARE':>7}  BAR")
    line("─")

    sorted_cats = sorted(totals.items(), key=lambda x: x[1], reverse=True)
    max_val = sorted_cats[0][1] if sorted_cats else 1

    for cat, amt in sorted_cats:
        pct  = (amt / grand_total) * 100
        bars = int((amt / max_val) * 20)
        bar  = "█" * bars
        print(f"  {cat:<25} {fmt_amount(amt):>12}  {pct:>6.1f}%  {bar}")

    line("─")
    print(f"  {'GRAND TOTAL':<25} {fmt_amount(grand_total):>12}")

    # Monthly breakdown
    months = {}
    for e in expenses:
        month = e["Date"][:7]
        months[month] = months.get(month, 0) + float(e["Amount"])

    print(f"\n  MONTHLY BREAKDOWN")
    line("─")
    for month, amt in sorted(months.items()):
        print(f"  {month}     {fmt_amount(amt):>12}")

    print(f"\n  Highest expense category : {sorted_cats[0][0]}")
    print(f"  Total number of entries  : {len(expenses)}")
    print(f"  Average expense amount   : {fmt_amount(grand_total / len(expenses))}")

    pause()


# ══════════════════════════════════════════════════════════════
#  FEATURE 6 — EXPORT
# ══════════════════════════════════════════════════════════════

def export_data():
    header("EXPORT DATA")
    expenses = load_expenses()

    if not expenses:
        print("  No expenses to export.")
        pause()
        return

    print("  Data is automatically saved to:")
    print(f"    📄  {os.path.abspath(CSV_FILE)}")
    print(f"    📋  {os.path.abspath(JSON_FILE)}")
    print("\n  Re-saving files now...")
    save_expenses(expenses)
    print(f"\n  ✔  Export complete!  ({len(expenses)} records)")
    pause()


# ══════════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════════

MENU = {
    "1": ("Add New Expense",          add_expense),
    "2": ("View All Expenses",         view_expenses),
    "3": ("Delete an Expense",         delete_expense),
    "4": ("Search & Filter Expenses",  search_expenses),
    "5": ("Summary & Statistics",      summary),
    "6": ("Export (CSV & JSON)",       export_data),
    "0": ("Exit",                      None),
}


def main_menu():
    while True:
        header("MAIN MENU")
        expenses = load_expenses()
        total    = sum(float(e["Amount"]) for e in expenses)

        print(f"  Records: {len(expenses)}   |   Total Spending: {fmt_amount(total)}")
        line("─")

        for key, (label, _) in MENU.items():
            prefix = "✖" if key == "0" else f"{key}"
            print(f"  [{prefix}] {label}")

        line("─")
        choice = input("  Select option: ").strip()

        if choice == "0":
            clear()
            print("\n  Thank you for using Expense Tracker!")
            print("  — CODTECH IT SOLUTIONS —\n")
            sys.exit(0)

        if choice in MENU:
            _, func = MENU[choice]
            func()
        else:
            print("  ✖  Invalid option. Try again.")
            pause()


# ══════════════════════════════════════════════════════════════
#  ENTRY POINT
# ══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    main_menu()

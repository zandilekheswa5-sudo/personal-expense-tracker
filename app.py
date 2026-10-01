import json
import csv
from datetime import date


# -----------------------------
# Load existing expenses
# -----------------------------

try:
    with open("expenses.json", "r") as file:
        expenses = json.load(file)
except (FileNotFoundError, json.JSONDecodeError):
    expenses = []


# -----------------------------
# Main Menu
# -----------------------------

while True:

    print("\n" + "=" * 40)
    print("💰 Personal Expense Tracker")
    print("=" * 40)

    print("1. Add Expense")
    print("2. View Expenses")
    print("3. View Total")
    print("4. Delete Expense")
    print("5. Exit")

    choice = input("\nChoose an option: ")


    # -----------------------------
    # 1. Add Expense
    # -----------------------------

    if choice == "1":

        description = input("\nWhat did you spend money on? ")

        print("\nCategories:")
        print("1. Food")
        print("2. Transport")
        print("3. Shopping")
        print("4. Bills")
        print("5. Entertainment")
        print("6. Other")

        category_choice = input("Choose a category: ")

        categories = {
            "1": "Food",
            "2": "Transport",
            "3": "Shopping",
            "4": "Bills",
            "5": "Entertainment",
            "6": "Other"
        }

        category = categories.get(category_choice, "Other")


        # -----------------------------
        # Validate Amount
        # -----------------------------

        while True:

            try:
                amount = float(
                    input("How much did you spend? R")
                )

                if amount <= 0:
                    print("❌ Amount must be greater than R0.")
                    continue

                break

            except ValueError:
                print("❌ Please enter a valid number.")


        # -----------------------------
        # Create Expense
        # -----------------------------

        expense = {
            "date": str(date.today()),
            "description": description,
            "category": category,
            "amount": amount
        }


        # Add expense to list FIRST
        expenses.append(expense)


        # -----------------------------
        # Save to JSON
        # -----------------------------

        with open("expenses.json", "w") as file:
            json.dump(expenses, file, indent=4)


        # -----------------------------
        # Save to CSV
        # -----------------------------

        with open("expenses.csv", "w", newline="") as file:

            fieldnames = [
                "date",
                "description",
                "category",
                "amount"
            ]

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames
            )

            writer.writeheader()
            writer.writerows(expenses)


        # -----------------------------
        # Success Message
        # -----------------------------

        print("\n✅ Expense added successfully!")
        print(f"📅 Date: {expense['date']}")
        print(f"📝 Description: {expense['description']}")
        print(f"🏷️ Category: {expense['category']}")
        print(f"💰 Amount: R{expense['amount']:.2f}")


    # -----------------------------
    # 2. View Expenses
    # -----------------------------

    elif choice == "2":

        print("\n📋 Your Expenses")
        print("=" * 75)

        if not expenses:

            print("No expenses recorded yet.")

        else:

            print(
                f"{'Date':<12} | "
                f"{'Description':<20} | "
                f"{'Category':<15} | "
                f"{'Amount':>10}"
            )

            print("-" * 75)

            for expense in expenses:

                print(
                    f"{expense['date']:<12} | "
                    f"{expense['description']:<20} | "
                    f"{expense['category']:<15} | "
                    f"R{expense['amount']:>9.2f}"
                )


    # -----------------------------
    # 3. View Total
    # -----------------------------

    elif choice == "3":

        total = sum(
            expense["amount"]
            for expense in expenses
        )

        category_totals = {}


        # Calculate totals by category

        for expense in expenses:

            category = expense["category"]
            amount = expense["amount"]

            if category not in category_totals:
                category_totals[category] = 0

            category_totals[category] += amount


        # -----------------------------
        # Spending Summary
        # -----------------------------

        print("\n📊 Spending Summary")
        print("=" * 30)

        if not expenses:

            print("No expenses recorded yet.")

        else:

            for category, amount in category_totals.items():

                print(
                    f"{category}: R{amount:.2f}"
                )

            print("-" * 30)

            print(
                f"💰 Total Expenses: R{total:.2f}"
            )


    # -----------------------------
    # 4. Delete Expense
    # -----------------------------

    elif choice == "4":

        print("\n🗑️ Delete Expense")
        print("=" * 40)


        if not expenses:

            print("No expenses to delete.")

        else:

            # Show expenses with numbers

            for index, expense in enumerate(
                expenses,
                start=1
            ):

                print(
                    f"{index}. "
                    f"{expense['date']} | "
                    f"{expense['description']} | "
                    f"{expense['category']} | "
                    f"R{expense['amount']:.2f}"
                )


            # Ask which expense to delete

            try:

                delete_choice = int(
                    input(
                        "\nChoose an expense to delete: "
                    )
                )


                if (
                    delete_choice < 1
                    or delete_choice > len(expenses)
                ):

                    print(
                        "❌ Invalid expense number."
                    )

                else:

                    deleted_expense = expenses.pop(
                        delete_choice - 1
                    )


                    # Save updated JSON

                    with open(
                        "expenses.json",
                        "w"
                    ) as file:

                        json.dump(
                            expenses,
                            file,
                            indent=4
                        )


                    # Save updated CSV

                    with open(
                        "expenses.csv",
                        "w",
                        newline=""
                    ) as file:

                        fieldnames = [
                            "date",
                            "description",
                            "category",
                            "amount"
                        ]

                        writer = csv.DictWriter(
                            file,
                            fieldnames=fieldnames
                        )

                        writer.writeheader()
                        writer.writerows(expenses)


                    print(
                        "\n✅ Expense deleted successfully!"
                    )

                    print(
                        f"🗑️ Deleted: "
                        f"{deleted_expense['description']} "
                        f"— R{deleted_expense['amount']:.2f}"
                    )


            except ValueError:

                print(
                    "❌ Please enter a valid expense number."
                )


    # -----------------------------
    # 5. Exit
    # -----------------------------

    elif choice == "5":

        print("\n👋 Goodbye!")
        break


    # -----------------------------
    # Invalid Menu Option
    # -----------------------------

    else:

        print(
            "\n❌ Invalid option. "
            "Please choose 1-5."
        )
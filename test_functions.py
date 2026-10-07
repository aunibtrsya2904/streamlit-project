from budget_module import calculate_remaining_budget, check_budget_status

budget = 1000
total_expenses = 700

remaining = calculate_remaining_budget(budget, total_expenses)
status = check_budget_status(remaining)

print("Budget: RM", budget)
print("Total Expenses: RM", total_expenses)
print("Remaining Budget: RM", remaining)
print("Status:", status)
from budget_class import StudentExpense

student1 = StudentExpense(
    "Nur",
    1000,
    "Food",
    700
)

print("Student Name:", student1.student_name)
print("Monthly Budget: RM", student1.monthly_budget)
print("Category:", student1.category)
print("Expense: RM", student1.amount)

print("Remaining Budget: RM", student1.calculate_remaining())
print("Status:", student1.get_status())
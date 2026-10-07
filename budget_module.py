# Fungsi 1: Data processing / calculation (Memenuhi kriteria a)
def calculate_remaining_budget(budget, total_expenses):
    return budget - total_expenses

# Fungsi 2: Decision making / status check (Memenuhi kriteria a)
def check_budget_status(remaining, budget):
    if budget <= 0:
        return "Invalid Budget"
    percentage = (remaining / budget) * 100
    if remaining < 0:
        return "Over Budget"
    elif percentage <= 20:
        return "Almost Exceeded"
    else:
        return "Within Budget"

# Parent Class (Memenuhi kriteria b & d)
class Expense:
    def __init__(self, item_name, category, amount, date_added):
        # 4 Atribut pada class
        self.item_name = item_name
        self.category = category
        self.amount = float(amount)
        self.date_added = date_added

    def display_details(self):
        return f"{self.item_name} ({self.category}): RM{self.amount:.2f}"

# Child Class / Subclass (Memenuhi kriteria d - Inheritance)
class StudentExpenseTracker(Expense):
    def __init__(self, student_name, monthly_budget, item_name="", category="", amount=0.0, date_added=""):
        super().__init__(item_name, category, amount, date_added)
        self.student_name = student_name
        self.monthly_budget = float(monthly_budget)

    # Method pengiraan
    def calculate_total_expenses(self, expense_list):
        return sum(item['amount'] for item in expense_list)

    # Method status
    def get_budget_percentage(self, total_spent):
        if self.monthly_budget <= 0:
            return 0.0
        return min(total_spent / self.monthly_budget, 1.0)
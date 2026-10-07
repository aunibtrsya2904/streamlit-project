class StudentExpense:

    def __init__(self, student_name, monthly_budget, category, amount):
        self.student_name = student_name
        self.monthly_budget = monthly_budget
        self.category = category
        self.amount = amount

    def calculate_remaining(self):
        return self.monthly_budget - self.amount

    def get_status(self):
        remaining = self.calculate_remaining()

        if remaining < 0:
            return "Over Budget"
        elif remaining <= 100:
            return "Almost Exceeded"
        else:
            return "Within Budget"
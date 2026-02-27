from datetime import datetime, timedelta


class InvestmentSimulator:

    def __init__(
        self,
        monthly_investment: float,
        interest_rate: float,
        begin: datetime | None = None,
        end: datetime | None = None,
        goal: float | None = None,
        initial_value: float | None = None,
        bonus: dict[int, float] | None = {},
    ):

        self.begin = datetime.now() if not begin else begin

        if not end and not goal:
            raise ValueError(
                "At least an end date or a final goal must be set to continue."
            )

        self.goal = goal
        self.end = end
        self.monthly_investment = monthly_investment
        self.interest_rate = interest_rate
        self.monthly_interest_rate = (1 + self.interest_rate) ** (1 / 12) - 1
        self.initial_value = initial_value if initial_value else 0.0
        self.bonus = bonus
        self.evolution = {}

    def simulate(self):

        date = self.begin
        value = self.initial_value
        while True:
            date += timedelta(days=30)
            value *= 1 + self.monthly_interest_rate
            value += self.monthly_investment

            value += self.add_bonus(date)

            self.save_point(date, value)

            if not self.iterate(date, value):
                break

        return self.calculate_final(date, value)

    def iterate(self, date, value):

        if self.goal and self.goal > value:
            return True

        if self.end and self.end >= date:
            return True

    def add_bonus(self, date):

        if str(date.month) in self.bonus:
            return self.bonus[str(date.month)]
        return 0.0

    def save_point(self, date, value):
        self.evolution[date] = value
        with open("dados.txt", "a", encoding="utf-8") as arq:
            arq.write(f"{date.strftime('%Y-%m-%d')}:{value}")
            arq.write(f"\n")

    def calculate_final(self, date, value):

        final_dict = {}

        final_dict["final_date"] = date.isoformat()
        final_dict["goal"] = value
        final_dict["evolution"] = self.evolution

        return final_dict

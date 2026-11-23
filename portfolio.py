# Fintual - 2026 
# Fabrizio Barisione at gmail.com
# Review this code along with either the excalidraw export and / or the PNG file
from dataclasses import dataclass
from math import isclose, isfinite
from random import randint

# Utilitary code (Constant + functions)

INVESTMENT_CLP_LIMIT = 1_000_000_000 # Arbitrary value

def get_current_stock_price(stock_name: str) -> int:
    return randint(100, 1000)


def report(portfolio_name: str, stock_name: str, stock_price: int, quantity: float, action: str) -> None:
    print(f"{portfolio_name} | {stock_name} (price: {stock_price}) : {action} {quantity:.1f} shares --- (Debugging invesment check : {quantity * stock_price})")


# Required classes and methods
@dataclass
class Stock:
    name: str
    price: float = 0
    quantity: float = 0

    def update_price(self) -> None:
        self.price = get_current_stock_price(self.name)


@dataclass
class AllocatedStock:
    stock: Stock
    percentage: float


@dataclass
class Portfolio:
    name: str
    clp_invested: int
    allocated_stocks: list[AllocatedStock]
    # Validating input (You can say is optional since this is an excersise)
    def __post_init__(self):
        if isinstance(self.clp_invested, int) and not (self.clp_invested <= INVESTMENT_CLP_LIMIT and self.clp_invested > 0):
            raise ValueError(f"Invested CLP must be a positive integer between [1, {INVESTMENT_CLP_LIMIT}].")
        percentages = [item.percentage for item in self.allocated_stocks]
        # Elegant way to validate that the sum of all percentages ~= 100
        if any(not isfinite(p) or p < 0 for p in percentages) or not isclose(
            sum(percentages), 100, rel_tol=0, abs_tol=1e-9
        ):
            raise ValueError("Allocations % must be positive and sum to 100%.")
        names = [item.stock.name for item in self.allocated_stocks]
        if len(names) != len(set(names)):
            raise ValueError("Stock names must be unique.")
        for item in self.allocated_stocks:
            if not isfinite(item.stock.quantity) or item.stock.quantity < 0:
                raise ValueError("Stock quantities must be positive and finite.")

    def rebalance(self) -> None:
        # See Simplified Rebalance flow, 2. Rebalance algorithm in the attached excalidraw PNG export
        for item in self.allocated_stocks:
            item.stock.update_price() # setCurrentPrice(), our "prerequisite"

        # for item in self.allocated_stocks:
            stock = item.stock
            target_value = self.clp_invested * item.percentage / 100
            current_value = stock.price * stock.quantity
            difference = target_value - current_value
            # Ignore differences of 0.001 CLP or less.
            if abs(difference) <= 0.001:
                report(self.name, stock.name, stock.price, 0, "keep")
            else:
                action = "buy" if difference > 0 else "sell"
                report(self.name, stock.name, stock.price, abs(difference) / stock.price, action)

# Another utilitary function
def create_portfolio(
    name: str,
    allocated_stocks: dict[str, int],
    clp_invested: int,
    quantities: dict[str, int] | None = None,
) -> Portfolio:
    print(allocated_stocks)
    quantities = quantities or {}
    # validating that all quantities must refer to allocated stocks, rest must be 0
    # Ejem if allocated_stocks={"meta": 30} a quantity = {"PelotiyehueCo": 100} is not valid
    if quantities.keys() - allocated_stocks.keys():
        raise ValueError("Quantities must refer to allocated stocks.")
    return Portfolio(
        name=name,
        clp_invested=clp_invested,
        allocated_stocks=[
            AllocatedStock(Stock(stock_name, quantity=quantities.get(stock_name, 0)), percentage)
            for stock_name, percentage in allocated_stocks.items()
        ],
    )

# Standalone test, first creates a portfolio and then run a rebalance 5 times in a row, 
# reporting the outcome on each iteration
if __name__ == "__main__":
    portfolio = create_portfolio(
        name="mi inversion",
        allocated_stocks={"meta": 30, "Microsoft": 40, "Fintual": 30},
        clp_invested=INVESTMENT_CLP_LIMIT,
    )

    # Run the rebalancing method 5 times (where 5 was arbitrarily chosen)
    for i in range(1, 6):
        print(f"rebalancing iteration number : {i}")
        portfolio.rebalance()

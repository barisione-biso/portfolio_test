# Fintual - 2026 
# Fabrizio Barisione at gmail.com
from dataclasses import dataclass
from math import isclose, isfinite
from random import randint


def get_current_stock_price(stock_name: str) -> int:
    return randint(100, 1000)


def report(portfolio_name: str, stock_name: str, stock_price: int, quantity: float, action: str):
    print(f"{portfolio_name} | {stock_name} (price: {stock_price}) : {action} {quantity:.1f} shares (total $: {quantity * stock_price})")


@dataclass
class Stock:
    name: str
    price: float = 0
    quantity: float = 0

    def set_current_price(self):
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

    def __post_init__(self):
        if isinstance(self.clp_invested, int) and not isfinite(self.clp_invested) or self.clp_invested <= 0:
            raise ValueError("Invested CLP must be a positive and finite integer.")
        percentages = [item.percentage for item in self.allocated_stocks]
        if any(not isfinite(p) or p < 0 for p in percentages) or not isclose(
            sum(percentages), 100, rel_tol=0, abs_tol=1e-9
        ):
            raise ValueError("Allocations must be nonnegative and sum to 100%.")
        names = [item.stock.name for item in self.allocated_stocks]
        if len(names) != len(set(names)):
            raise ValueError("Stock names must be unique.")
        for item in self.allocated_stocks:
            if not isfinite(item.stock.quantity) or item.stock.quantity < 0:
                raise ValueError("Stock quantities must be nonnegative and finite.")

    def rebalance(self):
        for item in self.allocated_stocks:
            item.stock.set_current_price()

        for item in self.allocated_stocks:
            stock = item.stock
            target_value = self.clp_invested * item.percentage / 100
            current_value = stock.price * stock.quantity
            difference = target_value - current_value
            if isclose(difference, 0, rel_tol=0, abs_tol=1e-6):
                report(self.name, stock.name, stock.price, 0, "keep")
            else:
                action = "buy" if difference > 0 else "sell"
                report(self.name, stock.name, stock.price, abs(difference) / stock.price, action)


def create_portfolio(
    name: str,
    allocated_stocks: dict[str, int],
    clp_invested: int,
    quantities: dict[str, int] | None = None,
) -> Portfolio:
    print(allocated_stocks)
    quantities = quantities or {}
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


if __name__ == "__main__":
    portfolio = create_portfolio(
        name="mi inversion",
        allocated_stocks={"meta": 30, "Microsoft": 40, "Fintual": 30},
        clp_invested=1_000_000,
    )
    for i in range(1, 6):
        print(f"rebalancing number : {i}")
        portfolio.rebalance()

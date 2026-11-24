# Fintual - 2026 
# Fabrizio Barisione at gmail.com
# Review this code along with either the excalidraw export and / or the PNG file
# Two part in this file were flagged with chatgpt usage
from dataclasses import dataclass
from math import isclose, isfinite
from random import randint

# Utilitary code (Constant + functions)

INVESTMENT_CLP_LIMIT = 1_000_000_000 # Arbitrary value

def get_current_stock_price(stock_name: str) -> int:
    return randint(100, 1000)


def report(portfolio_name: str, stock_name: str, stock_price: int, quantity: float, action: str) -> None:
    print(f"{portfolio_name} | {stock_name} (price: {stock_price}) : {action} {quantity:.1f} shares")


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
    def _validate_input(self) -> None:
        if type(self.clp_invested) is not int and not (self.clp_invested <= INVESTMENT_CLP_LIMIT and self.clp_invested > 0):
            raise ValueError(f"Invested CLP must be a positive integer between [1, {INVESTMENT_CLP_LIMIT}].")
        percentages = [item.percentage for item in self.allocated_stocks]
        # Elegant way to validate that the sum of all percentages ~= 100 
        # IMPORTANT: I used chatgpt for this validation
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

    
    def _start_investment(self) -> None: 
        print(f"Simulating the investment of {self.clp_invested} with name '{self.name}'")
        ratios = {item.stock.name: item.percentage for item in self.allocated_stocks}
        print(f"Stock ratio = {ratios}")
        for item in self.allocated_stocks:
            stock = item.stock
            stock.update_price() # setCurrentPrice(), our "prerequisite"
            amount = self.clp_invested * item.percentage / 100
            stock.quantity = amount / stock.price
            report(self.name, stock.name, stock.price, stock.quantity, "buy")
        print(f"portfolio value  = {self.clp_invested}") 

    def __post_init__(self) -> None:
        self._validate_input()

        self._start_investment()
    # The rebalance method implements a three step process:
    # 1. first updates the stock prices and reports the total portfolio value
    # 2. Then calculates what to trade
    # 3. Finally, executes the selling and with that money, buys stocks 
    # IMPORTANT: the process assumes that the customer is not able to inject more money to the portfolio and that there aren't any fees availables
    def rebalance(self) -> None:
        to_sell = []
        to_buy = []
        earnings = 0.0
        #1
        total_portfolio = 0.0
        for item in self.allocated_stocks:
            stock = item.stock
            stock.update_price() # setCurrentPrice(), our "prerequisite"
            total_portfolio = total_portfolio + stock.price  * stock.quantity

        #2 Then, per each allocated stocks we calculate whether to buy, sell or keep
        for item in self.allocated_stocks:
            stock = item.stock
            target_value = total_portfolio * item.percentage / 100
            current_value = stock.price * stock.quantity
            difference = target_value - current_value
            # Ignore differences of 0.01 CLP or less.
            if abs(difference) <= 0.01:
                report(self.name, stock.name, stock.price, 0, "keep")
            else:
                # Positive difference : Buy, otherwise sell but for that we need $
                quantity = difference / stock.price
                if difference > 0:
                    action = "buy"
                    to_buy.append((stock, quantity))
                else:
                    action = "sell" 
                    to_sell.append((stock, -quantity))
                report(self.name, stock.name, stock.price, abs(quantity), action)    
        print(f"portfolio value  = {total_portfolio:.1f}")
        #3. Finally execute the trades
        # IMPORTANT: I used chatgpt to validate my thought-process
        # Prompt "necesito restringir las compras a lo que tengo en acciones. Es decir, no podemos asumir que el cliente aporta más dinero"
        #       Respuesta "Exacto: las compras deben financiarse con las ventas, sin agregar dinero. Tu cálculo ya permite eso si usas el valor actual del portafolio y los porcentajes suman 100%. Para ejecutarlo, mantén un saldo disponible"
        print("Executing trading")
        # first sell and record the "earnings"
        for stock,quantity in to_sell:
            stock.quantity -= quantity
            earnings += quantity * stock.price

        # then spend, the budget is the earnings
        for stock, quantity in to_buy:
            quantity = min(quantity, earnings / stock.price)
            if quantity > 0:
                cost = min(quantity * stock.price, earnings)
                stock.quantity += quantity
                earnings -= cost
# Another utilitary function
def create_portfolio(
    name: str,
    allocated_stocks: dict[str, int],
    clp_invested: int,
    quantities: dict[str, int] | None = None,
) -> Portfolio:
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
        allocated_stocks={"PUCobre": 30, "CorporaTresMontes": 40, "Fintual": 30},
        clp_invested=10_000_000,
    )

    # Run the rebalancing method 5 times (where 5 was arbitrarily chosen)
    for i in range(1, 5):
        print(f"rebalancing iteration number : {i}")
        portfolio.rebalance()

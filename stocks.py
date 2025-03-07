import threading
import random
import time
from typing import List, Tuple

# Constants
MAX_TICKERS = 1024
MAX_ORDERS = 10000


class Order:
    def __init__(self, order_type: str, ticker_index: int, quantity: int, price: float):
        self.type = order_type          # either 'BUY' or 'SELL'
        self.ticker_index = ticker_index  # this is a stock ticker
        self.quantity = quantity        # number of shares
        self.price = price              # the price per share
        self.is_active = True           # check if the order is still active


class StockTradingEngine:
    def __init__(self):
        self.order_book: List[Order] = []  # List for storing all orders
        self.order_count = 0               # Counter for total number of orders
        self.lock = threading.Lock()       # Lock for threads

    def add_order(self, order_type: str, ticker_index: int, quantity: int, price: float):
        with self.lock:
            if self.order_count < MAX_ORDERS:
                new_order = Order(order_type, ticker_index, quantity, price)
                self.order_book.append(new_order)
                self.order_count += 1
                # Matching the new order
                self.match_order(self.order_count - 1)

    # O(n) time complexity where n is the number of orders in the Stock order book
    def match_order(self, new_order_index: int):
        new_order = self.order_book[new_order_index]
        if not new_order.is_active:
            return

        # Loop through all orders to identify a potential match
        for i in range(self.order_count):
            if i == new_order_index:
                continue

            existing_order = self.order_book[i]
            if not existing_order.is_active:
                continue

            # Ensure orders are for the same stock and have opposite buy/sell types
            if (new_order.ticker_index == existing_order.ticker_index and
                    new_order.type != existing_order.type):

                # Verify if the prices enable a matching transaction
                can_match = ((new_order.type == "BUY" and new_order.price >= existing_order.price) or
                             (new_order.type == "SELL" and new_order.price <= existing_order.price))

                if can_match:
                    matched_quantity = min(
                        new_order.quantity, existing_order.quantity)

                    # Update the quantities
                    new_order.quantity -= matched_quantity
                    existing_order.quantity -= matched_quantity

                    # Mark orders to inactive status if they are fully matched
                    if new_order.quantity == 0:
                        new_order.is_active = False
                    if existing_order.quantity == 0:
                        existing_order.is_active = False

                    # Print the match details
                    print(f"Matched order: Ticker {new_order.ticker_index}, "
                          f"Quantity {matched_quantity}, "
                          f"Price {existing_order.price if new_order.type == 'BUY' else new_order.price}")

                    # Terminate if the new order is completely matched
                    if new_order.quantity == 0:
                        break


def simulate_trading(engine: StockTradingEngine):
    while True:
        # Generate random parameters for the order
        order_type = random.choice(["BUY", "SELL"])
        ticker_index = random.randint(0, MAX_TICKERS - 1)
        quantity = random.randint(1, 100)
        price = round(random.uniform(1.0, 1000.0), 2)

        # Insert the randomly generated order into the trading engine
        engine.add_order(order_type, ticker_index, quantity, price)
        # Pause for 10 milliseconds to mimic real-time execution
        time.sleep(0.01)


if __name__ == "__main__":
    engine = StockTradingEngine()
    threads = []

    # Create and start 4 threads to simulate simultaneous trading operations
    for _ in range(4):
        thread = threading.Thread(target=simulate_trading, args=(engine,))
        threads.append(thread)
        thread.start()

    # Wait indefinitely for all threads to finish, even though they never will in this scenario
    for thread in threads:
        thread.join()

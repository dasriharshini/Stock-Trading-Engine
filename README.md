# Stock Trading Engine

## Overview
This project creates a real-time stock trading engine that matches Buy and Sell orders according to specific rules. It's built to handle up to 1,024 different stock tickers, simulating the fast-paced environment of a real-world trading platform with multiple stockbrokers placing orders simultaneously.

## Key Features
- Supports trading of up to 1,024 different stocks
- Handles both buy and sell orders
- Matches orders in real-time based on price and quantity
- Simulates concurrent trading with multiple threads
- Implements thread-safe operations to prevent race conditions

## How It Works

1. **Adding Orders**: The engine accepts buy and sell orders for various stocks. Each order includes:
   - Order type (buy or sell)
   - Stock ticker (represented as an index)
   - Quantity of shares
   - Price per share

2. **Matching Orders**: When a new order is added, the engine immediately tries to match it with existing orders. A match occurs when:
   - A buy order's price is greater than or equal to a sell order's price for the same stock
   - The orders are for the same stock but opposite types (buy vs. sell)

3. **Order Execution**: When a match is found, the engine:
   - Executes the trade for the matching quantity
   - Updates the remaining quantities for both orders
   - Marks fully executed orders as inactive

4. **Simulation**: The project includes a simulation feature that generates random orders to mimic real-world trading activity.

  ## Running the Simulation
To run the trading simulation:

1. Ensure you have Python installed on your system.
2. Run the script using: `python stocks.py`
3. The simulation will start, and you'll see output showing matched orders.

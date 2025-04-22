from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
from ibapi.common import OrderId  
import threading
import time

# Variables
symbol = None
quantity = None
contract = Contract()   
stop_price = None
limit_price = None
stop_loss_price = None
action = None


def create_contract_US_stock(symbol):
    contract = Contract()
    contract.symbol = symbol
    contract.secType = "STK"
    contract.exchange = "SMART"
    contract.currency = "USD"
    return contract


# def buy_stock_stop_limit_with_stop_loss_order(
#     app, contract, quantity, stop_price, limit_price, stop_loss_price, tif="DAY", transmit=False
# ):
#     """
#     Function to place a stop limit buy order with an attached stop loss order.

#     Parameters:
#         app: The IBKR app instance (EClient and EWrapper combined).
#         contract: The contract object for the stock.
#         quantity: The number of shares to buy.
#         stop_price: The stop price for the stop limit order.
#         limit_price: The limit price for the stop limit order.
#         stop_loss_price: The stop price for the stop loss order.
#         tif: Time in Force for the main order (default: "DAY").
#         transmit: Whether to transmit the orders immediately (default: False).
#     """
#     # Ensure the contract is a valid stock contract
#     if not isinstance(contract, Contract):
#         raise ValueError("The contract must be an instance of ibapi.contract.Contract.")
#     if contract.secType != "STK":
#         raise ValueError("The contract must be a stock contract (secType='STK').")

#     # Generate the parent order ID
#     parent_order_id = app.nextId()

#     # Main order: Stop Limit Buy

#     main_order = Order()
#     main_order.orderId = parent_order_id  # Set the order ID
#     main_order.orderType = "STP LMT"
#     main_order.action = "BUY"
#     main_order.totalQuantity = quantity
#     main_order.lmtPrice = limit_price
#     main_order.auxPrice = stop_price
#     main_order.tif = tif # Time in Force (DAY, GTC, etc.
#     main_order.transmit = False  # Do not transmit until the stop loss is attached

#     # Stop Loss order
#     stop_loss_order = Order()
#     stop_loss_order.orderId = app.nextId()  # Generate a new order ID for the stop loss order
#     stop_loss_order.orderType = "STP"
#     stop_loss_order.action = "SELL"
#     stop_loss_order.totalQuantity = quantity
#     stop_loss_order.auxPrice = stop_loss_price
#     stop_loss_order.tif = "GTC"  # Good Till Cancelled
#     stop_loss_order.parentId = parent_order_id  # Link to the main order
#     stop_loss_order.transmit = transmit  # Transmit both orders together

#     return(main_order, stop_loss_order)


def create_stock_stop_limit_with_stop_loss_order(
    action,
    app,
    contract,
    quantity,
    stop_price,
    limit_price,
    stop_loss_price,
    tif="DAY",
    transmit=False,
):
    """
    Function to place a stop limit order with an attached stop loss order.

    Parameters:
        action: The action for the order ("BUY" or "SELL").
        app: The IBKR app instance (EClient and EWrapper combined).
        contract: The contract object for the stock.
        quantity: The number of shares to trade.
        stop_price: The stop price for the stop limit order.
        limit_price: The limit price for the stop limit order.
        stop_loss_price: The stop price for the stop loss order.
        tif: Time in Force for the main order (default: "DAY").
        transmit: Whether to transmit the orders immediately (default: False).
    """
    # Ensure the contract is a valid stock contract
    if not isinstance(contract, Contract):
        raise ValueError("The contract must be an instance of ibapi.contract.Contract.")
    if contract.secType != "STK":
        raise ValueError("The contract must be a stock contract (secType='STK').")

    if action not in ["BUY", "SELL"]:
        raise ValueError("The action must be either 'BUY' or 'SELL'.")

    # Generate the parent order ID
    parent_order_id = app.nextId()

    # Main order: Stop Limit
    main_order = Order()
    main_order.orderId = parent_order_id  # Set the order ID
    main_order.orderType = "STP LMT"
    main_order.action = action
    main_order.totalQuantity = quantity
    main_order.lmtPrice = limit_price
    main_order.auxPrice = stop_price
    main_order.tif = tif  # Time in Force (DAY, GTC, etc.)
    main_order.transmit = False  # Do not transmit until the stop loss is attached

    # Stop Loss order
    stop_loss_order = Order()
    stop_loss_order.orderId = (
        app.nextId()
    )  # Generate a new order ID for the stop loss order
    stop_loss_order.orderType = "STP"
    stop_loss_order.action = "SELL" if action == "BUY" else "BUY"
    stop_loss_order.totalQuantity = quantity
    stop_loss_order.auxPrice = stop_loss_price
    stop_loss_order.tif = "GTC"  # Good Till Cancelled
    stop_loss_order.parentId = parent_order_id  # Link to the main order
    stop_loss_order.transmit = transmit  # Transmit both orders together

    return main_order, stop_loss_order


class PlaceOrderApp(EClient, EWrapper):
    def __init__(self):
        EClient.__init__(self, self)
        self.open_orders = []  # List to store open orders
        #self.orderId = self.nextId()  # Initialize order ID

    def nextValidId(self, orderId: OrderId):
        self.orderId = orderId

    def nextId(self):
        self.orderId += 1
        return self.orderId

    def error(self, reqId, errorCode, errorString, advancedOrderReject=""):
        print(
            f"reqId: {reqId}, errorCode: {errorCode}, errorString: {errorString}, orderReject: {advancedOrderReject}"
        )

    def openOrder(self, orderId, contract, order, orderState):
        """Callback for receiving open order details."""
        print(
            f"OrderId: {orderId}, Symbol: {contract.symbol}, Action: {order.action}, "
            f"Quantity: {order.totalQuantity}, Status: {orderState.status}"
        )
        self.open_orders.append(
            {
                "orderId": orderId,
                "symbol": contract.symbol,
                "action": order.action,
                "quantity": order.totalQuantity,
                "status": orderState.status,
            }
        )

    def openOrderEnd(self):
        """Callback indicating the end of open orders."""
        print("End of open orders.")

    def orderStatus(
        self,
        orderId,
        status,
        filled,
        remaining,
        avgFillPrice,
        permId,
        parentId,
        lastFillPrice,
        clientId,
        whyHeld,
        mktCapPrice,
    ):
        """Callback for receiving order status updates."""
        print(
            f"OrderId: {orderId}, Status: {status}, Filled: {filled}, Remaining: {remaining}, "
            f"AvgFillPrice: {avgFillPrice}"
        )


def place_US_stock_stop_limit_with_stop_loss(
    action,
    contract=contract,
    quantity=quantity,
    stop_price=stop_price,
    limit_price=limit_price,
    stop_loss_price=stop_loss_price,
    tif="DAY",
    transmit=False,
    port=7497,):
    """
    Place a buy stop limit order with a stop loss order using the IB API.
    Args:
        contract (Contract): The contract object for the stock.
        quantity (int): The number of shares to buy.
        stop_price (float): The stop price for the stop limit order.
        limit_price (float): The limit price for the stop limit order.
        stop_loss_price (float): The stop loss price.
        tif (str): Time in force for the orders (e.g., "DAY", "GTC").
        transmit (bool): Whether to transmit the orders immediately.
    """
    app = PlaceOrderApp()
    app.connect("127.0.0.1", port=port, clientId=0)

    # Start the API event loop in a separate thread
    thread = threading.Thread(target=app.run, daemon=True)
    thread.start()

    # Request open orders
    time.sleep(1)  # Wait for connection to establish

    app.reqIds(numIds=1)

    # Call the function, passing the app instance
    main_order, stop_loss_order = create_stock_stop_limit_with_stop_loss_order(
        action,
        app,
        contract,
        quantity,
        stop_price,
        limit_price,
        stop_loss_price,
        tif=tif,
        transmit=transmit,
    )

    # Place the main order
    app.placeOrder(main_order.orderId, contract, main_order)

    # Place the stop loss order
    app.placeOrder(stop_loss_order.orderId, contract, stop_loss_order)

    # Wait for the order to be placed
    time.sleep(2)  # Adjust this based on your order execution time
    app.reqAllOpenOrders()

    # Wait for open orders to be received
    time.sleep(2)  # Adjust this based on the number of open orders

    # Print all open orders
    print("All Open Orders:")
    for order in app.open_orders:
        print(order)

    # Disconnect
    app.disconnect()

    return()

from blankly import Alpaca, Strategy, StrategyState 
from blankly.indicators import rsi

def init(symbol, state:StrategyState):
    state.variables["history"] = state.interface.history(symbol, 150, resolution = state.resolution, return_as = "deque")["close"]
    state.variables['own_position'] = False

def price_event(price, symbol, state: StrategyState):
    state.variables["history"].append(price)
    rsi_output = rsi(state.variables["history"])

    if rsi_output[-1] < 10 and state.variables["own_position"] is False:
        qty = int(state.interface.cash / price)
        state.interface.market_order(symbol, 'buy', qty)
        state.variables['own_position'] = True

    elif rsi_output[-1] > 90 and state.variables["own_position"]:
        qty = int(state.interface.account[symbol].available)
        state.interface.market_order(symbol, 'sell', qty)
        state.variables['own_position'] = False


exchange = Alpaca()
s = Strategy(exchange)

s.add_price_event(price_event, "MSFT", "1h", init = init)
results = s.backtest('1y', {"USD": 10000})
print(results)
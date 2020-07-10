# This is the example code from the repo's README
import alpaca_backtrader_api
import backtrader as bt
import pandas as pd
from datetime import datetime

# Your credentials here
ALPACA_API_KEY = "PK95O39SG97BFP33X95R"
ALPACA_SECRET_KEY = "cDa/ti8eA63dyX1ojj9MWNDgmJ4xLTu/xO1nc502"
# change to True if you want to do live paper trading with Alpaca Broker.
#  False will do a back test
ALPACA_PAPER = False


class SmaCross(bt.SignalStrategy):
  def __init__(self):
    sma1, sma2 = bt.ind.SMA(period=10), bt.ind.SMA(period=30)
    crossover = bt.ind.CrossOver(sma1, sma2)
    self.signal_add(bt.SIGNAL_LONG, crossover)


if __name__ == '__main__':
    cerebro = bt.Cerebro()
    cerebro.addstrategy(SmaCross)

    store = alpaca_backtrader_api.AlpacaStore(
        key_id=ALPACA_API_KEY,
        secret_key=ALPACA_SECRET_KEY,
        paper=True
        #usePolygon=USE_POLYGON
    )

    DataFactory = store.getdata  # or use alpaca_backtrader_api.AlpacaData
    if ALPACA_PAPER:
        data0 = DataFactory(dataname='AAPL',
                            historical=False,
                            timeframe=bt.TimeFrame.Days)
        cerebro.adddata(data0)
        # or just alpaca_backtrader_api.AlpacaBroker()
        broker = store.getbroker()
        cerebro.setbroker(broker)
    else:
        DataFactory = store.getdata
        data0 = DataFactory(
            dataname='AAPL',
            timeframe=bt.TimeFrame.TFrame("Minutes"),
            fromdate=pd.Timestamp('2020-07-06'),
            todate=pd.Timestamp('2020-07-07'),
            historical=True)
        cerebro.adddata(data0)

    print('Starting Portfolio Value: {}'.format(cerebro.broker.getvalue()))
    cerebro.run()
    print('Final Portfolio Value: {}'.format(cerebro.broker.getvalue()))
    cerebro.plot()

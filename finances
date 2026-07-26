import random
import math
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass
from montecarloClass import MonteCarloModel
import yfinance as yf

# Finances from APPLE, MICROSOFT, TESLA
# No strategy, just holding for 30 days data from past 10 years
# Not good at all, high proportion of loss from monte carlo simulation
# Low probability using logNormal of increase in investment of $2000 or more (<10%)

# Both used and examples of uses 

ticker1 = yf.Ticker("AAPL")
ticker2 = yf.Ticker("MSFT")
ticker3 = yf.Ticker("TSLA")

hist1 = ticker1.history(period = "10y", auto_adjust = True)
hist2 = ticker2.history(period = "10y", auto_adjust = True)
hist3 = ticker3.history(period = "10y", auto_adjust = True)

hist1["Return"] = hist1["Close"].pct_change()
hist2["Return"] = hist2["Close"].pct_change()
hist3["Return"] = hist3["Close"].pct_change()

returns1 = hist1["Return"].dropna()
returns2 = hist2["Return"].dropna()
returns3 = hist3["Return"].dropna()

mean1 = statistics.mean(returns1)
mean2 = statistics.mean(returns2)
mean3 = statistics.mean(returns3)

stdev1 = statistics.stdev(returns1)
stdev2 = statistics.stdev(returns2)
stdev3 = statistics.stdev(returns3)

instance1 = MonteCarloModel(10000, stdev1, mean1, 150, 1, "AAPL")
instance2 = MonteCarloModel(10000, stdev2, mean2, 150, 1, "MSFT")
instance3 = MonteCarloModel(10000, stdev3, mean3, 150, 1, "TSLA")


print("")
instance1.monte_carlo(3000)
finals1 = instance1.finals
instance1.histogram(finals1, "Normal Simulation")
v1, er1, finals = instance1.bootstrapping(returns1, 5000)
instance1.bootStrapConf_Interval(v1, 0.05)
instance1.bootStrapConf_Interval(er1, 0.05)


print("")
instance2.monte_carlo(3000)
finals2 = instance2.finals
instance2.histogram(finals2, "Normal Simulation")
volatility, expectedReturn, finals = instance2.bootstrapping(returns2, 5000)
instance2.bootStrapConf_Interval(volatility, 0.05)
instance2.bootStrapConf_Interval(expectedReturn, 0.05)


print("")
instance3.monte_carlo(3000)
finals3 = instance3.finals
instance3.histogram(finals3, "Normal Simulation")
v3, er3, finals = instance3.bootstrapping(returns3, 5000)
instance2.bootStrapConf_Interval(v3, 0.05)
instance2.bootStrapConf_Interval(er3, 0.05)
instance3.histogram(instance3.logFinals, "Distribution of Log Final Investments: TSLA")

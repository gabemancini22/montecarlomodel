import random
import math
import matplotlib.pyplot as plt
import statistics
from dataclasses import dataclass
from scipy.stats import norm
import numpy as np

# This file has 2 classes, MonteCarloModel and BlackScholesModel
#
# MonteCarloModel: Runs a monte carlo simulation using a normal return distribution
# and using a bootstrapping method, also calculates some statistics for this simulation
#
# BlackScholesModel: Calculates a fair call and put price for options pricing,
# and calculates implied volatility


class MonteCarloModel:

    def __init__ (self, initial, volatility, expected, n, period, ticker):
        self.initial = initial
        self.volatility = volatility
        self.expected = expected
        self.n = n
        self.period = period
        self.ticker = ticker

        self.finals = []
        self.logFinals = []

    # Simulates a single investment growth
    def investment(self):

        # Commented to reduce console output, uncomment to see details for each period

        # Prints information for the initial period
        #print("Period 1: ")
        #print("Investment: " +str(initial))

        investments = [self.initial]
        returns = []

        final = self.initial
        for i in range(1, self.n):

            difference = final
            a = random.gauss(self.expected, (self.volatility)*math.sqrt(self.period))
            
            final = final*(1 + a)
            difference = difference - final
            # Commented to reduce console output, uncomment to see details for each period

            # Prints information for each period
            #print("Period " +str(i+1)+ ": ")
            #print("Investment: " +str(int(final)))
            #print("Return: " + str(int(a*100)) + "%")
            #print("Difference: " +str(int(difference)))
            #print("")

            investments.append(final)
            returns.append(a)
            
        return investments, final, returns
    

    # Monte Carlo Simulation for Investment Growth, giving some other statistics as well
    def monte_carlo(self, iterations):
        for i in range(iterations):
            invest, f, r = self.investment()
            plt.plot(invest)
            self.finals.append(f)

            self.logFinals.append(self.log_normal(r))

        print(str(self.ticker))
        print("Average Final Investment: " + str(int(statistics.mean(self.finals))))
        print("Standard Deviation of Final Investment: " + str(int(statistics.stdev(self.finals))))

        prop = self.proportion_loss(10000)
        print("Proportion of losses (Normal Model): " +str(prop))
        plt.xlabel('Period')
        plt.ylabel('Investment Value')
        plt.title(f'Investment Growth Over Time: {self.ticker} - Normal Distribution')
        plt.show()

        self.VaR_and_CVaR(0.01)
        return self.logFinals

    #Calculates the proportion of losses in the monte carlo simulation
    def proportion_loss(self, ceiling):
        if not self.finals:
            return 0

        count = 0
        for val in self.finals:
            if val < ceiling:
                count += 1

        return count / len(self.finals)
    
    @staticmethod
    def proportion_loss_STATIC(results, ceiling):
        if not results:
            return 0

        count = 0
        for val in results:
            if val < ceiling:
                count += 1

        return count / len(results)

    # Calculates the natural log of a final investment, used in MonteCarlo to create
    # A list of log finals that can be used for a histogram
    def log_normal(self, returns):
        logFinal = math.log(self.initial)

        for r in returns:
            logFinal += math.log(1 + r)

        return logFinal

    # Calculates probability of investment being between two values using logNormal distribution
    def probability(self, lower, upper):
        if not self.logFinals:
            print(f"No data to compute probability between {lower} and {upper}.")
            return 0.0

        if upper <= 0:
            print(f"Probability is 0.0 because upper bound {upper} is not positive.")
            return 0.0

        mean = statistics.mean(self.logFinals)
        stdev = statistics.stdev(self.logFinals)
        logLower = float("-inf") if lower <= 0 else math.log(lower)
        logUpper = math.log(upper)

        probability = norm.cdf(logUpper, loc=mean, scale=stdev) - norm.cdf(logLower, loc=mean, scale=stdev)

        print(f"The probability final investment being between {lower} and {upper} is {probability}.")

        return probability
    
    def histogram(self, values, title):
        plt.hist(values, bins = 20, edgecolor = 'black')
        plt.xlabel(f"Investment Value: {self.ticker} -" + title)
        plt.ylabel("Frequency")
        plt.show()

    #Bootstrap confidence interval calculates a confidence interval
    # At a certain alpha by sorting values in a list and keeping 1-alpha% of the data within
    # The lower and upper bound, which are the confidence interval bounds.
    @staticmethod
    def bootStrapConf_Interval(values, alpha):
        orderedVals = values.copy()
        orderedVals.sort()

        sides = (1-alpha)/2
        lowerIndex = int(len(orderedVals)*(sides))
        upperIndex = int(len(orderedVals)*(1-sides))

        lower = orderedVals[lowerIndex]
        upper = orderedVals[upperIndex]
        print("")
        print(f"There is {100-(alpha*100)}% Confidence that the true mean of the statstic is between {lower} and {upper} ")
        
    def bootstrapping(self, returns, trials):
        randomizedReturns = []
        volatilities = []
        exp_returns = []
        finals = []

        for i in range(trials):
            for j in range(self.n):
                randomizedReturns.append(random.choice(returns))

            vN = statistics.stdev(randomizedReturns)
            erN = statistics.mean(randomizedReturns)
            volatilities.append(vN)
            exp_returns.append(erN)

            final = self.initial
            investment = [final]
            for k in range(self.n):
                final = final*(1 + randomizedReturns[k])
                investment.append(final)
            finals.append(final)

            plt.plot(investment)
            randomizedReturns = []

        prop = self.proportion_loss_STATIC(finals, 10000)
        print("Proportion of losses (Bootstrapping): " +str(prop))
        plt.xlabel('Period')
        plt.ylabel('Investment Value')
        plt.title(f'Investment Growth Over Time: {self.ticker} - Bootstrapping')
        plt.show()

        self.histogram(finals, "Bootstrapping")
        self.VaR_and_CVaR_Bootstrap(finals, 0.01)

        return volatilities, exp_returns, finals
    
    # Calculated the Value at Risk and Conditional Value at Risk for the Normal Distribution model at a certain alpha
    # Value at Risk, confidence interval at 1-alpha%, meaning that the 1-alpha% of the time
    # The loss will not go under the Value at Risk
    def VaR_and_CVaR(self, alpha):
        loss = [final - self.initial for final in self.finals]
        sortedLoss = loss.copy()
        sortedLoss.sort()

        length = len(sortedLoss)
        value = int(length*alpha)
        VaR = sortedLoss[value]

        lossInt = []
        CVaR = 0
        for i in range(0, value):
            CVaR += sortedLoss[i]
        CVaR /= value

        print("")
        print(f"Value at Risk for Normal Simulation: {-VaR}")
        print("")
        print(f"Conditional Value At Risk for Normal Simulation: {-CVaR}")
        
        return VaR, CVaR
    
    @staticmethod
    def VaR_and_CVaR_Bootstrap(finals, alpha):
        loss = [final - 10000 for final in finals]
        sortedLoss = loss.copy()
        sortedLoss.sort()

        length = len(sortedLoss)
        value = int(length*alpha)
        VaR = sortedLoss[value]

        lossInt = []
        CVaR = 0
        for i in range(0, value):
            CVaR += sortedLoss[i]
        CVaR = CVaR/value

        print("")
        print(f"Value at Risk for Bootstrap Simulation: {-VaR}")
        print("")
        print(f"Conditional Value At Risk for Bootstrap Simulation: {-CVaR}")

        return VaR, CVaR



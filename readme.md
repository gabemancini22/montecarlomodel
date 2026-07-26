MONTECARLOMODEL

Thank you for looking at my code! I understand this is a very simple model and free for anyone to use to calculate any statistics they would like, but please do not take this work and pass it off as your own. Also please recognize that to my best knowledge everything is correct and has been checked multiple times, but please understand that there could be some mistakes.
For more information on the mathematics and analysis behind the project, please see the report Monte_Carlo_Simulations.pdf

Monte Carlo Model is a python class and some execution written to perform a Monte Carlo Simulation of investments
using a historical bootstrapping and normal distribution model. The Monte Carlo Simulation performs a specified number of investments randomly with either 2 of the methods, a period of time, and a certain ticker. Using the class MonteCarloModel, these simulations can be run and histograms, line plots, and some statistics can be calculated. The purpose of this project is to calculate and display some financial data using real financial returns taken from Yahoo Finance. Any financial data from yahoo finance can be used, as examples, Tesla, Apple, and Microsoft were used and some statistics were calculated.

On finances.py, both the historical bootstrapping and normal distribution model were used. Histograms for log final investments and final investments were created, along with calculating the confidece intervals of standard deviation and mean of the final investments using the bootstrapping confidence interval method.

The method monte_carlo calculates more than just the monte carlo simulation. It displays the line plot of investments, and calculated the Value at Risk, Conditional Value at Risk of the simulation, and the Proportion of Loss.

There are both static and non static methods for a lot of the calculations. This is because the historical bootstrapping method takes a different approach from the Normal Distribution method and must be static. the method bootstrapping calculates the value at risk, Condition Value at Risk, proportion of loss, and plots line plots of investments and histograms for the final investments.

Examples of how to use the code are on finances.py, please refer to that to understand how to use the program.
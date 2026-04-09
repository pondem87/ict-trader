# ICT Trading Bot

This trading bot, build on Python, builds upon ICT market structure principles and implements a variety of trading strategies based on identifying the various ICT market structures.

One of the reasons for picking Python was access to the large machine learning resources which will be incorporated into the trading strategies.

A core component of design is to build the trading and backtesting engines independent of the UI application and the broker. Here I will implement core trading and backtesting logic and provide interfaces that will allow UI and broker choices to be made at a later time.
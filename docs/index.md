# Gaussian Ornstein-Uhlenbeck Process

Welcome to the documentation for the Gaussian Ornstein-Uhlenbeck (OU) process simulation. This project focuses on modeling mean-reverting stochastic processes.

## Mathematical Formulation

The Ornstein-Uhlenbeck process is defined by the following stochastic differential equation (SDE):

$$dx_t = \theta (\mu - x_t) dt + \sigma dW_t$$

Where:
* $\theta$ is the rate of mean reversion.
* $\mu$ is the long-term mean.
* $\sigma$ is the volatility parameter.
* $dW_t$ is a Wiener process (Brownian motion).

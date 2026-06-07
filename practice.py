# OU process simulation

import numpy as np
import matplotlib.pyplot as plt

# Parameters for the OU process
theta = 0.7      # Speed of mean reversion
mu = 0.0         # Long-term mean
sigma = 0.3      # Volatility
X0 = 1.0         # Initial value
T = 30.0         # Total time
dt = 0.01        # Time step
N = int(T / dt)  # Number of time steps

# Pre-allocate array for efficiency
X = np.zeros(N)
X[0] = X0

# Generate the OU process
for t in range(1, N):
    dW = np.sqrt(dt) * np.random.normal(0, 1)
    X[t] = X[t-1] + theta * (mu - X[t-1]) * dt + sigma * dW

# Plot the result
plt.plot(np.linspace(0, T, N), X)
plt.title("Ornstein-Uhlenbeck Process Simulation")
plt.xlabel("Time")
plt.ylabel("X(t)")
plt.show()


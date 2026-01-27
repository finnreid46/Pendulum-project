from __future__ import annotations
from dataclasses import dataclass
import numpy as np

@dataclass(frozen=True)
class Params:
    g: float = 9.81      # m/s^2
    L: float = 1.0       # m
    theta0: float = 0.6  # rad
    omega0: float = 0.0  # rad/s
    t_max: float = 10.0  # s
    dt: float = 0.01     # s
    gamma: float = 0.0   # 1/s damping coefficient (using 2*gamma convention)
    A: float = 0.0       # rad/s^2 driving amplitude
    wd: float = 2.0      # rad/s driving angular frequency


def derivs(t: float, y: np.ndarray, p: Params) -> np.ndarray:
    theta, omega = y
    dtheta = omega

    # Damped, driven nonlinear pendulum
    domega = (
        -(p.g / p.L) * np.sin(theta)
        - 2.0 * p.gamma * omega
        + p.A * np.cos(p.wd * t)
    )

    return np.array([dtheta, domega], dtype=float)


def rk4_step(t: float, y: np.ndarray, dt: float, p: Params) -> np.ndarray:
    k1 = derivs(t, y, p)
    k2 = derivs(t + 0.5*dt, y + 0.5*dt*k1, p)
    k3 = derivs(t + 0.5*dt, y + 0.5*dt*k2, p)
    k4 = derivs(t + dt, y + dt*k3, p)
    return y + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

def energy(theta: np.ndarray, omega: np.ndarray, p: Params) -> np.ndarray:
    # energy per unit mass (m cancels): E = 1/2 (L^2 omega^2) + gL(1 - cos theta)
    return 0.5*(p.L**2)*(omega**2) + p.g*p.L*(1.0 - np.cos(theta))

def simulate(p: Params):
    n = int(np.floor(p.t_max / p.dt)) + 1
    t = np.linspace(0.0, p.t_max, n)

    y = np.zeros((n, 2), dtype=float)
    y[0, 0] = p.theta0
    y[0, 1] = p.omega0

    for i in range(n - 1):
        y[i+1] = rk4_step(t[i], y[i], p.dt, p)

    theta = y[:, 0]
    omega = y[:, 1]
    E = energy(theta, omega, p)
    return t, theta, omega, E

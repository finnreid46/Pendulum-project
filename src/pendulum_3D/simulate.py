import numpy as np
from .equations import Params3D, derivs_spherical, xyz_from_angles


def rk4_step_3d(t: float, y: np.ndarray, dt: float, p: Params3D) -> np.ndarray:
    k1 = derivs_spherical(t, y, p)
    k2 = derivs_spherical(t + 0.5 * dt, y + 0.5 * dt * k1, p)
    k3 = derivs_spherical(t + 0.5 * dt, y + 0.5 * dt * k2, p)
    k4 = derivs_spherical(t + dt, y + dt * k3, p)
    return y + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)


def simulate_3d(p: Params3D):
    n = int(np.floor(p.t_max / p.dt)) + 1
    t = np.linspace(0.0, p.t_max, n)

    y = np.zeros((n, 4), dtype=float)
    y[0] = np.array([p.theta0, p.phi0, p.theta_dot0, p.phi_dot0], dtype=float)

    for i in range(n - 1):
        y[i + 1] = rk4_step_3d(t[i], y[i], p.dt, p)

    theta = y[:, 0]
    phi = y[:, 1]
    theta_dot = y[:, 2]
    phi_dot = y[:, 3]

    x, y_, z = xyz_from_angles(theta, phi, p.L)
    return t, theta, phi, theta_dot, phi_dot, x, y_, z

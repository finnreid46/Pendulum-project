from __future__ import annotations
from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class Params3D:
    g: float = 9.81
    L: float = 1.0

    # Damping + driving (2*gamma convention)
    gamma: float = 0.0      # 1/s damping coefficient
    A: float = 0.0          # rad/s^2 driving amplitude
    wd: float = 2.0         # rad/s driving angular frequency

    # Initial conditions
    theta0: float = 0.6         # rad (angle from vertical)
    phi0: float = 0.0           # rad (azimuth)
    theta_dot0: float = 0.0     # rad/s
    phi_dot0: float = 2.0       # rad/s

    # Time settings
    t_max: float = 10.0         # s
    dt: float = 0.01            # s


def derivs_spherical(t: float, y: np.ndarray, p: Params3D) -> np.ndarray:
    """
    Spherical pendulum (general model), with optional damping + driving.
    State vector:
        y = [theta, phi, theta_dot, phi_dot]
    """
    theta, phi, theta_dot, phi_dot = y

    dtheta = theta_dot
    dphi = phi_dot

    # Avoid singularity at theta=0 where cot(theta) blows up
    eps = 1e-8
    sin_th = np.sin(theta)
    cos_th = np.cos(theta)

    # theta_ddot = sinθ cosθ (phi_dot)^2 - (g/L) sinθ  - 2γ θdot + A cos(wd t)
    dtheta_dot = (sin_th * cos_th) * (phi_dot**2) - (p.g / p.L) * sin_th
    dtheta_dot += -2.0 * p.gamma * theta_dot + p.A * np.cos(p.wd * t)

    # phi_ddot = -2 cotθ θdot φdot  - 2γ φdot
    denom = sin_th if abs(sin_th) > eps else (eps if sin_th >= 0 else -eps)
    cot_th = cos_th / denom
    dphi_dot = -2.0 * cot_th * theta_dot * phi_dot
    dphi_dot += -2.0 * p.gamma * phi_dot

    return np.array([dtheta, dphi, dtheta_dot, dphi_dot], dtype=float)


def xyz_from_angles(theta: np.ndarray, phi: np.ndarray, L: float):
    x = L * np.sin(theta) * np.cos(phi)
    y = L * np.sin(theta) * np.sin(phi)
    z = -L * np.cos(theta)
    return x, y, z


def energy_spherical(theta: np.ndarray,
                     theta_dot: np.ndarray,
                     phi_dot: np.ndarray,
                     p: Params3D) -> np.ndarray:
    """
    Total mechanical energy per unit mass (E/m).
    Note: if gamma or A is nonzero, E will not be conserved (physically expected).
    """
    T = 0.5 * (p.L**2) * (theta_dot**2 + (np.sin(theta)**2) * (phi_dot**2))
    V = p.g * p.L * (1.0 - np.cos(theta))
    return T + V

# import matplotlib.pyplot as plt
# from .equations import Params3D, energy_spherical
# from .simulate import simulate_3d

# def main():
#     p = Params3D(
#         theta0=0.8,
#         phi0=0.0,
#         theta_dot0=0.25,
#         phi_dot0=1.7,
#         t_max=20.0,
#         dt=0.01
#     )

#     t, theta, phi, theta_dot, phi_dot, x, y_, z = simulate_3d(p)

#     # --- Energy per unit mass ---
#     E = energy_spherical(theta, theta_dot, phi_dot, p)
#     rel_drift = (E - E[0]) / E[0]

#     # Plot top-down trajectory
#     plt.figure()
#     plt.plot(x, y_)
#     plt.xlabel("x (m)")
#     plt.ylabel("y (m)")
#     plt.axis("equal")
#     plt.title("Top-down trajectory")

#     # Plot relative energy drift
#     plt.figure()
#     plt.plot(t, rel_drift)
#     plt.xlabel("t (s)")
#     plt.ylabel("(E - E0) / E0")
#     plt.title("Relative energy drift")

#     plt.show()

# if __name__ == "__main__":
#     main()


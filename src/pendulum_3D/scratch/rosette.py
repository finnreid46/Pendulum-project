# import numpy as np
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 (needed for 3D)

# from .equations import Params3D
# from .simulate import simulate_3d


# def main():
#     # --- parameters (edit for rosette) ---
#     p0 = Params3D(
#         theta0=0.8,
#         phi0=0.0,
#         theta_dot0=0.25,
#         phi_dot0=1.7,
#         t_max=20.0,
#         dt=0.01,
#     )

#     # --- simulate ---
#     t, theta, phi, theta_dot, phi_dot, x, y_, z = simulate_3d(p0)

#     L = p0.L

#     # --- figure + 3D axis ---
#     fig = plt.figure(figsize=(10, 6))
#     ax = fig.add_subplot(111, projection="3d")
#     ax.set_title("3D Spherical Pendulum")

#     # Set equal-ish limits
#     lim = 1.1 * L
#     ax.set_xlim(-lim, lim)
#     ax.set_ylim(-lim, lim)
#     ax.set_zlim(-lim, lim)

#     ax.set_xlabel("x (m)")
#     ax.set_ylabel("y (m)")
#     ax.set_zlabel("z (m)")

#     # --- artists: rod + bob ---
#     (rod_line,) = ax.plot([0, x[0]], [0, y_[0]], [0, z[0]], lw=2)
#     (bob_point,) = ax.plot([x[0]], [y_[0]], [z[0]], marker="o", markersize=8)

#     # --- trail (3D) ---
#     trail_len = 300  # number of recent points to show
#     (trail_line,) = ax.plot([x[0]], [y_[0]], [z[0]], lw=1)

#     # --- shadow projection on xy-plane ---
#     # Project onto z = z_floor
#     z_floor = -L
#     (shadow_line,) = ax.plot([x[0]], [y_[0]], [z_floor], lw=1)
#     (shadow_point,) = ax.plot([x[0]], [y_[0]], [z_floor], marker="o", markersize=4)

#     #  draw the floor circle 
#     ang = np.linspace(0, 2 * np.pi, 200)
#     floor_r = L
#     ax.plot(floor_r * np.cos(ang), floor_r * np.sin(ang), z_floor, lw=1)

#     # --- animation state ---
#     state = {"i": 0}

#     def animate(_frame):
#         i = state["i"]
#         state["i"] = (i + 1) % len(t)

#         # rod + bob
#         rod_line.set_data([0, x[i]], [0, y_[i]])
#         rod_line.set_3d_properties([0, z[i]])

#         bob_point.set_data([x[i]], [y_[i]])
#         bob_point.set_3d_properties([z[i]])

#         # trail
#         i0 = max(0, i - trail_len)
#         trail_line.set_data(x[i0:i], y_[i0:i])
#         trail_line.set_3d_properties(z[i0:i])

#         # shadow
#         shadow_line.set_data(x[i0:i], y_[i0:i])
#         shadow_line.set_3d_properties(np.full(i - i0, z_floor))

#         shadow_point.set_data([x[i]], [y_[i]])
#         shadow_point.set_3d_properties([z_floor])

#         return rod_line, bob_point, trail_line, shadow_line, shadow_point

#     ani = FuncAnimation(fig, animate, interval=20, blit=True)
#     plt.show()


# if __name__ == "__main__":
#     main()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import TextBox, Button
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

from .equations import Params3D
from .simulate import simulate_3d


def main():
    # ---- initial params ----
    p0 = Params3D(
        g=9.81,
        L=1.0,
        theta0=0.8,
        phi0=0.0,
        theta_dot0=0.25,
        phi_dot0=1.7,
        gamma=0.0,
        A=0.0,
        wd=2.0,
        t_max=20.0,
        dt=0.01,
    )

    # ---- simulate ----
    t, theta, phi, theta_dot, phi_dot, x, y_, z = simulate_3d(p0)

    # ---- figure layout ----
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection="3d")
    ax.set_title("3D Spherical Pendulum (Forced/Damped)")

    # inputs - left
    plt.subplots_adjust(left=0.32)

    # ---- axis limits ----
    def set_limits(L):
        lim = 1.1 * L
        ax.set_xlim(-lim, lim)
        ax.set_ylim(-lim, lim)
        ax.set_zlim(-lim, lim)
        ax.set_xlabel("x (m)")
        ax.set_ylabel("y (m)")
        ax.set_zlabel("z (m)")

    set_limits(p0.L)

    # ---- artists ----
    (rod_line,) = ax.plot([0, x[0]], [0, y_[0]], [0, z[0]], lw=2)
    (bob_point,) = ax.plot([x[0]], [y_[0]], [z[0]], marker="o", markersize=8)

    trail_len = 300
    (trail_line,) = ax.plot([x[0]], [y_[0]], [z[0]], lw=1)

    z_floor = -p0.L
    (shadow_line,) = ax.plot([x[0]], [y_[0]], [z_floor], lw=1)
    (shadow_point,) = ax.plot([x[0]], [y_[0]], [z_floor], marker="o", markersize=4)

    ang = np.linspace(0, 2 * np.pi, 200)
    floor_circle, = ax.plot(p0.L * np.cos(ang), p0.L * np.sin(ang), z_floor, lw=1)

    # ---- shared state ----
    state = {
        "p": p0,
        "t": t,
        "x": x,
        "y_": y_,
        "z": z,
        "i": 0,
    }

    # ---- animation ----
    def animate(_frame):
        i = state["i"]
        t_arr = state["t"]
        x_arr = state["x"]
        y_arr = state["y_"]
        z_arr = state["z"]

        state["i"] = (i + 1) % len(t_arr)

        rod_line.set_data([0, x_arr[i]], [0, y_arr[i]])
        rod_line.set_3d_properties([0, z_arr[i]])

        bob_point.set_data([x_arr[i]], [y_arr[i]])
        bob_point.set_3d_properties([z_arr[i]])

        i0 = max(0, i - trail_len)
        trail_line.set_data(x_arr[i0:i], y_arr[i0:i])
        trail_line.set_3d_properties(z_arr[i0:i])

        z_floor_local = -state["p"].L
        shadow_line.set_data(x_arr[i0:i], y_arr[i0:i])
        shadow_line.set_3d_properties(np.full(i - i0, z_floor_local))

        shadow_point.set_data([x_arr[i]], [y_arr[i]])
        shadow_point.set_3d_properties([z_floor_local])

        return rod_line, bob_point, trail_line, shadow_line, shadow_point

    ani = FuncAnimation(fig, animate, interval=20, blit=False)

    # ---- "table" inputs (TextBoxes) ----
    # helper to place rows
    def add_row(y, label, initial):
        fig.text(0.02, y, label, fontsize=10, va="center")
        axbox = plt.axes([0.12, y - 0.015, 0.16, 0.03])
        tb = TextBox(axbox, "", initial=initial)
        return tb

    # rows (top to bottom)
    y0 = 0.92
    dy = 0.045

    tb_g       = add_row(y0 - 0*dy, "g",       str(p0.g))
    tb_L       = add_row(y0 - 1*dy, "L",       str(p0.L))
    tb_gamma   = add_row(y0 - 2*dy, "gamma",   str(p0.gamma))
    tb_A       = add_row(y0 - 3*dy, "A",       str(p0.A))
    tb_wd      = add_row(y0 - 4*dy, "wd",      str(p0.wd))

    tb_theta0  = add_row(y0 - 5*dy, "theta0",  str(p0.theta0))
    tb_phi0    = add_row(y0 - 6*dy, "phi0",    str(p0.phi0))
    tb_thdot0  = add_row(y0 - 7*dy, "theta_dot0", str(p0.theta_dot0))
    tb_phdot0  = add_row(y0 - 8*dy, "phi_dot0",   str(p0.phi_dot0))

    tb_tmax    = add_row(y0 - 9*dy, "t_max",   str(p0.t_max))
    tb_dt      = add_row(y0 -10*dy, "dt",      str(p0.dt))

    # Apply button
    ax_apply = plt.axes([0.12, 0.02, 0.16, 0.04])
    btn_apply = Button(ax_apply, "Apply")

    def safe_float(tb, name):
        try:
            return float(tb.text)
        except ValueError:
            raise ValueError(f"Invalid {name}: '{tb.text}'")

    def on_apply(_event):
        nonlocal floor_circle

        try:
            p = Params3D(
                g=safe_float(tb_g, "g"),
                L=safe_float(tb_L, "L"),
                gamma=safe_float(tb_gamma, "gamma"),
                A=safe_float(tb_A, "A"),
                wd=safe_float(tb_wd, "wd"),
                theta0=safe_float(tb_theta0, "theta0"),
                phi0=safe_float(tb_phi0, "phi0"),
                theta_dot0=safe_float(tb_thdot0, "theta_dot0"),
                phi_dot0=safe_float(tb_phdot0, "phi_dot0"),
                t_max=safe_float(tb_tmax, "t_max"),
                dt=safe_float(tb_dt, "dt"),
            )
        except ValueError as e:
            print(e)
            return

        # re-simulate
        t, theta, phi, theta_dot, phi_dot, x, y_, z = simulate_3d(p)

        # update state
        state.update({"p": p, "t": t, "x": x, "y_": y_, "z": z, "i": 0})

        # update axes limits + floor circle
        set_limits(p.L)

        z_floor_local = -p.L
        floor_circle.remove()
        floor_circle, = ax.plot(p.L * np.cos(ang), p.L * np.sin(ang), z_floor_local, lw=1)

        fig.canvas.draw_idle()

    btn_apply.on_clicked(on_apply)

    plt.show()


if __name__ == "__main__":
    main()


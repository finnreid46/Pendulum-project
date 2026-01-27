
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation

from src.core import Params, simulate


def main():
    p0 = Params()

    # --- figure layout: left = time series, right = animation ---
    fig = plt.figure(figsize=(10, 6))
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 1], width_ratios=[1.3, 1.0])
    ax_theta = fig.add_subplot(gs[0, 0])
    ax_E = fig.add_subplot(gs[1, 0])
    ax_anim = fig.add_subplot(gs[:, 1])

    plt.subplots_adjust(bottom=0.34)

    # --- initial simulation ---
    t, theta, omega, E = simulate(p0)

    # time-series lines
    (line_theta,) = ax_theta.plot(t, theta)
    ax_theta.set_ylabel("theta (rad)")
    ax_theta.set_title("Damped / Driven Pendulum (RK4)")

    (line_E,) = ax_E.plot(t, E)
    ax_E.set_ylabel("Energy (per unit mass)")
    ax_E.set_xlabel("time (s)")

    # --- animation artists (rod + bob) ---
    L = p0.L
    x = L * np.sin(theta)
    y = -L * np.cos(theta)

    (rod_line,) = ax_anim.plot([0, x[0]], [0, y[0]], lw=2)
    (bob_point,) = ax_anim.plot([x[0]], [y[0]], marker="o", markersize=10)

    ax_anim.set_aspect("equal", adjustable="box")
    ax_anim.set_xlim(-1.2 * L, 1.2 * L)
    ax_anim.set_ylim(-1.2 * L, 0.2 * L)
    ax_anim.set_xlabel("x")
    ax_anim.set_ylabel("y")
    ax_anim.set_title("2D Animation")

    # --- sliders (same idea as your existing UI) ---
    ax_L = plt.axes([0.12, 0.25, 0.76, 0.03])
    ax_th0 = plt.axes([0.12, 0.20, 0.76, 0.03])
    ax_dt = plt.axes([0.12, 0.15, 0.76, 0.03])
    ax_gamma = plt.axes([0.12, 0.10, 0.76, 0.03])
    ax_A = plt.axes([0.12, 0.05, 0.76, 0.03])
    ax_wd = plt.axes([0.12, 0.00, 0.76, 0.03])

    sL = Slider(ax_L, "L (m)", 0.2, 5.0, valinit=p0.L, valstep=0.05)
    sth0 = Slider(ax_th0, "theta0 (rad)", 0.0, 3.0, valinit=p0.theta0, valstep=0.01)
    sdt = Slider(ax_dt, "dt (s)", 0.001, 0.05, valinit=p0.dt, valstep=0.001)
    sgamma = Slider(ax_gamma, "gamma (1/s)", 0.0, 2.0, valinit=p0.gamma, valstep=0.01)
    sA = Slider(ax_A, "A (rad/s^2)", 0.0, 10.0, valinit=p0.A, valstep=0.05)
    swd = Slider(ax_wd, "wd (rad/s)", 0.1, 10.0, valinit=p0.wd, valstep=0.05)

    # --- shared state used by animation + plots ---
    state = {
        "t": t,
        "theta": theta,
        "E": E,
        "x": x,
        "y": y,
        "i": 0,
        "L": p0.L,
    }

    def resimulate_from_sliders():
        p = Params(
            g=p0.g,
            omega0=p0.omega0,
            t_max=p0.t_max,
            L=float(sL.val),
            theta0=float(sth0.val),
            dt=float(sdt.val),
            gamma=float(sgamma.val),
            A=float(sA.val),
            wd=float(swd.val),
        )

        t, theta, omega, E = simulate(p)

        L = p.L
        x = L * np.sin(theta)
        y = -L * np.cos(theta)

        state.update({"t": t, "theta": theta, "E": E, "x": x, "y": y, "i": 0, "L": L})

        # update time-series
        line_theta.set_data(t, theta)
        line_E.set_data(t, E)

        ax_theta.set_xlim(t[0], t[-1])
        ax_E.set_xlim(t[0], t[-1])

        ax_theta.relim()
        ax_theta.autoscale_view(scalex=False, scaley=True)

        ax_E.relim()
        ax_E.autoscale_view(scalex=False, scaley=True)

        # update animation axis limits for new L
        ax_anim.set_xlim(-1.2 * L, 1.2 * L)
        ax_anim.set_ylim(-1.2 * L, 0.2 * L)

        fig.canvas.draw_idle()

    def on_slider(_):
        resimulate_from_sliders()

    for s in (sL, sth0, sdt, sgamma, sA, swd):
        s.on_changed(on_slider)

    # --- animation update ---
    def animate(_frame):
        x = state["x"]
        y = state["y"]
        n = len(x)

        i = state["i"] % n
        state["i"] = i + 1

        rod_line.set_data([0, x[i]], [0, y[i]])
        bob_point.set_data([x[i]], [y[i]])
        return rod_line, bob_point

    ani = FuncAnimation(fig, animate, interval=20, blit=True)

    plt.show()


if __name__ == "__main__":
    main()

print("ui_matplotlib.py started")

import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

from src.core import Params, simulate


def make_plot(p: Params):
    return simulate(p)


def main():
    p0 = Params()

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
    plt.subplots_adjust(bottom=0.42)

    t, theta, omega, E = make_plot(p0)

    (line_theta,) = ax1.plot(t, theta)
    ax1.set_ylabel("theta (rad)")
    ax1.set_title("Simple Pendulum (RK4)")

    (line_E,) = ax2.plot(t, E)
    ax2.set_ylabel("Energy (per unit mass)")
    ax2.set_xlabel("time (s)")

    # Sliders area
    ax_L     = plt.axes([0.15, 0.29, 0.7, 0.03])
    ax_th0   = plt.axes([0.15, 0.24, 0.7, 0.03])
    ax_dt    = plt.axes([0.15, 0.19, 0.7, 0.03])
    ax_gamma = plt.axes([0.15, 0.14, 0.7, 0.03])
    ax_A     = plt.axes([0.15, 0.09, 0.7, 0.03])
    ax_wd    = plt.axes([0.15, 0.04, 0.7, 0.03])



    sL = Slider(ax_L, "L (m)", 0.2, 5.0, valinit=p0.L, valstep=0.05)
    sth0 = Slider(ax_th0, "theta0 (rad)", 0.0, 3.0, valinit=p0.theta0, valstep=0.01)
    sdt = Slider(ax_dt, "dt (s)", 0.001, 0.05, valinit=p0.dt, valstep=0.001)
    sgamma = Slider(ax_gamma, "gamma (1/s)", 0.0, 2.0, valinit=p0.gamma, valstep=0.01)
    sA     = Slider(ax_A,     "A (rad/s^2)", 0.0, 10.0, valinit=p0.A, valstep=0.05)
    swd    = Slider(ax_wd,    "wd (rad/s)",  0.1, 10.0, valinit=p0.wd, valstep=0.05)


    def update(_):
        p = Params(
            L=float(sL.val),
            theta0=float(sth0.val),
            dt=float(sdt.val),
            gamma=float(sgamma.val),
            A=float(sA.val),
            wd=float(swd.val),
            t_max=p0.t_max,
            g=p0.g,
            omega0=p0.omega0,
        )

        t, theta, omega, E = make_plot(p)

        line_theta.set_data(t, theta)
        line_E.set_data(t, E)

        # keep x-range consistent with new t length
        ax1.set_xlim(t[0], t[-1])
        ax2.set_xlim(t[0], t[-1])

        ax1.relim()
        ax1.autoscale_view(scalex=False, scaley=True)

        ax2.relim()
        ax2.autoscale_view(scalex=False, scaley=True)

        fig.canvas.draw_idle()


    sL.on_changed(update)
    sth0.on_changed(update)
    sdt.on_changed(update)
    sgamma.on_changed(update)
    sA.on_changed(update)
    swd.on_changed(update)


    plt.show()


if __name__ == "__main__":
    main()
print("ui_matplotlib.py imports done")
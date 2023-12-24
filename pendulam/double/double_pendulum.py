from numpy import sin, cos
from scipy.integrate import solve_ivp
from matplotlib.animation import FuncAnimation
import numpy as np
import matplotlib.pyplot as plt


G = 9.8     # 重力加速度 [m/s^2]
L1 = 1.0    # 単振り子1の長さ [m]
L2 = 1.0    # 単振り子2の長さ [m]
M1 = 1.0    # おもり1の質量 [kg]
M2 = 1.0    # おもり2の質量 [kg]

# 運動方程式
def derivs(t, state):
    dydx = np.zeros_like(state)
    dydx[0] = state[1]

    delta = state[2] - state[0]
    den1 = (M1+M2) * L1 - M2 * L1 * cos(delta) * cos(delta)
    dydx[1] = ((M2 * L1 * state[1] * state[1] * sin(delta) * cos(delta)
                + M2 * G * sin(state[2]) * cos(delta)
                + M2 * L2 * state[3] * state[3] * sin(delta)
                - (M1+M2) * G * sin(state[0]))
               / den1)

    dydx[2] = state[3]

    den2 = (L2/L1) * den1
    dydx[3] = ((- M2 * L2 * state[3] * state[3] * sin(delta) * cos(delta)
                + (M1+M2) * G * sin(state[0]) * cos(delta)
                - (M1+M2) * L1 * state[1] * state[1] * sin(delta)
                - (M1+M2) * G * sin(state[2]))
               / den2)

    return dydx

# 時間生成
t_span = [0,20]
dt = 0.05
t = np.arange(t_span[0], t_span[1], dt)

# 初期条件
th1 = 90.0
w1 = 0.0
th2 = 90.0
w2 = 0.0
state = np.radians([th1, w1, th2, w2])

# 運動方程式を解く
sol = solve_ivp(derivs, t_span, state, t_eval=t)
y = sol.y

x1 = L1 * sin(y[0,:])
y1 = -L1 * cos(y[0,:])
x2 = L2 * sin(y[2,:]) + x1
y2 = -L2 * cos(y[2,:]) + y1

fig, ax = plt.subplots()
line, = ax.plot([], [], "o-", linewidth=2)
time_template = 'time = %.1fs'
time_text = ax.text(0.05, 0.9, '', transform=ax.transAxes)

def animate(i):
    tt = t[i]
    thisx1 = [0, x1[i]]
    thisy1 = [0, y1[i]]
    thisx2 = [thisx1, x2[i]]
    thisy2 = [thisy1, y2[i]]
    line.set_data([0, thisx1[1], thisx2[1]], [0, thisy1[1], thisy2[1]])
    time_text.set_text(time_template % (tt))
    return line,

ani = FuncAnimation(fig, animate, frames=np.arange(0, len(t)), interval=25, repeat=True)

ax.set_xlim(-(L1+L2+1), L1+L2+1)
ax.set_ylim(-(L1+L2+1), L1+L2+1)
ax.set_aspect('equal')
ax.grid()
ani.save('double_pendulum.gif', writer='pillow', fps=5)

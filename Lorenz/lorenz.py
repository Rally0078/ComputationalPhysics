import matplotlib.pyplot as plt
import numpy as np
from sys import argv
import copy #For shallow copy
from cube import Cube
from math import floor

#Default initial values
initPos = (1, 1, 1)
initTime = 0
timeLimit = 100
params = (15,40,2.66)
numSteps = 40000

#################-----Command Line arguments-----###################
show3DFigure = False
showTimeSeries = False
showPhasePortrait = False

if "phase" in argv:
    showPhasePortrait = True
if "time" in argv:
    showTimeSeries = True
if ("3d" in argv) or ("3D" in argv):
    show3DFigure = True

#Lorenz system
def f(r: tuple, params):
    x, y, z = r
    sigma, rho, beta = params
    dx = sigma*(y - x)
    dy = x*(rho - z) - y
    dz = x*y - beta * z
    return dx, dy, dz


#RK4 solver for IVP
def RK4(func, init: tuple, t0: float, numSteps: int, params: tuple, maxTime = 10.0):
    h = (maxTime - t0)/numSteps     #Step size
    prevPosition = init

    x = np.empty(numSteps)
    y = np.empty(numSteps)
    z = np.empty(numSteps)
    x0, y0, z0 = prevPosition

    xdot = np.empty(numSteps)
    ydot = np.empty(numSteps)
    zdot = np.empty(numSteps)

    for i in range(0, numSteps):
        k0, l0, m0 = func(prevPosition, params)     #Gets xdot, ydot, zdot at given instant of time
        k1, l1, m1 = func((x0 + h * k0/2, y0 + h * l0/2, z0 + h * m0/2), params)
        k2, l2, m2 = func((x0 + h * k1/2, y0 + h * l1/2, z0 + h * m1/2), params)
        k3, l3, m3 = func((x0 + h * k2, y0 + h * l2, z0 + h * m2), params)
        x0 = x0 + h/6 * (k0 + 2*k1 + 2*k2 + k3)
        y0 = y0 + h/6 * (l0 + 2*l1 + 2*l2 + l3)
        z0 = z0 + h/6 * (m0 + 2*m1 + 2*m2 + m3)

        x[i] = x0
        y[i] = y0
        z[i] = z0
        prevPosition = x0, y0, z0
        xdot[i] = k0
        ydot[i] = l0
        zdot[i] = m0
    return x, y, z, xdot, ydot, zdot

x, y, z, dx, dy, dz = RK4(func = f, init = copy.copy(initPos), t0 = initTime, numSteps = numSteps, params = params, maxTime = timeLimit)    #params = (sigma, rho, beta)
zmax = np.array([])

#Plot solution of Lorenz system
fig = plt.figure(figsize=(12,9))
ax = fig.add_subplot(projection='3d')
ax.set_xlabel("x axis")
ax.set_ylabel("y axis")
ax.set_zlabel("z axis")
ax.plot(initPos[0], initPos[1], initPos[2], "ro", label="Initial Position")

ax.set_title("Lorenz system")
ax.set_xlim(floor(x.min()) - 10 , floor(x.max()) + 10)
ax.set_ylim(floor(y.min()) - 10 , floor(y.max()) + 10)
ax.set_zlim(floor(z.min()) - 10 , floor(z.max()) + 10)
ax.plot(x, y, z, lw = 0.7)

plt.savefig("lorenz.jpeg", dpi=250)
if show3DFigure == True:
    plt.show()
plt.close()

#Plot time series
fig, ax = plt.subplots(3,1, figsize=(12,9))

fig.suptitle("Time series of Lorenz system")
ax[0].set_ylabel(r'$x$', rotation="horizontal")
ax[1].set_ylabel(r'$y$', rotation="horizontal")
ax[2].set_ylabel(r'$z$', rotation="horizontal")
fig.supxlabel('Time (seconds)')

maxSample = 12000   #My own limit to show timeseries upto a particular time
maxTime = maxSample * (timeLimit - initTime)/numSteps
timeSteps = np.linspace(0, maxTime, maxSample)
ax[0].plot(timeSteps, x[:maxSample], linewidth="1.8")
ax[1].plot(timeSteps, y[:maxSample], linewidth="1.8")
ax[2].plot(timeSteps, z[:maxSample], linewidth="1.8")

for axs in ax:
    axs.margins(x=0)
    axs.grid()
fig.tight_layout()
plt.savefig("timeseries.jpeg", dpi=150)
if showTimeSeries == True:
    plt.show()
plt.close()

#Plot phase portrait
fig, ax = plt.subplots(3,1, figsize=(9, 14))
fig.suptitle("Phase portrait of Lorenz system")

ax[0].set_xlabel(r'$x$', rotation="horizontal")
ax[0].set_title(r'$x$ vs $\dot{x}$')
ax[1].set_xlabel(r'$y$', rotation="horizontal")
ax[1].set_title(r'$y$ vs $\dot{y}$')
ax[2].set_xlabel(r'$z$', rotation="horizontal")
ax[2].set_title(r'$z$ vs $\dot{z}$')

ax[0].set_ylabel(r'$\dot{x}$', rotation="horizontal")
ax[1].set_ylabel(r'$\dot{y}$', rotation="horizontal")
ax[2].set_ylabel(r'$\dot{z}$', rotation="horizontal")

maxSample = 10000
ax[0].plot(x[:maxSample], dx[:maxSample], linewidth="1.8", label="Phase space trajectory")
ax[0].plot(x[0], dx[0], "ro", label="Initial Position")
ax[1].plot(y[:maxSample], dy[:maxSample],linewidth="1.8")
ax[1].plot(y[0], dy[0], "ro")
ax[2].plot(z[:maxSample], dz[:maxSample],linewidth="1.8")
ax[2].plot(z[0], dz[0], "ro")

fig.legend()
for axs in ax:
    axs.grid()

fig.tight_layout(pad=2.5)

plt.savefig("phaseportrait.jpeg", dpi=150)
if showPhasePortrait == True:
    plt.show()
plt.close()

#Box counting dimension
cubeSide = 10
cubeLts = 75
cubeArray = []
for i in range(-cubeLts, cubeLts, cubeSide):
    for j in range(-cubeLts, cubeLts, cubeSide):
        for k in range(-cubeLts, cubeLts, cubeSide):
            cubeArray.append(Cube(i, j, k, cubeSide))
# Todo: Iterate through all the cubes in cubeArray and check if point is in cube(preferably multithreaded)

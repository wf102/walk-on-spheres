import numpy as np
import matplotlib.pyplot as plt

x0 = 0.0
x1 = 1.0
y0 = 0.0
y1 = 1.0

T_x0 = 10.0
T_x1 = 10.0
T_y0 = 20.0
T_y1 = 20.0

eps = 0.01
grid_size = 20

def boundary_temp(x, y):

    edge = np.argmin([x - x0, x1 - x, y - y0, y1 - y])

    return (T_x0, T_x1, T_y0, T_y1)[edge]



def walk_once(x, y):

    while True:

        r = min(x - x0, x1 - x, y - y0, y1 - y)

        if r < eps:
            return boundary_temp(x, y)

        theta = np.random.uniform(0, 2*np.pi)

        x += r * np.cos(theta)
        y += r * np.sin(theta)


def temperature(x, y, n_walks=1000):

    # return 10

    samples = [walk_once(x, y) for i in range(n_walks)]
    return np.mean(samples)


def main():
    print("Hello from walk-on-spheres!")

    # define temp grid
    T = np.empty((grid_size, grid_size))

    # define sample points
    xs = np.linspace(x0, x1, grid_size)
    ys = np.linspace(y0, y1, grid_size)


    # Fill grid with estimates
    for i in range(1, grid_size-1):
        print(i)
        for j in range(1, grid_size-1):
            T[j, i] = temperature(xs[i], ys[j])

    # Add BCs to grid
    T[:, 0]  = T_x0
    T[:, -1] = T_x1
    T[0, :]  = T_y0
    T[-1, :] = T_y1
 
    T[0, 0] = 0.5 * (T_x0 + T_y0)
    T[0, -1] = 0.5 * (T_x0 + T_y1)
    T[-1, 0] = 0.5 * (T_x1 + T_y0)
    T[-1, -1] = 0.5 * (T_x1 + T_y1)

    print(T)

    plt.imshow(T, cmap='hot', interpolation='nearest')
    plt.show()


if __name__ == "__main__":
    main()

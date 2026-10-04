import numpy as np
import matplotlib.pyplot as plt

# Rectangle widths
Lx = 1.0
Ly = 1.0

# Temperature boundary conditions (left, right, top, bottom)
T_l = 100.0
T_r = 50.0
T_t = 100.0
T_b = 0.0

eps = 0.01
grid_size = 20

pi = np.pi

def boundary_temp(x, y):

    edge = np.argmin([x, Lx - x, y, Ly - y])
    return (T_l, T_r, T_b, T_t)[edge]


def walk_once(x, y):

    while True:
        r = min(x, Lx - x, y, Ly - y)
        if r < eps:
            return boundary_temp(x, y)
        theta = np.random.uniform(0, 2 * pi)
        x += r * np.cos(theta)
        y += r * np.sin(theta)


def temperature_wos(x, y, n_walks=1000):

    samples = [walk_once(x, y) for i in range(n_walks)]
    return np.mean(samples)

def sinh_ratio(a, b):

    return np.exp(a - b) * (1.0 - np.exp(-2.0 * a)) / (1.0 - np.exp(-2.0 * b))

def temperature(x, y, terms = 20):

    sum = 0
    for n in range(1, 2 * terms, 2):
        sum += 4 / (n * pi) * (
            T_b * np.sin(n * pi * x / Lx) * sinh_ratio(n * pi * (Ly - y) / Lx, n * pi * Ly / Lx) +
            T_t * np.sin(n * pi * x / Lx) * sinh_ratio(n * pi * y / Lx, n * pi * Ly / Lx) +
            T_l * np.sin(n * pi * y / Ly) * sinh_ratio(n * pi * (Lx - x) / Ly, n * pi * Lx / Ly) +
            T_r * np.sin(n * pi * y / Ly) * sinh_ratio(n * pi * x / Ly, n * pi * Lx / Ly)
            )
    return sum


def plot(T):

    fig, axes = plt.subplots(1, 2, figsize=(5, 5))

    dx = 1.0/(grid_size - 1)
    extent = [-dx/2, 1.0 + dx/2, -dx/2, 1.0 + dx/2]
    
    axes[0].imshow(
        T[:,:,0],
        cmap='plasma',
        interpolation='nearest',
        origin='lower',
        extent=extent
    )

    axes[1].imshow(
        T[:,:,1],
        cmap='plasma',
        interpolation='nearest',
        origin='lower',
        extent=extent
    )

    for ax in axes:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xticks([])
        ax.set_yticks([])

    axes[0].set_title("Walk-on-spheres")
    axes[1].set_title("Analytic")

    plt.tight_layout()
    plt.show()


def main():

    # define temp grid
    T = np.empty((grid_size, grid_size, 2))

    # define sample points
    xs = np.linspace(0, Lx, grid_size)
    ys = np.linspace(0, Ly, grid_size)

    # Fill grid with estimates
    for i in range(1, grid_size-1):
        print(i)
        for j in range(1, grid_size-1):
            T[j, i, 0] = temperature_wos(xs[i], ys[j])
            T[j, i, 1] = temperature(xs[i], ys[j])

    # Add BCs to grid
    T[:, 0, :]  = T_l
    T[:, -1, :] = T_r
    T[0, :, :]  = T_b
    T[-1, :, :] = T_t
    
    # Average corners
    T[0, 0] = 0.5 * (T_l + T_b)
    T[-1, 0] = 0.5 * (T_l + T_t)
    T[0, -1] = 0.5 * (T_r + T_b)
    T[-1, -1] = 0.5 * (T_r + T_t)

    plot(T)

if __name__ == "__main__":
    main()

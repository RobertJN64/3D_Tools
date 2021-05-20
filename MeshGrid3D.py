import matplotlib.pyplot as plt
import numpy as np

def graph(data, override_h = 1):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    X, Y = np.meshgrid(range(0, len(data[0])), range(0, len(data)))

    mv = 0

    for y in range(0, len(data)):
        for x in range(0, len(data[0])):
            if data[y][x] is not None and data[y][x] > mv:
                mv = data[y][x]


    ax.contour3D(X, Y, data, round(mv), cmap="summer")
    ax.set_zlim(0, mv * override_h)


    plt.show()
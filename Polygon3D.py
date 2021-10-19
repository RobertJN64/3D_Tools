import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

sampleData = [[0,0,0,0,0],
              [0,0,0,0,0],
              [0,1,1,1,0],
              [0,1,2,1,0],
              [0,0,0,0,0]]

def graph(data, override_h = 1):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    #create list of vertices
    polygons = []
    hs = []
    for y in range(0, len(data)-1):
        for x in range(0, len(data[0])-1):
            if data[y][x] is None or data[y + 1][x] is None or data[y][x+1] is None or data[y + 1][x + 1] is None:
                continue

            mpoint = sum([data[y][x], data[y][x+1], data[y+1][x], data[y+1][x+1]])/4

            vertices = [(x, y, data[y][x]),
                        (x + 1, y, data[y][x + 1]),
                        (x + 0.5, y + 0.5, mpoint)]
            polygons.append(vertices)
            # vertices = [(x, y, data[y][x]),
            #             (x, y + 1, data[y+1][x]),
            #             (x + 0.5, y + 0.5, mpoint)]
            # #polygons.append(vertices)
            # vertices = [(x + 1, y, data[y][x + 1]),
            #             (x + 1, y + 1, data[y + 1][x + 1]),
            #             (x + 0.5, y + 0.5, mpoint)]
            # #polygons.append(vertices)
            # vertices = [(x, y + 1, data[y + 1][x]),
            #             (x + 1, y + 1, data[y + 1][x + 1]),
            #             (x + 0.5, y + 0.5, mpoint)]
            # #polygons.append(vertices)
            for i in range(0, 4):
                hs.append(mpoint)

    mv = 0

    for y in range(0, len(data)):
        for x in range(0, len(data[0])):
            if data[y][x] is not None and data[y][x] > mv:
                mv = data[y][x]

    print("Rendering", len(polygons), "polygons")
    for i in range(0, len(polygons)):
        poly = polygons[i]
        h = hs[i]

        #print(poly)
        p = Poly3DCollection([poly])
        p.set_color((h/mv, h/mv, h/mv))
        p.set_edgecolor("black")
        p.set_linewidth(0.01)

        ax.add_collection3d(p)

    ax.set_xlim(0, len(data[0])-1)
    ax.set_ylim(0, len(data)-1)
    ax.set_zlim(0, mv * override_h)

    plt.show()
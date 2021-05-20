import numpy as np
from stl import mesh
import sys

def recMin(data):
    m = data[0][0]
    for row in data:
        for i in range(0, len(row)):
            if m is None:
                m = i
            elif i is not None and i < m:
                m = i
    return m

def stlFromMesh(data, fname):
    data.insert(0, [None]*len(data[0]))
    data.insert(len(data), [None] * len(data[0]))
    for row in data:
        row.insert(0, None)
        row.append(None)

    lowpoint = recMin(data) - 1

    faces = []
    for y in range(0, len(data) - 1):
        sys.stdout.write("\r" + "Creating faces: " + str(round(y * 100 / len(data)-1)) + "%")
        for x in range(0, len(data[0]) - 1):
            vTL = [x, y, data[y][x]]
            vTR = [x + 1, y, data[y][x + 1]]
            vBL = [x, y + 1, data[y + 1][x]]
            vBR = [x + 1, y + 1, data[y + 1][x + 1]]

            aTL = [x, y, lowpoint]
            aTR = [x + 1, y, lowpoint]
            aBL = [x, y + 1, lowpoint]
            aBR = [x + 1, y + 1, lowpoint]

            #FLAT
            if vTL[2] is not None and vTR[2] is not None and vBL[2] is not None and vBR[2] is not None:
                mpoint = sum([data[y][x], data[y][x + 1], data[y + 1][x], data[y + 1][x + 1]]) / 4
                vMID = [x + 0.5, y + 0.5, mpoint]
                aMID = [x + 0.5, y + 0.5, lowpoint]

                faces.append([vTR, vTL, vMID])
                faces.append([vTL, vBL, vMID])
                faces.append([vBL, vBR, vMID])
                faces.append([vBR, vTR, vMID])

                faces.append([aTR, aTL, aMID])
                faces.append([aTL, aBL, aMID])
                faces.append([aBL, aBR, aMID])
                faces.append([aBR, aTR, aMID])


            else:
                # TOP
                if vBL[2] is not None and vBR[2] is not None:
                    faces.append([vBL, vBR, aBR])
                    faces.append([aBR, aBL, vBL])

                #BOTTOM
                if vTL[2] is not None and vTR[2] is not None:
                    faces.append([vTL, vTR, aTR])
                    faces.append([aTR, aTL, vTL])

                # Left
                if vTR[2] is not None and vBR[2] is not None:
                    faces.append([vTR, vBR, aBR])
                    faces.append([aBR, aTR, vTR])

                # Right
                if vTL[2] is not None and vBL[2] is not None:
                    faces.append([vTL, vBL, aBL])
                    faces.append([aBL, aTL, vTL])

    sys.stdout.write("\r" + "Creating faces: done!")

    shape = mesh.Mesh(np.zeros(len(faces), dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            shape.vectors[i][j] = f[j]

    shape.save(fname + ".stl")



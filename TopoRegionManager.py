import copy

import RelativeGeoComputer as rgc

import matplotlib.pyplot as pyplot
import matplotlib.colors as mcolors
from PIL import Image
from sys import stdout

#region classes
class RefMode:
    NoneAssigned = -1
    Peak = 0
    NeutralDif = 1
    NegativeDif = 2
    PositiveDif = 3

class Tile:
    def __init__(self, num, peaks, circles):
        self.lineID = num
        self.visited = False
        self.isLine = num > 0
        self.isPeak = num in peaks
        self.isCircle = num in circles
        self.region = -1

class Region:
    def __init__(self, borders, edge):
        self.borders = borders
        self.edge = edge
        self.ref_region = None
        self.mode = RefMode.NoneAssigned
        self.forceHeight = False
        self.currentHeight = 0 #doesn't matter because forceHeight
#endregion classes

#region Helper Funcs
def floodFill(grid, x, y, regionID):
    borders = []
    queue = [(x,y)]
    isEdge = False

    while len(queue) > 0:
        xpos, ypos = queue.pop(0)
        if ypos < 0 or xpos < 0 or ypos >= len(grid) or xpos >= len(grid[0]):
            isEdge = True
        else:
            pix =  grid[ypos][xpos]
            if (not pix.isLine) and (not pix.visited):
                pix.visited = True
                pix.region = regionID

                queue.append((xpos + 1, ypos))
                queue.append((xpos - 1, ypos))
                queue.append((xpos, ypos + 1))
                queue.append((xpos, ypos - 1))

            if pix.isLine and pix.lineID not in borders:
                borders.append(pix.lineID)

    return borders, isEdge

def renderRegions(grid, c=None, click=False):
    if c is None:
        c = colors

    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    current_img = Image.new('RGB', (len(grid[0]), len(grid)), (255, 255, 255))

    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            pix = row[x]
            if not pix.isLine:
                current_img.putpixel((x, y), c[pix.region % len(c)])
    ax.imshow(current_img)

    if click:
        fig.canvas.mpl_connect('button_press_event', onClick)

    pyplot.show()

def overlap(a, b):
    for item in a:
        if item in b:
            return True
    return False

def onClick(event):
    if event.xdata is not None and event.ydata is not None:
        print(event.xdata, event.ydata)

def inverseWeightedAverage(weights, vals):
    m = sum(weights)
    total = 0
    counter = 0
    for i in range(0, len(weights)):
        total += vals[i] * (m - weights[i])
        counter += (m - weights[i])
    return total/counter

def linearScan(x, y, lgrid, maxdis):
    pointInfo = []
    row = lgrid[y]
    for xpos in range(x, min(x + maxdis, len(row))):
        pix = row[xpos]
        if pix != -1:
            pointInfo.append([pix, xpos-x]) #height, distance
            break
    for xpos in range(x, max(x - maxdis,0) -1):
        pix = row[xpos]
        if pix != -1:
            pointInfo.append([pix, x - xpos])  # height, distance
            break
    for ypos in range(y, min(y + maxdis, len(lgrid))):
        pix = lgrid[ypos][x]
        if pix != -1:
            pointInfo.append([pix, ypos - y]) #height, distance
            break
    for ypos in range(y, max(y - maxdis, 0) -1):
        pix = lgrid[ypos][x]
        if pix != -1:
            pointInfo.append([pix, y - ypos]) #height, distance
            break

    if len(pointInfo) == 0:
        return False, 0

    distances = []
    heights = []
    for pInfo in pointInfo:
        if pInfo[0] in heights:
            index = heights.index(pInfo[0])
            distances[index] = min(distances[index], pInfo[1])
        else:
            heights.append(pInfo[0])
            distances.append(pInfo[1])

    if max(heights) == min(heights):
        return True, heights[0]

    return True, inverseWeightedAverage(distances, heights)



colors = []
def createColors():
    for color in list(mcolors.CSS4_COLORS.values()):
        r, g, b = mcolors.colorConverter.to_rgb(color)
        colors.append((round(r*255),round(g*255),round(b*255)))
createColors()
#endregion

def process(origgrid, circles, peaks):
    regionDB = []
    grid = []

    #region Data Converts
    print("Converting data types...")
    for row in origgrid:
        l = []
        for item in row:
            l.append(Tile(item, peaks, circles))
        grid.append(l)
    #endregion
    #region Flood Fill
    print("Flood fill") #Switch to scan + join fill
    for y in range(0, len(grid)):
        stdout.write("\r" + str(round(y*100/len(grid))) + "%")
        for x in range(0, len(grid[0])):
            pix = grid[y][x]
            if not pix.isLine and not pix.visited:
                borders, isEdge = floodFill(grid, x, y, len(regionDB))
                regionDB.append(Region(borders, isEdge))
    print("\nFound " + str(len(regionDB)) + " regions.")
    #renderRegions(grid)
    #endregion
    #Lock onto a peak
    simpleregions = []
    for region in regionDB:
        borders = region.borders
        if len(borders) == 2 and not region.edge:
            print("HANDLING CIRCLE:", borders[0], " & ", borders[1])
            simpleregions.append(region)

        if len(borders) == 1 and not region.edge and borders[0] in peaks:
            region.mode = RefMode.Peak

    for i in range(0, len(simpleregions)):
        iregion = simpleregions[i]
        for p in peaks:
            if p in iregion.borders:
                iregion.ref_region = regionDB[p]
                iregion.mode = RefMode.NegativeDif #below peak

        for j in range(0, len(simpleregions)):
            if i != j:
                jregion = simpleregions[j]
                if overlap(jregion.borders, iregion.borders):
                    if iregion.mode == RefMode.NegativeDif or iregion.mode == RefMode.PositiveDif and jregion.mode == RefMode.NoneAssigned:
                        jregion.mode = iregion.mode
                        jregion.ref_region = iregion

                    elif jregion.mode == RefMode.NegativeDif or jregion.mode == RefMode.PositiveDif and iregion.mode == RefMode.NoneAssigned:
                        iregion.mode = jregion.mode
                        iregion.ref_region = jregion

                    elif jregion.mode == RefMode.NoneAssigned and iregion.mode == RefMode.NoneAssigned:
                        iregion.mode = RefMode.NeutralDif
                        jregion.mode = RefMode.NeutralDif
                        iregion.ref_region = jregion
                        jregion.ref_region = iregion #create circular reference


    print(simpleregions)
    colorificate(grid, regionDB, peaks)

    regionINFO = rgc.forceComputeGeometry(regionDB)
    print("Matching regions and lines...")
    lineHDB = {}
    for region in regionINFO:
        for border in region.borders:
            if region.forceHeight:
                if border not in lineHDB:
                    lineHDB[border] = [region.currentHeight]
                else:
                    lineHDB[border].append(region.currentHeight)

    lineDB = {}
    for key in lineHDB:
        total = 0
        for v in lineHDB[key]:
            total += v
        lineDB[key] = total/len(lineHDB[key])

    print("Computing line heights...")
    lgrid = []
    for row in grid:
        lrow = []
        for item in row:
            if item.isLine:
                lrow.append(lineDB.get(item.lineID, 0)) #TODO - defaulting
            else:
                lrow.append(-1) #h not yet computed
        lgrid.append(lrow)

    print("Computing point heights")

    mgrid = []
    for y in range(0, len(lgrid)):
        stdout.write("\r" + str(round(y * 100 / len(lgrid))) + "%")
        mrow = []
        for x in range(0, len(lgrid[0])):
            pix = lgrid[y][x]
            if pix == -1:
                borders = copy.deepcopy(regionDB[grid[y][x].region].borders)
                if len(borders) > 1:
                    valid, num = linearScan(x, y, lgrid, 10)
                    if not valid:
                        num = regionINFO[grid[y][x].region].currentHeight
                    mrow.append(num)
                else:
                    mrow.append(regionINFO[grid[y][x].region].currentHeight)
            else:
                mrow.append(pix)
        mgrid.append(mrow)

    print()
    return mgrid


def colorificate(grid, regionDB, peaks):
    cregions = []
    for region in regionDB:
        if region.edge:
            cregions.append((0,0,255))
        else:
            cregions.append((255,0,0))
    renderRegions(grid, cregions)


    # cregions = []
    # for region in regionDB:
    #     borders = region.borders
    #     if len(borders) == 1 and borders[0] in peaks:
    #         cregions.append((0,0,255))
    #     elif len(borders) == 2 and overlap(borders, peaks):
    #         cregions.append((200,0,0))
    #     elif overlap(borders, peaks):
    #         cregions.append((0,200,0))
    #     else:
    #         cregions.append((100,100,100))
    # renderRegions(grid, cregions)
    #
    # cregions = []
    # for region in regionDB:
    #     borders = region.borders
    #     if len(borders) == 1 and borders[0] in peaks:
    #         cregions.append((0, 0, 255)) #peaks are blue
    #     elif len(borders) == 2:
    #         cregions.append((200, 100, 0)) #normal regions are orange
    #     elif len(borders) >= 3:
    #         cregions.append((200, 0, 0)) #hard regions are red
    #     elif len(borders) == 1 and borders[0] not in peaks:
    #         cregions.append((0, 255, 0)) #side regions are green
    #     else:
    #         print("ERROR?", borders)
    #         cregions.append((0, 0, 0)) #error is black
    #
    # renderRegions(grid, cregions, click=True)


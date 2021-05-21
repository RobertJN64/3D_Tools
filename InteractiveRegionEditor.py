import matplotlib.pyplot as pyplot
from PIL import Image

class RefMode:
    NoneAssigned = -1
    Peak = 0
    NeutralDif = 1
    NegativeDif = 2
    PositiveDif = 3
    NoDif = 4 #handle edges easyily because lazy

regionDB = []
grid = []
last_region_clicked = None

def onClick(event):
    global grid
    global regionDB
    global last_region_clicked
    if event.xdata is not None and event.ydata is not None:
        print(event.xdata, event.ydata)

    xpos = round(event.xdata)
    ypos = round(event.ydata)

    tile = grid[ypos][xpos]
    region = regionDB[tile.region]

    if last_region_clicked is None:
        last_region_clicked = region

    else:
        regionA = region
        regionB = last_region_clicked
        last_region_clicked = None

        if regionA.mode == [RefMode.NoDif] and regionA.ref_region == [regionB]:
            regionA.mode = []
            regionA.ref_region = []

        regionB.mode.append(RefMode.NegativeDif)
        regionB.ref_region.append(regionA)

        fig = pyplot.gcf()
        ax = fig.add_subplot(111)
        ax.imshow(createImage())
        pyplot.show()


def colorificate():
    cregions = []
    for region in regionDB:
        if RefMode.Peak in region.mode:
            cregions.append((0, 0, 255))
        elif RefMode.PositiveDif in region.mode or RefMode.NegativeDif in region.mode:
            cregions.append((255, 0, 0))
        elif len(region.mode) == 0:
            cregions.append((200, 200, 200))
        elif RefMode.NoDif in region.mode:
            cregions.append((255, 128, 0))
        elif RefMode.NeutralDif in region.mode:
            cregions.append((0, 255, 0))
        else:
            print("Error colorizing mode: ", region.mode)
    return cregions

def createImage():
    global grid
    global regionDB
    colors = colorificate()
    current_img = Image.new('RGB', (len(grid[0]), len(grid)), (255, 255, 255))

    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            pix = row[x]
            if not pix.isLine:
                current_img.putpixel((x, y), colors[pix.region])
    return current_img

def edit(Grid, RegionDB):
    global grid
    global regionDB
    global last_region_clicked
    grid = Grid
    regionDB = RegionDB
    last_region_clicked = None

    fig = pyplot.figure()
    ax = fig.add_subplot(111)
    current_img = createImage()
    ax.imshow(current_img)
    fig.canvas.mpl_connect('button_press_event', onClick)
    pyplot.show()

    return regionDB
import copy

from PIL import Image
from matplotlib import pyplot

colors = [(255,0,0),
          (0,255,0),
          (100,100,0),
          (0,100,100),
 	      (100,0,100),
          (100,100,100),
          (128,128,128),
          (128,0,0),
          (128,128,0),
          (0,128,0),
          (128,0,128),
          (0,128,128),
          (0,0,128)]

def searchAround(x, y, grid):
    options = []

    if y < len(grid)-1:
        pix = grid[y+1][x]
        if pix not in options and pix not in [-1, 0]:
            options.append(pix)
    if y > 0:
        pix = grid[y - 1][x]
        if pix not in options and pix not in [-1, 0]:
            options.append(pix)
    if x < len(grid[0]) - 1:
        pix = grid[y][x + 1]
        if pix not in options and pix not in [-1, 0]:
            options.append(pix)
    if x > 0:
        pix = grid[y][x - 1]
        if pix not in options and pix not in [-1, 0]:
            options.append(pix)

    return options

def renderGrid(grid, imgpos, fig, show):
    if show:
        ax = fig.add_subplot(3,3,imgpos)
        current_img = Image.new('RGB', (len(grid[0]), len(grid)), (255, 255, 255))

        for y in range(0, len(grid)):
            row = grid[y]
            for x in range(0, len(row)):
                pix = row[x]
                if pix != -1:
                    current_img.putpixel((x, y), colors[pix % len(colors)])
        ax.imshow(current_img)

def linkedDict(refdict, key):
    result = refdict[key]
    while refdict[result] != result:
        result = refdict[result]
    return result

def process(fname, show):
    #region load
    print("Loading image")
    imgpos = 1
    orig_img = Image.open(fname)
    grey_img = Image.open(fname).convert('LA')
    current_img = orig_img.copy()
    #endregion
    #region display the array of pixels as an image
    print("Processing image")
    if show:
        fig = pyplot.figure()
        ax = fig.add_subplot(3,3,imgpos)
        imgpos += 1
        ax.imshow(grey_img)
    else:
        fig = None
    #endregion
    #region createGrid
    print("Finding lines")
    grid = []
    for y in range(0, orig_img.height):
        row = []
        for x in range(0, orig_img.width):
            pix, alph = grey_img.getpixel((x,y))
            if pix < 200:
                current_img.putpixel((x,y), (0,0,255,0))
                row.append(0)
            else:
                row.append(-1)
        grid.append(row)

    if show:
        ax = fig.add_subplot(3,3,imgpos)
        imgpos += 1
        ax.imshow(current_img)
    #endregion
    #region colorize lines
    print("Coloring lines")
    colorcounter = 0
    reftracker = {}
    #Tag each line with a sep color
    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            pix = row[x]
            if pix == 0:
                options = searchAround(x, y, grid)
                if len(options) == 0:
                    colorcounter += 1
                    grid[y][x] = colorcounter
                    reftracker[colorcounter] = colorcounter

                elif len(options) == 1:
                    grid[y][x] = options[0]

                else:
                    colorcounter += 1
                    reftracker[colorcounter] = colorcounter
                    for num in options:
                        reftracker[linkedDict(reftracker, num)] = colorcounter

                    grid[y][x] = colorcounter

    for row in grid:
        for i in range(0, len(row)):
            pix = row[i]
            if pix != -1:
                row[i] = linkedDict(reftracker, pix)

    renderGrid(grid, imgpos, fig, show)
    imgpos += 1
    #endregion
    #region remove edge lines
    print("Removing edge lines")
    fullGrid = copy.deepcopy(grid)
    invalid = []
    for pix in grid[0]:
        if pix != -1 and pix not in invalid:
            invalid.append(pix)
    for pix in grid[len(grid)-1]:
        if pix != -1 and pix not in invalid:
            invalid.append(pix)
    for row in grid:
        pix = row[0]
        if pix != -1 and pix not in invalid:
            invalid.append(pix)
        pix = row[len(row)-1]
        if pix != -1 and pix not in invalid:
            invalid.append(pix)

    for y in range(0, len(grid)):
        row = grid[y]
        for x in range(0, len(row)):
            pix = row[x]
            if pix in invalid:
                row[x] = -1

    renderGrid(grid, imgpos, fig, show)
    imgpos += 1
    #endregion
    #region scan for empty circles
    print("Finding circles")
    invalidlines = []
    for y in range(0, len(grid)):
        for x in range(0, len(grid[0])):
            pix = grid[y][x]
            if pix != -1 and pix not in invalidlines:
                #scan downward
                interior = False
                lastpix = pix
                for d in range(y + 1, len(grid)):
                    npix = grid[d][x]
                    if npix == -1 and lastpix == pix:
                        interior = not interior

                    if npix != pix and npix > 0 and interior and pix not in invalidlines:
                        invalidlines.append(pix)

                    lastpix = npix

                if interior and pix in invalidlines:
                    invalidlines.remove(pix)

    peaks = []
    cgrid = copy.deepcopy(grid)
    for y in range(0, len(cgrid)):
        for x in range(0, len(cgrid[0])):
            pix = cgrid[y][x]
            if pix in invalidlines:
                cgrid[y][x] = -1
            elif pix != -1 and pix not in peaks:
                peaks.append(pix)


    renderGrid(cgrid, imgpos, fig, show)
    imgpos += 1
    #endregion
    #region Reprocess
    print("Reprocessing...")
    keycounter = 1
    remaps = {}
    circles = []
    for row in fullGrid:
        for x in range(0, len(row)):
            pix = row[x]
            if pix != -1 and pix not in remaps:
                remaps[pix] = keycounter
                keycounter += 1
                if pix not in invalid and pix not in circles:
                    circles.append(pix)

    for row in fullGrid:
        for x in range(0, len(row)):
            pix = row[x]
            if pix != -1:
                row[x] = remaps[pix]

    for i in range(0, len(circles)):
        circles[i] = remaps[circles[i]]

    for i in range(0, len(peaks)):
        peaks[i] = remaps[peaks[i]]

    renderGrid(fullGrid, imgpos, fig, show)
    imgpos += 1

    #for row in fullGrid:
        #print(row)

    print("Peaks: ", peaks)
    print("Circles: ", circles)

    #endregion
    if show:
        pyplot.show()

    return fullGrid, circles, peaks
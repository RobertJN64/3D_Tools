def scan(fname):
    with open(fname) as f:
        lines = f.readlines()

    dps = []

    validpointcounter = 0
    for line in lines:
        minilist = []
        points = line.split(" ")

        for point in points:
            if float(point) == -9999:
                minilist.append(None)
            else:
                validpointcounter += 1
                minilist.append(float(point) * -1 + 10)

        dps.append(minilist)

    print("Found a datset with", len(dps) * len(dps[0]), "total points")
    print("Found a datset with", validpointcounter, "valid points!")
    #print(dps)
    return dps

def listscan(fname, interval):
    with open(fname) as f:
        lines = f.readlines()

    xvals = []
    yvals = []
    zvals = []

    for line in lines:
        x, y, z = line.split(' ')
        xvals.append(float(x))
        yvals.append(float(y))
        zvals.append(float(z))

    minx, maxx = min(xvals), max(xvals)
    miny, maxy = min(yvals), max(yvals)
    minz, maxz = min(zvals), max(zvals)

    for i in range(0, len(xvals)):
        xvals[i] = (xvals[i] - minx)/interval
        yvals[i] = (yvals[i] - miny)/interval
        zvals[i] -= minz

    maxx = int(max(xvals))
    maxy = int(max(yvals))

    dps: list = []
    for y in range(0, maxy+1):
        mlist = []
        for x in range(0, maxx+1):
            mlist.append(None)
        dps.append(mlist)

    for i in range(0, len(xvals)):
        dps[int(yvals[i])][int(xvals[i])] = zvals[i]

    return dps

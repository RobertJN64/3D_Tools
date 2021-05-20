def scrape(section, start, end, index=0):
    start = section.index(start, index) + len(start)
    end = section.index(end, start)
    return section[start:end]

def scan(fname):
    with open(fname) as f:
        raw = f.read()

    index = 0

    datapoints = []

    for i in range(0, raw.count('div id="MapPixel"')):
        index = raw.index('div id="MapPixel"', index+1)
        end = raw.index('div', index+20)
        #print(raw[index:end])
        xpos = int(int(scrape(raw[index:end], 'left: ', 'px'))/5)
        ypos = int(int(scrape(raw[index:end], 'top: ', 'px'))/5)
        colors = scrape(raw[index:end], 'rgba(', ')').split(',')
        h = 255 + int(colors[0]) - int(colors[2])
        #print(xpos, ypos)
        datapoints.append([xpos, ypos, h])

    maxx = 0
    maxy = 0
    for point in datapoints:
        if point[0] > maxx:
            maxx = point[0]
        if point[1] > maxy:
            maxy = point[1]

    outpoints = []
    for i in range(0, maxy+1):
        mlist = []
        for j in range(0, maxx+1):
            mlist.append(None)
        outpoints.append(mlist)

    for point in datapoints:
        #print(point[0], point[1])
        outpoints[point[1]][point[0]] = point[2]


    return outpoints

def compress(data, interval):
    outdata = []
    for y in range(0, len(data), interval):
        mlist = []
        for x in range(0, len(data[0]), interval):
            mlist.append(data[y][x])
        outdata.append(mlist)
    return outdata

def DLAvg(data, x, y, interval):
    total = 0
    for xpos in range(x, x+interval):
        for ypos in range(y, y+interval):
            if ypos >= len(data) or xpos >= len(data[0]):
                total += data[y][x]
            else:
                total += data[ypos][xpos]

    return total/ (interval * interval)

def smartCompress(data, interval):
    outdata = []
    for y in range(0, len(data), interval):
        mlist = []
        for x in range(0, len(data[0]), interval):
            mlist.append(DLAvg(data, x, y, interval))
        outdata.append(mlist)
    return outdata
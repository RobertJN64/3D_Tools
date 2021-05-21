from sys import stdout

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

def smooth(data, size):
    outdata = []
    for y in range(0, len(data)):
        stdout.write("\r" + "Smoothing data: " + str(round(100 * y / len(data))) + "%.")
        row = []
        for x in range(0, len(data)):
            total = 0
            count = 0
            for ypos in range(y - size, y + size):
                for xpos in range(x - size, x + size):
                    if ypos < 0 or xpos < 0 or ypos >= len(data) or xpos >= len(data[0]):
                        pass
                    else:
                        count += 1
                        total += data[ypos][xpos]
            row.append(total/count)
        outdata.append(row)
    print()
    return outdata
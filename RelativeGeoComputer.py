class RefMode:
    NoneAssigned = -1
    Peak = 0
    NeutralDif = 1
    NegativeDif = 2
    PositiveDif = 3
    NoDif = 4

def forceComputeGeometry(regionDB):
    print("\n\n--------------------------")
    print("Found", len(regionDB), "regions. Preparing to compute geometry.")

    unassignedCounter = 0
    for region in regionDB:
        if len(region.mode) == 0:
            unassignedCounter += 1

    loopedReferenceCounter = 0
    for region in regionDB:
        if RefMode.NeutralDif in region.mode:
            loopedReferenceCounter += 1

    if unassignedCounter > 0:
        print("Found", unassignedCounter, "regions with no info: (" + str(round(100*unassignedCounter/len(regionDB))) + "%).",
              "Countinuing anyway.")
    if loopedReferenceCounter > 0:
        print("Found", loopedReferenceCounter, "regions with looped references: (", round(100*loopedReferenceCounter/len(regionDB)), "%).",
              "Countinuing anyway.")
    if unassignedCounter == 0 and loopedReferenceCounter == 0:
        print("All geometry is valid!")

    foundStartingPoint = False
    for region in regionDB:
        if region.forceHeight:
            print("Found specified height, preparing to calc geo.")
            foundStartingPoint = True
            break

        if RefMode.Peak in region.mode:
            print("Found peak, preparing to calc geo.")
            foundStartingPoint = True
            region.forceHeight = True
            region.currentHeight = 40 #TODO - max h handling
            break

    if not foundStartingPoint:
        print("Error, no starting point found. Terminating calc.")
        return regionDB

    fullyTerminated = False
    while not fullyTerminated:
        #region Compute Relative Geometry
        madeChangesLastLoop = True
        while madeChangesLastLoop:
            madeChangesLastLoop = False
            for region in regionDB:
                for regionCounter in range(0, len(region.ref_region)):
                    ref_region = region.ref_region[regionCounter]
                    mode = region.mode[regionCounter]
                    #forward prop
                    if (not region.forceHeight) and ref_region.forceHeight:
                        region.forceHeight = True
                        if mode == RefMode.NegativeDif:
                            region.currentHeight = ref_region.currentHeight - 5
                            madeChangesLastLoop = True
                        elif mode == RefMode.PositiveDif:
                            region.currentHeight = ref_region.currentHeight + 5
                            madeChangesLastLoop = True
                        elif mode == RefMode.NoDif:
                            region.currentHeight = ref_region.currentHeight
                            madeChangesLastLoop = True
                        elif mode == RefMode.NeutralDif:
                            print("Error, referencing a region with difference not specified.")
                        elif mode == RefMode.Peak:
                            print("Error, peak is attempting to reference a region.")
                        elif mode == RefMode.NoneAssigned:
                            print("Error, referencing a region but no mode specified.")
                        else:
                            print("Error, unexpected region code: ", mode)
                    #back prop
                    elif region.forceHeight and (not ref_region.forceHeight):
                        ref_region.forceHeight = True
                        if mode == RefMode.NegativeDif:
                            ref_region.currentHeight = region.currentHeight + 5
                            madeChangesLastLoop = True
                        elif mode == RefMode.PositiveDif:
                            ref_region.currentHeight = region.currentHeight - 5
                            madeChangesLastLoop = True
                        elif mode == RefMode.NoDif:
                            ref_region.currentHeight = region.currentHeight
                            madeChangesLastLoop = True
                        elif mode == RefMode.NeutralDif:
                            print("Backprop Error, referencing a region with difference not specified.")
                        elif mode == RefMode.Peak:
                            print("Backprop Error, peak is attempting to reference a region.")
                        elif mode == RefMode.NoneAssigned:
                            print("Backprop Error, referencing a region but no mode specified.")
                        else:
                            print("Backprop Error, unexpected region code: ", mode)
                    #error checking
                    elif region.forceHeight and ref_region.forceHeight:
                        if mode == RefMode.PositiveDif:
                            if region.currentHeight != ref_region.currentHeight + 5:
                                print("Geometry construction error (Pos): Regions",
                                      regionDB.index(region), regionDB.index(ref_region))
                        if mode == RefMode.NegativeDif:
                            if region.currentHeight != ref_region.currentHeight - 5:
                                print("Geometry construction error (Neg): Regions",
                                      regionDB.index(region), regionDB.index(ref_region))
                        if mode == RefMode.NoDif:
                            if region.currentHeight != ref_region.currentHeight:
                                print("Geometry construction error (=): Regions",
                                      regionDB.index(region), regionDB.index(ref_region))
        #endregion
        #Attempt to find new starting points
        fullyTerminated = True
        for region in regionDB:
            if RefMode.Peak in region.mode and not region.forceHeight:
                print("Geometry not fully constrained. Peak relative height may be wrong.")
                region.forceHeight = True
                region.currentHeight = 40 #TODO - fix double locked h
                fullyTerminated = False
                break

    print("Geometry calc finished. Evalutating results.")

    lockedHCounter = 0
    for region in regionDB:
        if region.forceHeight:
            lockedHCounter += 1

    print("Computed: ", lockedHCounter,
          "regions successfully: (" + str(round(100 * lockedHCounter / len(regionDB))) + "%).")

    return regionDB




class RefMode:
    NoneAssigned = -1
    Peak = 0
    NeutralDif = 1
    NegativeDif = 2
    PositiveDif = 3

def forceComputeGeometry(regionDB):
    print("\n\n--------------------------")
    print("Found", len(regionDB), "regions. Preparing to compute geometry.")

    unassignedCounter = 0
    for region in regionDB:
        if region.mode == RefMode.NoneAssigned:
            unassignedCounter += 1

    loopedReferenceCounter = 0
    for region in regionDB:
        if region.mode == RefMode.NeutralDif:
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
        if region.mode == RefMode.Peak:
            print("Found peak, preparing to calc geo.")
            foundStartingPoint = True
            region.forceHeight = True
            region.currentHeight = 100 #TODO - max h handling
            break

        if region.forceHeight:
            print("Found specified height, preparing to calc geo.")
            foundStartingPoint = True
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
                ref_region = region.ref_region
                if (not region.forceHeight) and (ref_region is not None) and ref_region.forceHeight:
                    region.forceHeight = True
                    if region.mode == RefMode.NegativeDif:
                        region.currentHeight = ref_region.currentHeight - 5
                        madeChangesLastLoop = True
                    elif region.mode == RefMode.PositiveDif:
                        region.currentHeight = ref_region.currentHeight + 5
                        madeChangesLastLoop = True
                    elif region.mode == RefMode.NeutralDif:
                        print("Error, referencing a region with difference not specified.")
                    elif region.mode == RefMode.Peak:
                        print("Error, peak is attempting to reference a region.")
                    elif region.mode == RefMode.NoneAssigned:
                        print("Error, referencing a region but no mode specified.")
                    else:
                        print("Error, unexpected region code: ", region.mode)
        #endregion
        #Attempt to find new starting points
        fullyTerminated = True
        for region in regionDB:
            if region.mode == RefMode.Peak and not region.forceHeight:
                region.forceHeight = True
                region.currentHeight = 100 #TODO - fix double locked h
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




import ImagePreProcess
import TopoRegionManager
import MeshGrid3D
import DataCompresser
import STLCreator

rawGrid, circles, peaks = ImagePreProcess.process("Data/flipped_map.jpg", False)
meshGrid = TopoRegionManager.process(rawGrid, circles, peaks)
cGrid = DataCompresser.smartCompress(meshGrid, 4)
sGrid = DataCompresser.smooth(cGrid, 3)
MeshGrid3D.graph(sGrid)
STLCreator.stlFromMesh(sGrid, "models/MapDataTest")
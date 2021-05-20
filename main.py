import ImagePreProcess
import TopoRegionManager
import MeshGrid3D
import DataCompresser
import STLCreator

rawGrid, circles, peaks = ImagePreProcess.process("Data/largemap.jpg", False)
meshGrid = TopoRegionManager.process(rawGrid, circles, peaks)
cGrid = DataCompresser.smartCompress(meshGrid, 2)
MeshGrid3D.graph(cGrid)
STLCreator.stlFromMesh(cGrid, "models/MapDataTest")
API_VERSION = 'API_v1.0'
MOD_NAME = 'ThreeDimentionalLastSpot' 

try:
    import utils, events, ui, callbacks, battle
except:
    pass

import SpatialUI
from Math import Matrix, Vector3


BOX_SIZE = 0.01
BOX_POINT_TOP = Vector3(BOX_SIZE, BOX_SIZE, BOX_SIZE)
BOX_POINT_END = Vector3(-BOX_SIZE, -BOX_SIZE, -BOX_SIZE)


class ThreeDimentionalLastSpot(object):
    def __init__(self):
        self.vary = None
        self.meshes = {}
        events.onBattleStart(self.onBattleStart)
        events.onBattleQuit(self.onBattleQuit)
        
    def onBattleStart(self, *args):
        self.meshes = {}
        self.vary = callbacks.perTick(self.update)

    def onBattleQuit(self, *args):
        callbacks.cancel(self.vary)
        self.meshes.clear()
        
    def update(self, *args):
        isMeshVisible = battle.cameraAltVision()
        for ship in battle.getAllShips():
            uiId = ship.uiId

            if not self._isShipValid(ship):
                if uiId in self.meshes:
                    self.meshes.pop(uiId)
                continue

            if uiId in self.meshes:
                mesh = self.meshes[uiId]
            else:
                mesh = self._createMesh()
                self.meshes[uiId] = mesh
            currentPosition = ship.getPosition()
            m = Matrix()
            m.setTranslate(currentPosition)
            SpatialUI.setTransform(mesh, m)
            mesh.visible = isMeshVisible
    
    def _createMesh(self):
        box = SpatialUI.Box(1, SpatialUI.LDR)
        box.setWired(BOX_POINT_END, BOX_POINT_TOP, 0xFFFF0000)
        box.lineWidth = 5
        return box
    
    def _isShipValid(self, ship):
        if not ship.isAlive:
            return False
        if battle.getSelfPlayer().teamId == ship.teamId:
            return False
        return True


matViewer = ThreeDimentionalLastSpot()

import os


class Helper:

    def checkForEndPointNodes(self, root, endPoint):
        for OUTn in range(0, 150, 10):
            if os.path.exists(self.getPath(root, endPoint, OUTn)) == False:
                break
            print("OUT" + str((int)(OUTn / 10)))
        for INn in range(1, 151, 10):
            if os.path.exists(self.getPath(root, endPoint, INn)) == False:
                break
            print("IN" + str((int)(INn / 10)))

    def availableEndpoints(self, root, endPoint):
        if endPoint == Def.CONTROL:
            print("control :")
            self.checkForEndPointNodes(root, endPoint)
        elif endPoint == Def.BULK:
            print("bulk :")
            self.checkForEndPointNodes(root, endPoint)
        elif endPoint == Def.INTERRUPT:
            print("interrupt :")
            self.checkForEndPointNodes(root, endPoint)
        elif endPoint == Def.ISOCHRONOUS:
            print("isochronous:")
            self.checkForEndPointNodes(root, endPoint)

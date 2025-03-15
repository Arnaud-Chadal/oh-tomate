import node

class Automate:

    def __init__(
        self,
        alphabet,
        nodeList,
    ):
        self.alphabet = alphabet
        self.nodeList = nodeList

    def __str__(self):
        string = ""
        for node in self.nodeList:
            string += node.__str__() + "\n"
        return string

    # Méthode de vérification :

    def isMinimized(self):
        pass

    def isStantard(self):
        pass

    def isDetermined(self):
        pass

    def isCompet(self):
        pass

    # Méthodes d'action :

    def toDetermine(self):
        pass

    def toMinimize(self):
        pass

    def toComplete(self):
        varBin = 0
        for nodeVar in self.nodeList :
            if nodeVar.bin :
                varBin = nodeVar
        if varBin == 0 :
            varBin = node.Node("Bin", 0, 0)
            self.nodeList.append(varBin)

        for nodeVar in self.nodeList :
            for letter in self.alphabet :
                linkExists = False
                for link in nodeVar.linkList :
                    if letter == link[0] :
                        linkExists = True
                if not linkExists :
                    nodeVar.linkList.append([letter, varBin])


    def toComplement(self):
        for nodeVar in self.nodeList :
            nodeVar.isLast = not nodeVar.isLast


    def toStandardize(self):
        pass

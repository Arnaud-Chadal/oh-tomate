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
        if(self.nodeList[1].isInit == True):   # If there is more than one initial node
           return False
        for node in self.nodeList:
            for link in node.linkList:
                if link[1].name == self.nodeList[0].name:        # If there is a link to the initial node
                    return False
        return True

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
        pass

    def toComplement(self):
        pass

    def toStandardize(self):
        newNode = node.Node("0", True, False)
        nodeIndex = 0
        while self.nodeList[nodeIndex].isInit == True:
            if self.nodeList[nodeIndex].isLast == True:
                newNode.isLast = True
            for link in self.nodeList[nodeIndex].linkList:
                newNode.addLinkToLinkList(link)
            self.nodeList[nodeIndex].name = str(int(self.nodeList[nodeIndex].name) + 1)
            self.nodeList[nodeIndex].isInit = False
            nodeIndex += 1
        while nodeIndex < len(self.nodeList):
            self.nodeList[nodeIndex].name = str(int(self.nodeList[nodeIndex].name) + 1)
            nodeIndex += 1
        self.nodeList.insert(0, newNode)

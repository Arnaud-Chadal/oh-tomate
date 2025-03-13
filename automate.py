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
        pass

    def toComplement(self):
        pass

    def toStandardize(self):
        pass

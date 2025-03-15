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
        print(self.nodeList)
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
        
        # if not self.isDetermined():
        #     print("Automate not determined !!")
        #     return
        
        partition = [[], []]
        newPartition = [[], []]
        for node in self.nodeList:
            if node.isLast:
                newPartition[0].append(node)
            else:
                newPartition[1].append(node)
        while partition != newPartition:
            partition = []
            for i in newPartition:
                partition.append(i.copy())
            transition = {}
            for group in newPartition:
                for node in group:
                    transition[node] = []
                    for letterNumber in range(len(self.alphabet)):
                        nextNode = None
                        for link in node.linkList:
                            if link[0] == self.alphabet[letterNumber]:
                                nextNode = link[1]
                        for i in range(len(newPartition)):
                            if nextNode in newPartition[i]:
                                transition[node].append(i)

            currentPartition = []
            indexCurrent = 0

            for groupNum in range(len(newPartition)):
                while newPartition[groupNum] != []:
                    node = newPartition[groupNum][0]
                    currentPartition.append([node])
                    newPartition[groupNum].remove(node)
                    transitionNode = transition[node]
                    indexMax = len(newPartition[groupNum])
                    currentIndex = 0
                    while currentIndex < indexMax:
                        otherNode = newPartition[groupNum][currentIndex]
                        if node != otherNode and transition[otherNode] == transitionNode:
                            currentPartition[indexCurrent].append(otherNode)
                            newPartition[groupNum].remove(otherNode)
                            indexMax -= 1
                        else:
                            currentIndex += 1
                    indexCurrent += 1                    
            
            newPartition = []
            for i in currentPartition:
                newPartition.append(i.copy())
            
        for newStateNumber in range(len(partition)):
            for i in range(len(partition[newStateNumber])):
                partition[newStateNumber][i] = partition[newStateNumber][i].getName()
        print(partition)

    def toComplete(self):
        pass

    def toComplement(self):
        pass

    def toStandardize(self):
        pass

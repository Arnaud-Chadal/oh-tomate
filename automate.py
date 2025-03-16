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
        print(self.nodeList)
        for node in self.nodeList:
            string += node.__str__() + "\n"
        return string

    # Méthode de vérification :

    def isMinimized(self):
        pass

    def isStantard(self):
        numberOfInitialNodesIsOk = False
        for node in self.nodeList:
            if node.isInit == True and numberOfInitialNodesIsOk == True:
                return False
            if node.isInit == True:
                numberOfInitialNodesIsOk = True
            for link in node.linkList:
                if link[1].name == self.nodeList[0].name:        # If there is a link to the initial node
                    return False
        return True

    def isDetermined(self):
        numberOfInitStates=0
        alphabetLen=len(self.alphabet)
        for node in self.nodeList:
            transition=[0]*alphabetLen
            if node.isInit:
                numberOfInitStates+=1
                if numberOfInitStates>1:
                   return 0
            numberOfTransitions=len(node.linkList)
            if numberOfTransitions>alphabetLen:
                return 0
            for link in node.linkList:
                insertionPlace=ord(link[0])-97
                transition[insertionPlace]+=1
                if transition[insertionPlace]>1:
                    return 0
        return 1
    

    def isCompet(self):
        pass

    # Méthodes d'action :

    def toDetermine(self):

        shouldWeContinue=0
        alphabetLen=len(self.alphabet)
        oldInit=[]
        newIsLast=0
        transitions=[]
        newTransitions=[]
        transitionPlace=0
        newName=set()
        newNames=[]
        newNodes=[]
        newNodePlace=0
        for nodeObj in self.nodeList:
            if nodeObj.isInit:
                newIsLast=0
                oldInit.append(nodeObj)
                if not(newIsLast) & nodeObj.isLast:
                    newIsLast=1
        newNode=node.Node(str(newNodePlace),1,newIsLast)
        newNodePlace+=1
        newNodes.append(newNode)
        transitions.append([[] for i in range (0,len(self.alphabet))])
        newTransitions.append([set() for i in range (0,len(self.alphabet))])
        transitionPlace+=1

        for initState in oldInit:
            newName.add(str(initState.name))
            for link in initState.linkList:
                transitions[transitionPlace-1][ord(link[0])-97].append(link[1])
                newTransitions[transitionPlace-1][ord(link[0])-97].add(link[1].name)
                shouldWeContinue=1
        newNames.append(newName)
        
        while shouldWeContinue:
            shouldWeContinue=0

            for nodeList in transitions[transitionPlace-1]:
                
                newName=set()
                transitions.append([[] for i in range (0,len(self.alphabet))])
                newTransitions.append([set() for i in range (0,len(self.alphabet))])
                transitionPlace+=1
                for nodeObj in nodeList:
                    newIsLast=0

                    if (not newIsLast) & nodeObj.isLast:
                        newIsLast=1

                    if nodeObj.name not in newName:
                        newName.add(str(nodeObj.name))
                        
                        for link in nodeObj.linkList:  
                            transitions[transitionPlace-1][ord(link[0])-97].append(link[1])
                            newTransitions[transitionPlace-1][ord(link[0])-97].add(link[1].name)
                                
                if newName not in newNames:
                        shouldWeContinue=1
                        newNames.append(newName)
                        newNode=node.Node(str(newNodePlace),0,newIsLast)
                        newNodePlace+=1
                        newNodes.append(newNode)
                else:
                    del transitions[transitionPlace-1]
                    del newTransitions[transitionPlace-1]
                    transitionPlace-=1

        for i in range (0, len(newNames)):
            letter=0

            for newTransition in newTransitions[i]:
                newNodes[i].addLinkToLinkList([self.alphabet[letter],newNodes[newNames.index(newTransition)]])
                letter+=1

        #récupérer newNames
        self.nodeList=newNodes
        
        

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
        newNode = node.Node(str(len(self.nodeList)), True, False)
        for nodeIndex in range(len(self.nodeList)):
            if self.nodeList[nodeIndex].isInit == True and self.nodeList[nodeIndex].isLast == True:
                newNode.isLast = True
            if self.nodeList[nodeIndex].isInit == True:
                for link in self.nodeList[nodeIndex].linkList:
                    if link not in newNode.linkList:
                        newNode.addLinkToLinkList(link)
                self.nodeList[nodeIndex].isInit = False
        self.nodeList.insert(0, newNode)
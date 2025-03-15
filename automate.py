from node import Node
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
        newNode=Node(str(newNodePlace),1,newIsLast)
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
                        newNode=Node(str(newNodePlace),0,newIsLast)
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
        self.nodeList=newNodes
        
        

    def toMinimize(self):
        pass

    def toComplete(self):
        pass

    def toComplement(self):
        pass

    def toStandardize(self):
        pass

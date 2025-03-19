import node
import os


class Automate:

    def __init__(
        self,
        alphabet,
        nodeList,
    ):
        self.alphabet = alphabet
        self.nodeList = nodeList
        self.backupNodeList = [nodeList.copy(), [], [], []]
        self.nodeInitList = []
        self.nodeLastList = []
        for node in self.nodeList:
            if node.isInit:
                self.nodeInitList.append(node)
            if node.isLast:
                self.nodeLastList.append(node)
        self.nodeLastAndInitList = list(set(self.nodeInitList) & set(self.nodeLastList))

    def __str__(self):
        string = ""
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
                if (
                    link[1].name == self.nodeList[0].name
                ):  # If there is a link to the initial node
                    return False
        return True

    def isDetermined(self):
        numberOfInitStates = 0
        alphabetLen = len(self.alphabet)
        for node in self.nodeList:
            transition = [0] * alphabetLen
            if node.isInit:
                numberOfInitStates += 1
                if numberOfInitStates > 1:
                    return 0
            numberOfTransitions = len(node.linkList)
            if numberOfTransitions > alphabetLen:
                return 0
            for link in node.linkList:
                insertionPlace = ord(link[0]) - 97
                transition[insertionPlace] += 1
                if transition[insertionPlace] > 1:
                    return 0
        return 1

    def isCompet(self):
        pass

    # Méthodes d'action :

    def toDetermine(self):

        shouldWeContinue = 0
        alphabetLen = len(self.alphabet)
        oldInit = []
        newIsLast = 0
        transitions = []
        newTransitions = []
        transitionPlaceToInsert = 0
        newName = set()
        newNames = []
        newNodes = []
        newNodePlace = 0
        for nodeObj in self.nodeList:
            if nodeObj.isInit:
                oldInit.append(nodeObj)
                if not (newIsLast) and nodeObj.isLast:
                    newIsLast = 1
        newNode = node.Node(str(newNodePlace), 1, newIsLast)
        newNodePlace += 1
        newNodes.append(newNode)
        transitions.append([[] for i in range(0, len(self.alphabet))])
        newTransitions.append([set() for i in range(0, len(self.alphabet))])
        transitionPlaceToInsert += 1

        for initState in oldInit:
            newName.add(str(initState.name))
            for link in initState.linkList:
                transitions[transitionPlaceToInsert - 1][ord(link[0]) - 97].append(
                    link[1]
                )
                newTransitions[transitionPlaceToInsert - 1][ord(link[0]) - 97].add(
                    link[1].name
                )
                shouldWeContinue = 1
        if newNames != set():
            newNames.append(newName)
        transitionPlaceToRead = 0
        while shouldWeContinue:

            shouldWeContinue = 0
            for nodeList in transitions[transitionPlaceToRead]:
                newIsLast = 0
                newName = set()
                transitions.append([[] for i in range(0, len(self.alphabet))])
                newTransitions.append([set() for i in range(0, len(self.alphabet))])
                transitionPlaceToInsert += 1
                for nodeObj in nodeList:
                    if (not newIsLast) and nodeObj.isLast:
                        newIsLast = 1

                    if nodeObj.name not in newName:
                        newName.add(str(nodeObj.name))

                        for link in nodeObj.linkList:
                            transitions[transitionPlaceToInsert - 1][
                                ord(link[0]) - 97
                            ].append(link[1])
                            newTransitions[transitionPlaceToInsert - 1][
                                ord(link[0]) - 97
                            ].add(link[1].name)

                if (newName not in newNames) and (newName != set()):
                    shouldWeContinue = 1
                    newNames.append(newName)
                    newNode = node.Node(str(newNodePlace), 0, newIsLast)
                    newNodePlace += 1
                    newNodes.append(newNode)
                else:
                    del transitions[transitionPlaceToInsert - 1]
                    del newTransitions[transitionPlaceToInsert - 1]
                    transitionPlaceToInsert -= 1
            transitionPlaceToRead += 1

        for i in range(0, len(newNames)):
            letter = 0

            for newTransition in newTransitions[i]:
                if len(newTransition) != 0:
                    newNodes[i].addLinkToLinkList(
                        [self.alphabet[letter], newNodes[newNames.index(newTransition)]]
                    )
                letter += 1

        # récupérer newNames
        self.nodeList = newNodes.copy()

        self.nodeInitList = []
        self.nodeLastList = []
        for n in self.nodeList:
            if n.isInit:
                self.nodeInitList.append(n)
            if n.isLast:
                self.nodeLastList.append(n)
        self.nodeLastAndInitList = list(set(self.nodeInitList) & set(self.nodeLastList))
        self.backupNodeList[1] = newNames

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
                    print(transitionNode)
                    indexMax = len(newPartition[groupNum])
                    currentIndex = 0
                    while currentIndex < indexMax:
                        otherNode = newPartition[groupNum][currentIndex]
                        if (
                            node != otherNode
                            and transition[otherNode] == transitionNode
                        ):
                            currentPartition[indexCurrent].append(otherNode)
                            newPartition[groupNum].remove(otherNode)
                            indexMax -= 1
                        else:
                            currentIndex += 1
                    indexCurrent += 1
            print(transition)

            newPartition = []
            for i in currentPartition:
                newPartition.append(i.copy())

        for newStateNumber in range(len(partition)):
            for i in range(len(partition[newStateNumber])):
                partition[newStateNumber][i] = partition[newStateNumber][i].getName()
        print(partition)
        self.backupNodeList[3] = partition
        newNode = []
        newNodeDico = {}
        import node

        for groupNum in range(len(newPartition)):
            n = node.Node(
                newPartition[groupNum][0].getName(),
                newPartition[groupNum][0].isInit,
                newPartition[groupNum][0].isLast,
            )
            newNode.append(n)
            newNodeDico[n] = partition[groupNum]
        automateNameToObject = {}
        for i in self.nodeList:
            automateNameToObject[i.getName()] = transition[i]
        for n in newNode:
            for linkNum in range(len(automateNameToObject[n.getName()])):
                for key, val in newNodeDico.items():
                    if partition[automateNameToObject[n.getName()][linkNum]] == val:
                        n.addLinkToLinkList([self.alphabet[linkNum], key])

        self.nodeList = newNode.copy()

    def toComplete(self):
        varBin = 0
        for nodeVar in self.nodeList:
            if nodeVar.bin:
                varBin = nodeVar
        if varBin == 0:
            varBin = node.Node("Bin", 0, 0)
            varBin.bin = True
            self.nodeList.append(varBin)
            print(self.backupNodeList)
            if self.backupNodeList[1] == []:
                self.backupNodeList[2] = self.backupNodeList[0].copy()
            else:
                self.backupNodeList[2] = self.backupNodeList[1].copy()
            self.backupNodeList[2].append("Bin")

        for nodeVar in self.nodeList:
            for letter in self.alphabet:
                linkExists = False
                for link in nodeVar.linkList:
                    if letter == link[0]:
                        linkExists = True
                if not linkExists:
                    nodeVar.linkList.append([letter, varBin])

    def toComplement(self):
        for nodeVar in self.nodeList:
            nodeVar.isLast = not nodeVar.isLast

    def toStandardize(self):
        newNode = node.Node(str(len(self.nodeList)), True, False)
        for nodeIndex in range(len(self.nodeList)):
            if (
                self.nodeList[nodeIndex].isInit == True
                and self.nodeList[nodeIndex].isLast == True
            ):
                newNode.isLast = True
            if self.nodeList[nodeIndex].isInit == True:
                for link in self.nodeList[nodeIndex].linkList:
                    if link not in newNode.linkList:
                        newNode.addLinkToLinkList(link)
                self.nodeList[nodeIndex].isInit = False
        self.nodeList.insert(0, newNode)

    def saveToFile(self, fileName):
        numberOfInitialStates = 0
        numberOfFinalStates = 0
        numberOfInitialAndFinalStates = 0
        thereIsABin = False
        for node in self.nodeList:
            if node.isInit and not node.isLast:
                numberOfInitialStates += 1
            elif node.isInit:
                numberOfInitialAndFinalStates += 1
            elif node.isLast:
                numberOfFinalStates += 1
            if node.bin:
                thereIsABin = True

        filePath = "./automates/" + fileName + ".txt"
        if os.path.exists(filePath):
            return False
        file = open(filePath, "w")
        file.write(str(len(self.alphabet)) + "\n")
        file.write(str(numberOfInitialStates) + "\n")
        if numberOfInitialStates > 0:
            for node in self.nodeList:
                if node.isInit and not node.isLast:
                    line = node.getName() + ";"
                    for link in node.linkList:
                        line += link[0] + "/" + link[1].getName() + ","
                    line = line.rstrip(",")
                    file.write(line + "\n")
        file.write(str(numberOfFinalStates) + "\n")
        if numberOfFinalStates > 0:
            for node in self.nodeList:
                if node.isLast and not node.isInit:
                    line = node.getName() + ";"
                    for link in node.linkList:
                        line += link[0] + "/" + link[1].getName() + ","
                    line = line.rstrip(",")
                    file.write(line + "\n")
        file.write(str(numberOfInitialAndFinalStates) + "\n")
        if numberOfInitialAndFinalStates > 0:
            for node in self.nodeList:
                if node.isInit and node.isLast:
                    line = node.getName() + ";"
                    for link in node.linkList:
                        line += link[0] + "/" + link[1].getName() + ","
                    line = line.rstrip(",")
                    file.write(line + "\n")
        file.write(str(int(thereIsABin)) + "\n")
        if thereIsABin:
            for node in self.nodeList:
                if node.bin:
                    line = node.getName() + ";"
                    for link in node.linkList:
                        line += link[0] + "/" + link[1].getName() + ","
                    line = line.rstrip(",")
                    file.write(line + "\n")
        file.write(
            str(
                len(self.nodeList)
                - numberOfInitialStates
                - numberOfFinalStates
                - numberOfInitialAndFinalStates
                - int(thereIsABin)
            )
            + "\n"
        )
        if (
            len(self.nodeList)
            - numberOfInitialStates
            - numberOfFinalStates
            - numberOfInitialAndFinalStates
            - int(thereIsABin)
            > 0
        ):
            for node in self.nodeList:
                if not node.isInit and not node.isLast and not node.bin:
                    line = node.getName() + ";"
                    for link in node.linkList:
                        line += link[0] + "/" + link[1].getName() + ","
                    line = line.rstrip(",")
                    file.write(line + "\n")
        file.close()

    def recognize(self, word: str) -> bool:
        if not self.isDetermined():
            self.toDetermine()
        for c in word:
            if c not in self.alphabet:
                print("Not same alphabet")
                return False
        wordCopy = word
        node = self.nodeInitList[0]
        cont = True
        while len(wordCopy) > 0 and cont:
            cont = False
            for transitions in node.linkList:
                if transitions[0] == wordCopy[0]:
                    cont = True
                    wordCopy = wordCopy[1:]
                    node = transitions[1]
                    break
        if len(wordCopy) == 0 and node.isLast:
            return True
        return False

    def printTransitionTables(self):
        stringTabReturn = [[], [], [], []]
        string = "========= Initial Nodes =========\t"
        stringTabReturn[0].append("========= Initial Nodes =========")
        if self.backupNodeList[1] != []:
            string += (
                "========= [Previous array Nodes] -> New Determined node =========\t"
            )
            
            stringTabReturn[1].append((
                "========= [Previous array Nodes] -> New Determined node ========="
            ))
        if self.backupNodeList[2] != []:
            string += "========= [Previous Array Nodes] -> Complete node =========\t"
            stringTabReturn[2].append((
                "========= [Previous Array Nodes] -> Complete node ========="
            ))
        if self.backupNodeList[3] != []:
            string += (
                "========= [Previous Array Nodes] -> New Minimized node =========\t"
            )
            stringTabReturn[3].append((
                "========= [Previous Array Nodes] -> New Minimized node ========="
            ))
        string += "\n"

        lenInitial = len(self.backupNodeList[0])
        lenDetermined = len(self.backupNodeList[1])
        lenComplete = len(self.backupNodeList[2])
        lenMinimized = len(self.backupNodeList[3])

        for nIndex in range(max(lenInitial, lenDetermined, lenMinimized, lenComplete)):
            if nIndex < lenInitial:
                string += f"{self.backupNodeList[0][nIndex].getName()}\t".center(35)
                stringTabReturn[0].append(f"{self.backupNodeList[0][nIndex].getName()}".center(35))
            else:
                string += " \t".center(35)
            if nIndex < lenDetermined:
                string += f"{self.backupNodeList[1][nIndex]} -> {nIndex}\t".center(58)
                stringTabReturn[1].append(f"{self.backupNodeList[1][nIndex]} -> {nIndex}".center(58))
            elif lenDetermined != 0:
                string += "\t\t\t".center(58)
            if lenDetermined == 0:
                if nIndex < lenComplete:
                    if self.backupNodeList[2][nIndex] != "Bin":
                        string += (
                            f"{self.backupNodeList[2][nIndex].getName()}\t".center(58)
                        )
                        stringTabReturn[2].append(f"{self.backupNodeList[2][nIndex].getName()}".center(58))
                    else:
                        string += f"{self.backupNodeList[2][nIndex]}\t".center(58)
                        stringTabReturn[2].append(f"{self.backupNodeList[2][nIndex]}".center(58))
                elif lenComplete != 0:
                    string += "\t\t\t".center(58)
            else:
                if nIndex < lenComplete:
                    if self.backupNodeList[2][nIndex] != "Bin":
                        string += (
                            f"{self.backupNodeList[2][nIndex]} -> {nIndex}\t".center(58)
                        )
                        stringTabReturn[2].append(f"{self.backupNodeList[2][nIndex]} -> {nIndex}".center(58))
                    else:
                        string += f"{self.backupNodeList[2][nIndex]}\t".center(58)
                        stringTabReturn[2].append(f"{self.backupNodeList[2][nIndex]}".center(58))
                elif lenComplete != 0:
                    string += "\t\t\t".center(58)
            if nIndex < lenMinimized:
                string += f"{self.backupNodeList[3][nIndex]} -> {self.nodeList[nIndex].getName()}\t".center(
                    63
                )
                stringTabReturn[3].append(f"{self.backupNodeList[3][nIndex]} -> {self.nodeList[nIndex].getName()}".center(63))
            string += "\n"
        return stringTabReturn

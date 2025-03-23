import node
import os


class Automate:

    def __init__(
        self,
        alphabet,
        nodeList,
        isAsynchronous,
    ):
        self.alphabet = alphabet
        self.nodeList = nodeList
        self.backupNodeList = [nodeList.copy(), [], [], []]
        self.nodeInitList = []
        self.nodeLastList = []
        self.isAsynchronous = isAsynchronous

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
        if self.isAsynchronous:
            return False
        numberOfInitStates = 0
        alphabetLen = len(self.alphabet)
        for node in self.nodeList:
            transition = [0] * alphabetLen
            if node.isInit:
                numberOfInitStates += 1
                if numberOfInitStates > 1:
                    return False
            numberOfTransitions = len(node.linkList)
            if numberOfTransitions > alphabetLen:
                return False
            for link in node.linkList:
                if link[0] == "&":
                    return False
                insertionPlace = ord(link[0]) - 97
                transition[insertionPlace] += 1
                if transition[insertionPlace] > 1:
                    return False
        return True

    def isComplet(self):
        if not self.isDetermined:
            return False
        for node in self.nodeList:
            toGet = len(self.alphabet)
            for link in node.linkList:
                toGet -= 1
            if toGet > 0:
                return False
        return True

    # Méthodes d'action :

    def removeEpsilonMove(self):
        closureToProcess = set()
        linkFromClosureToProcess = []
        newNames = {}

        newLink = []
        newIsLast = 0
        newIsInit = 0
        newNodePlace = 0
        newNodes = []
        for nodeObj in self.nodeList:
            if nodeObj.isInit:
                closureToProcess.add(nodeObj)
                continue
            for link in nodeObj.linkList:
                if link[0] in self.alphabet:
                    closureToProcess.add(link[1])
        for ele in closureToProcess:
            newIsLast = 0
            newIsInit = 0
            newLink = []
            newName = set()
            newName.add(ele.name)
            if ele.isLast:
                newIsLast = 1
            if ele.isInit:
                newIsInit = 1
            for link in ele.linkList:
                if link[0] == "&" and (link[1].name not in newName):
                    if link[1].isInit:
                        newIsInit = 1
                    if link[1].isLast:
                        newIsLast = 1
                    newName.add(link[1].name)
                    linkFromClosureToProcess.append(link[1])
                if link[0] in self.alphabet:
                    if link[1].isInit:
                        newIsInit = 1
                    if link[1].isLast:
                        newIsLast = 1
                    newLink.append([link[0], link[1]])
            while linkFromClosureToProcess:

                for linkToProcess in linkFromClosureToProcess[0].linkList:
                    # print('ici:',linkToProcess[1].name)
                    # print(linkToProcess[0])
                    if (not newIsInit) and (linkToProcess[1].isInit):
                        newIsInit = 1
                    if (not newIsLast) and (linkToProcess[1].isLast):
                        newIsLast = 1
                    if linkToProcess[0] == "&" and (
                        linkToProcess[1].name not in newName
                    ):
                        # print("ici &")
                        newName.add(linkToProcess[1].name)
                        linkFromClosureToProcess.append(linkToProcess[1])
                    if linkToProcess[0] in self.alphabet:
                        # print("ici alpha")
                        newLink.append([linkToProcess[0], linkToProcess[1]])
                del linkFromClosureToProcess[0]
            newNames[ele.name] = newName

            newNode = node.Node(str(ele.name), newIsInit, newIsLast)
            newNode.linkList = newLink
            newNodePlace += 1
            newNodes.append(newNode)
        newNamesIdxMap = {key: i for i, key in enumerate(newNames)}

        for myNewNode in newNodes:
            for link in myNewNode.linkList:
                link[1] = newNodes[newNamesIdxMap.get(link[1].name)]
        self.nodeList = newNodes.copy()
        self.nodeInitList = []
        self.nodeLastList = []
        for n in self.nodeList:
            if n.isInit:
                self.nodeInitList.append(n)
            if n.isLast:
                self.nodeLastList.append(n)
        self.nodeLastAndInitList = list(set(self.nodeInitList) & set(self.nodeLastList))
        self.isAsynchronous = 0
        print(self)

    def toDetermine(self):

        numberOfNewNode = 0
        nodeNewName = set()

        translationTable = []
        oldNodesToProcess = []

        automateNewStructure = []
        idxToInvestigate = 0

        # Étape 1 : rendre l'automate synchrone
        if self.isAsynchronous:
            self.removeEpsilonMove()

        # Étape 2 : constituer le nouvel état initial et récupérer les transitions à inspecter
        oldNodesToProcess.append(set())
        for nodeObj in self.nodeInitList:
            nodeNewName.add(nodeObj.name)
            oldNodesToProcess[0].add(nodeObj)
        translationTable.append(nodeNewName)
        if self.nodeLastAndInitList:
            automateNewStructure.append(node.Node(str(numberOfNewNode), 1, 1))
        else:
            automateNewStructure.append(node.Node(str(numberOfNewNode), 1, 0))
        numberOfNewNode += 1

        # Étape 3 : Parcourir les liens pour créer les nouveaux états
        while idxToInvestigate < numberOfNewNode:
            newName = [set() for i in range(0, len(self.alphabet))]
            eleForOldNodesToProcess = [
                [0, set(), False] for i in range(0, len(self.alphabet))
            ]

            for oldNode in oldNodesToProcess[idxToInvestigate]:
                for link in oldNode.linkList:
                    if (
                        eleForOldNodesToProcess[ord(link[0]) - 97][0] == 0
                        and link[1].isLast
                    ):
                        eleForOldNodesToProcess[ord(link[0]) - 97][0] = 1
                    if link[1].bin:
                        eleForOldNodesToProcess[ord(link[0]) - 97][2] = True
                    newName[ord(link[0]) - 97].add(link[1].name)
                    eleForOldNodesToProcess[ord(link[0]) - 97][1].add(link[1])

            for namePlaceInAlpha in range(0, len(self.alphabet)):
                if (
                    newName[namePlaceInAlpha] != set()
                    and newName[namePlaceInAlpha] not in translationTable
                ):
                    translationTable.append(newName[namePlaceInAlpha])
                    newNode = node.Node(
                        str(numberOfNewNode),
                        0,
                        eleForOldNodesToProcess[namePlaceInAlpha][0],
                    )
                    if eleForOldNodesToProcess[namePlaceInAlpha][2] == True:
                        newNode.bin = True
                        newNode.name = "P"
                    oldNodesToProcess.append(
                        eleForOldNodesToProcess[namePlaceInAlpha][1]
                    )
                    automateNewStructure.append(newNode)
                    automateNewStructure[idxToInvestigate].addLinkToLinkList(
                        [self.alphabet[namePlaceInAlpha], newNode]
                    )
                    numberOfNewNode += 1
                elif newName[namePlaceInAlpha] in translationTable:
                    automateNewStructure[idxToInvestigate].addLinkToLinkList(
                        [
                            self.alphabet[namePlaceInAlpha],
                            automateNewStructure[
                                translationTable.index(newName[namePlaceInAlpha])
                            ],
                        ]
                    )

            idxToInvestigate += 1

        self.nodeList = automateNewStructure.copy()

        self.updateInitAndLastNodeList()
        self.backupNodeList[1] = translationTable

    def updateInitAndLastNodeList(self):
        self.nodeInitList = []
        self.nodeLastList = []
        for n in self.nodeList:
            if n.isInit:
                self.nodeInitList.append(n)
            if n.isLast:
                self.nodeLastList.append(n)
        self.nodeLastAndInitList = list(set(self.nodeInitList) & set(self.nodeLastList))

    def toMinimize(self):
        if not self.isComplet():
            return False
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
            n.bin = newPartition[groupNum][0].bin
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
        return True

    def toComplete(self):
        if not self.isDetermined():
            return False
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
        return True

    def toComplement(self):
        if not self.isComplet():
            return False
        for nodeVar in self.nodeList:
            nodeVar.isLast = not nodeVar.isLast
        self.updateInitAndLastNodeList()
        return True

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

    def saveToFile(self, fileName, graphicNodeTab):
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
        if len(fileName) > 5 and fileName[len(fileName) - 4 :] == ".txt":
            filePath = "./automates/" + fileName
            dataPath = "./automates/" + fileName[: len(fileName) - 4] + ".data"
        else:
            filePath = "./automates/" + fileName + ".txt"
            dataPath = "./automates/" + fileName + ".data"
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
        dataFile = open(dataPath, "w")
        for graphicNode in graphicNodeTab:
            dataFile.write(
                str(graphicNode.nodeVar.name)
                + "("
                + str(graphicNode.x)
                + ","
                + str(graphicNode.y)
                + ")\n"
            )
        dataFile.close()

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

            stringTabReturn[1].append(
                ("========= [Previous array Nodes] -> New Determined node =========")
            )
        if self.backupNodeList[2] != []:
            string += "========= [Previous Array Nodes] -> Complete node =========\t"
            stringTabReturn[2].append(
                ("========= [Previous Array Nodes] -> Complete node =========")
            )
        if self.backupNodeList[3] != []:
            string += (
                "========= [Previous Array Nodes] -> New Minimized node =========\t"
            )
            stringTabReturn[3].append(
                ("========= [Previous Array Nodes] -> New Minimized node =========")
            )
        string += "\n"

        lenInitial = len(self.backupNodeList[0])
        lenDetermined = len(self.backupNodeList[1])
        lenComplete = len(self.backupNodeList[2])
        lenMinimized = len(self.backupNodeList[3])

        for nIndex in range(max(lenInitial, lenDetermined, lenMinimized, lenComplete)):
            if nIndex < lenInitial:
                string += f"{self.backupNodeList[0][nIndex].getName()}\t".center(35)
                stringTabReturn[0].append(
                    f"{self.backupNodeList[0][nIndex].getName()}".center(35)
                )
            else:
                string += " \t".center(35)
            if nIndex < lenDetermined:
                string += f"{self.backupNodeList[1][nIndex]} -> {nIndex}\t".center(58)
                stringTabReturn[1].append(
                    f"{self.backupNodeList[1][nIndex]} -> {nIndex}".center(58)
                )
            elif lenDetermined != 0:
                string += "\t\t\t".center(58)
            if lenDetermined == 0:
                if nIndex < lenComplete:
                    if self.backupNodeList[2][nIndex] != "Bin":
                        string += (
                            f"{self.backupNodeList[2][nIndex].getName()}\t".center(58)
                        )
                        stringTabReturn[2].append(
                            f"{self.backupNodeList[2][nIndex].getName()}".center(58)
                        )
                    else:
                        string += f"{self.backupNodeList[2][nIndex]}\t".center(58)
                        stringTabReturn[2].append(
                            f"{self.backupNodeList[2][nIndex]}".center(58)
                        )
                elif lenComplete != 0:
                    string += "\t\t\t".center(58)
            else:
                if nIndex < lenComplete:
                    if self.backupNodeList[2][nIndex] != "Bin":
                        string += (
                            f"{self.backupNodeList[2][nIndex]} -> {nIndex}\t".center(58)
                        )
                        stringTabReturn[2].append(
                            f"{self.backupNodeList[2][nIndex]} -> {nIndex}".center(58)
                        )
                    else:
                        string += f"{self.backupNodeList[2][nIndex]}\t".center(58)
                        stringTabReturn[2].append(
                            f"{self.backupNodeList[2][nIndex]}".center(58)
                        )
                elif lenComplete != 0:
                    string += "\t\t\t".center(58)
            if nIndex < lenMinimized:
                string += f"{self.backupNodeList[3][nIndex]} -> {self.nodeList[nIndex].getName()}\t".center(
                    63
                )
                stringTabReturn[3].append(
                    f"{self.backupNodeList[3][nIndex]} -> {self.nodeList[nIndex].getName()}".center(
                        63
                    )
                )
            string += "\n"
        return stringTabReturn

import node
import automate
import graphicWindow
import mainMenu

file = open("./automates/automateTest35.txt", "r")
fullAlphabet = "abcdefghijklmnopqrstuvwxyz"
fileLines = []
isAsynchronous = False
for line in file:
    fileLines.append(line.rstrip())
    if (not isAsynchronous) and "&" in line:
        isAsynchronous = True

alphabet = [fullAlphabet[i] for i in range(int(fileLines[0]))]
allautos = [[], [], [], [], []]

# EXTRACTION DES AUTOS DEPUIS LE FICHIER TXT
counter = 0
index = -1
for line in fileLines[1:]:
    if counter == 0:
        index += 1
        counter = int(line)
    else:
        allautos[index].append(line)
        counter -= 1

automateNameToObject = {}

# SPLIT DES AUTOS
for groupOfautos in allautos:
    for autoNumber in range(len(groupOfautos)):
        groupOfautos[autoNumber] = groupOfautos[autoNumber].split(";")
        if len(groupOfautos[autoNumber]) == 1:
            groupOfautos[autoNumber].append([])
        elif len(groupOfautos[autoNumber]) == 2:
            groupOfautos[autoNumber][1] = groupOfautos[autoNumber][1].split(",")
            numberOfTransitions = len(groupOfautos[autoNumber][1])
            for transitionNumber in range(numberOfTransitions):
                groupOfautos[autoNumber][1][transitionNumber] = groupOfautos[
                    autoNumber
                ][1][transitionNumber].split("/")

nodeTab = []
for groupNumber in range(len(allautos)):
    for auto in allautos[groupNumber]:
        isAlreadyHere = False
        newNode = node.Node(auto[0], False, False)
        if groupNumber == 0:
            newNode.isInit = True
            nodeTab.append(newNode)
        if groupNumber == 1:
            newNode.isLast = True
            nodeTab.append(newNode)
        if groupNumber == 2:
            newNode.isInit = newNode.isLast = True
            nodeTab.append(newNode)
        if groupNumber == 3:
            for n in nodeTab:
                if auto[0] == n.getName():
                    isAlreadyHere = True
                    n.setBin(True)
            if isAlreadyHere == False:
                newNode.bin = True
                nodeTab.append(newNode)
        if groupNumber == 4:
            nodeTab.append(newNode)
        if not isAlreadyHere:
            automateNameToObject[auto[0]] = newNode

for group in allautos:
    for auto in group:
        currentNode = automateNameToObject[auto[0]]
        for link in auto[1]:
            currentNode.addLinkToLinkList([link[0], automateNameToObject[link[1]]])

firstauto = automate.Automate(alphabet, nodeTab, isAsynchronous)
print(firstauto)
deterministe = firstauto.isDetermined()
if deterministe:
    print("automate déterministe")
else:
    print("automate non déterministe")
mainMenu.Main().run()
print("\n=======================\n")
# print(firstauto.isStantard())
# firstauto.toStandardize()
# print(firstauto)
# print("\n=======================\n")
deterministe = firstauto.isDetermined()
if deterministe:
    print("automate déterministe")
else:
    print("automate non déterministe")

firstauto.toDetermine()
# print(firstauto)

firstauto.toDetermine

if firstauto.isComplet:
    print("complet")
else:
    print("pas complet")

firstauto.toComplete()
if firstauto.isComplet:
    print("complet")
else:
    print("pas complet")
# firstauto.toMinimize()
# print(firstauto)
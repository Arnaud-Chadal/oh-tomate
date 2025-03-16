class Node:
    def __init__(self, name: str, init: bool, last: bool):
        self.name = name
        self.isInit = init
        self.isLast = last
        self.bin = False
        self.linkList = []

    def __str__(self):
        string = f"{self.name} -- Initial : {self.isInit} \t Final : {self.isLast} \t Poubelle : {self.bin}\n"
        for link in self.linkList:
            string += self.name + " ---- " + link[0] + " ---> " + link[1].name + "\n"
        return string

    def addLinkToLinkList(self, newLink: list):
        self.linkList.append(newLink)

    def setBin(self, bin: bool):
        self.bin = bin

    def getName(self):
        return self.name

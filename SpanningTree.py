class Switch():
    def __init__(self,id):
        self.port =1
        self.id=id
        self.root=id
        self.neighbors =list()
        self.hubsToRoot =0
        self.packetsBuffer =list()
    def updatePortCounter(self):
        self.port+=1
    def resetPortCounter(self):
        self.port=1
        
DROPPED_PORT = -1
switchesTests = list()
with open("input.txt") as myFile:
    for line in myFile:
        switchesTests.append(line)

def eachTestComponent(testNumber,testsList):
    myTest = testsList[testNumber]
    numOFswitches = int(myTest[0])
    print("Solution of problem #{}\nThe number of Switches {}".format(testNumber,numOFswitches))
    print("Input: {}".format(myTest))
    if myTest[2] == "R":
        print("Random Implementation")
        #connectionList = randomTestBuilder()
        pass
    else:
        connections = myTest[2:].split()
        connectionsInTuples = [tuple( map(int,pair.split("-")) ) for pair  in connections]
    return numOFswitches,connectionsInTuples

def randomTestBuilder():
    pass


def buildSwitches(amount):
    switchObjects= dict()
    for i in range(1,amount+1):
        switchObjects[i]=Switch(i)
    return switchObjects   

def buildSwitchesConnections(switches,connectionsToBeMade):
    for leftSwitch,rightSwitch in connectionsToBeMade:
        switchA = switches[leftSwitch]
        switchB = switches[rightSwitch] 
        switchA.neighbors.append(tuple((switchB.port,switchB)))
        print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(switchA.id,switchA.port,switchB.id,switchB.port))
        switchB.updatePortCounter()
        switchB.neighbors.append(tuple((switchA.port,switchA)))
        switchA.updatePortCounter()
        
def broadcasting(switchesMap):
    myswitches = switchesMap.values()
    for senderSwitch in myswitches:
        senderSwitch.resetPortCounter()
        for neighbor in senderSwitch.neighbors:
            neighborPort = neighbor[0]
            currentNeighbor = neighbor[1]
            senderPort = senderSwitch.port
            packet =[senderSwitch.id,senderSwitch.root,senderSwitch.hubsToRoot,senderPort,neighborPort]
            if currentNeighbor == DROPPED_PORT:
                continue
            else:
                currentNeighbor.packetsBuffer.append(tuple(packet))
            senderSwitch.updatePortCounter()
                

def receiving(round,switchesMap):
    myswitches = switchesMap.values()
    for receiverSwitch in myswitches:
        processedSwitchesIPs =list()
        receiverPackets = receiverSwitch.packetsBuffer[:]
        for (senderId,senderRoot,SenderNumHubs,senderPort,receiverPort) in receiverPackets:
            if round ==1:
                if senderId in processedSwitchesIPs:
                    receiverSwitch.neighbors[receiverPort-1]=DROPPED_PORT
                    switchesMap[senderId].neighbors[senderPort-1]=DROPPED_PORT
                    del(switchesMap[senderId].packetsBuffer[senderPort-1])
                else:
                    processedSwitchesIPs.append(senderId)
            if senderRoot < receiverSwitch.root:
                receiverSwitch.root = senderRoot
                receiverSwitch.hubsToRoot = SenderNumHubs+1
            receiverSwitch.packetsBuffer.remove((senderId,senderRoot,SenderNumHubs,senderPort,receiverPort))

def printSwitchesStates(switches):
    myswitches = switches.values()
    for switch in myswitches:
        switch.resetPortCounter()
        for neighbor in switch.neighbors:
            if neighbor==-1:
                switch.updatePortCounter()
                continue
            else:
                print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(switch.id,switch.port,neighbor[1].id,neighbor[0]))
            switch.updatePortCounter()

def printStatus(switches):
    for switch in myswitches.values():
        print("SwitchId {} sends--> {} {} {}".format(switch.id,switch.id,switch.root,switch.hubsToRoot))




numberOFswitches,connectionsbetweenSwitches = eachTestComponent(1,switchesTests)
myswitches = buildSwitches(numberOFswitches)
print("Printing Initial Connections")
print("*"*70)
buildSwitchesConnections(myswitches,connectionsbetweenSwitches)
sameRootAll =False
print("*"*70)
print("Initial Status of Switches")
print("*"*30)
printStatus(myswitches)
print("*"*30)
loopCounter=1
minRoot = min(myswitches.keys())
while(sameRootAll==False):
    print("Loop {}".format(loopCounter))
    print("*"*20)
    print("Status of switches")
    print("*"*30)
    broadcasting(myswitches) 
    receiving(loopCounter,myswitches)
    printStatus(myswitches)
    print("*"*30)
    loopCounter+=1
    for switch in myswitches.values():
        if switch.root!=minRoot:
            break
    else:
        sameRootAll=True
print("Printing Final Connections")
print("*"*70)
printSwitchesStates(myswitches)

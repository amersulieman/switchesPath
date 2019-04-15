class Switch():
    def __init__(self,id):
        self.id=id
        self.root=id
        self.neighbors =list()
        self.hubsToRoot =0
        self.packetsBuffer =list()

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
    ports = dict()
    for switch in switches:
        ports[switch]=[]
    for leftSwitch,rightSwitch in connectionsToBeMade:
        switchA = switches[leftSwitch]
        switchB = switches[rightSwitch] 
        switchA.neighbors.append(switchB)
        ports[switchA.id].append(len(ports[switchA.id])+1)
        switchB.neighbors.append(switchA)
        ports[switchB.id].append(len(ports[switchB.id])+1)    
    for leftSwitch,rightSwitch in connectionsToBeMade:
       print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(leftSwitch,ports[leftSwitch].pop(0),rightSwitch,ports[rightSwitch].pop(0)))


def broadcasting(switchesMap):
    myswitches = switchesMap.values()
    for senderSwitch in myswitches:
        for neighborIndex in range(0,len(senderSwitch.neighbors)):
            currentNeighbor = senderSwitch.neighbors[neighborIndex]
            neighborPort = neighborIndex+1
            senderSwitchPacket =[senderSwitch.id,senderSwitch.root,senderSwitch.hubsToRoot,neighborPort]
            if currentNeighbor == DROPPED_PORT:
                continue
            else:
                currentNeighbor.packetsBuffer.append(tuple(senderSwitchPacket))
                

def receiving(round,switchesMap):
    myswitches = switchesMap.values()
    for receiverSwitch in myswitches:
        processedSwitchesIPs =list()
        senderSwitchIndex = 0
        receiverPackets = receiverSwitch.packetsBuffer[:]
        for (senderId,senderRoot,SenderNumHubs,senderPort) in receiverPackets:
            if round ==1:
                if senderId in processedSwitchesIPs:
                    receiverSwitch.neighbors[senderSwitchIndex]=DROPPED_PORT
                    switchesMap[senderId].neighbors[senderPort-1]=DROPPED_PORT
                    del(switchesMap[senderId].packetsBuffer[senderPort-1])
                else:
                    processedSwitchesIPs.append(senderId)
            if senderRoot < receiverSwitch.root:
                receiverSwitch.root = senderRoot
                receiverSwitch.hubsToRoot = SenderNumHubs+1
            senderSwitchIndex+=1
            receiverSwitch.packetsBuffer.remove((senderId,senderRoot,SenderNumHubs,senderPort))
def printSwitchesStates(switches):
    myswitches = switches.values()
    for switch in myswitches:
        portCounter =1
        for neighbor in switch.neighbors:
            print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(switch.id,portCounter,neighbor.id,"fix"))
            portCounter+=1

def printStatus(switches):
    for switch in myswitches.values():
        print("SwitchId {} sends--> {} {} {}".format(switch.id,switch.id,switch.root,switch.hubsToRoot))


numberOFswitches,connectionsbetweenSwitches = eachTestComponent(2,switchesTests)
myswitches = buildSwitches(numberOFswitches)
print("Printing Initial Connections")
print("*"*70)
buildSwitchesConnections(myswitches,connectionsbetweenSwitches)
sameRootAll =False
#printSwitchesStates(myswitches)
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



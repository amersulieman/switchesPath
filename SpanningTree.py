'''
    @author Amer Sulieman
    @version 04/10/2019
    @description A program that determines min spanning tree for switches 
                to connect with each other without loops when sending packets
'''    

import random
import sys
#Check if the user provided the file name with tests
if len(sys.argv)<2:
    print("Provide the file Name please")
    sys.exit()

#object switch that contain port counter, and its neighbors and buffer for packets
class Switch():
    def __init__(self,id):
        self.port =1
        self.id=id
        self.root=id
        self.neighbors =dict()
        self.hubsToRoot =0
        self.packetsBuffer =dict()
        self.finalConn = None
    def updatePortCounter(self):
        self.port+=1

#list to contain each test from the file        
switchesTests = list()
#the file name the user proves
theFile = sys.argv[1]
with open(theFile) as myFile:
    for line in myFile:
        switchesTests.append(line)

#parses the test and creates a list of tuples for the connections
def eachTestComponent(testNumber,testsList):
    myTest = testsList[testNumber]
    numOFswitches = int(myTest[0])
    print("Solution of problem #{}\nThe number of Switches {}".format(testNumber+1,numOFswitches))
    print("Input: {}".format(myTest).rstrip())
    if myTest[2] == "R":
        print("Random Implementation")
        connectionsInTuples = randomTestBuilder(numOFswitches)
        pass
    else:
        connections = myTest[2:].split()
        connectionsInTuples = [tuple( map(int,pair.split("-")) ) for pair  in connections]
    return numOFswitches,connectionsInTuples

#if the user wanted random tests the this method is called
def randomTestBuilder(max):
    random.seed()
    myList = list()
    minimumConn =[x for x in range(1,max+1)]
    for x in minimumConn:
        r=random.choice([i for i in range(1,max+1) if i not in [x]])
        myList.append((x,r))
    for numTuples in range(1,random.randint(4,15)):
        n = random.randint(2,max)
        r=random.choice([i for i in range(1,max) if i not in [n]])
        tup= tuple((n,r))
        myList.append(tup)
    return myList

#create the switches objects
def buildSwitches(amount):
    switchObjects= dict()
    for i in range(1,amount+1):
        switchObjects[i]=Switch(i)
    return switchObjects   

#connects the switches with each other as in the test file
def buildSwitchesConnections(switches,connectionsToBeMade):
    for leftSwitch,rightSwitch in connectionsToBeMade:
        switchA = switches[leftSwitch]
        switchB = switches[rightSwitch] 
        switchA.neighbors[switchA.port]=tuple((switchB.port,switchB))
        print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(switchA.id,switchA.port,switchB.id,switchB.port))
        switchB.neighbors[switchB.port]=tuple((switchA.port,switchA))
        switchA.updatePortCounter()
        switchB.updatePortCounter()

#each switch broadcasts its info for the rest of its neighbors to determine min root        
def broadcasting(switchesMap):
    myswitches = switchesMap.values()
    for senderSwitch in myswitches:
        for senderPort,neighbor in senderSwitch.neighbors.items():
            neighborPort = neighbor[0]
            currentNeighbor = neighbor[1]
            packet =[senderSwitch.id,senderSwitch.root,senderSwitch.hubsToRoot,senderPort]
            currentNeighbor.packetsBuffer[neighborPort]=tuple(packet)

#each switch handles the packets it received and choosed the min root packet                
def receiving(round,switchesMap):
    myswitches = switchesMap.values()
    for switch in myswitches:
        processedPacketSources =list()
        packetBuffer = switch.packetsBuffer.items()
        for portListening,(packetSource,packetRoot,packetHubs,packetSourcePort) in packetBuffer:
            if round ==1:#round one of receiving I check for duplicate connections to a switch
                if packetSource in processedPacketSources:
                    del(switch.neighbors[portListening])
                    del(switchesMap[packetSource].neighbors[packetSourcePort])
                    del(switchesMap[packetSource].packetsBuffer[packetSourcePort])
                else:
                    processedPacketSources.append(packetSource)
            if packetRoot < switch.root:
                switch.root = packetRoot
                switch.hubsToRoot = packetHubs+1
                switch.finalConn =(tuple((portListening,packetSource,packetSourcePort)))
        switch.packetsBuffer.clear()

def printSwitchesStates(switches):
    myswitches = switches.values()
    for switch in myswitches:
        if switch.finalConn!=None:
            sourcePort,destination,destinationPort = switch.finalConn
            print("Source Switch {} Port Number {}-----Destination Switch {} Port Number {}".format(switch.id,sourcePort,destination,destinationPort))

def printStatus(switches):
    for switch in myswitches.values():
        print("SwitchId {} sends--> {} {} {}".format(switch.id,switch.id,switch.root,switch.hubsToRoot))

for test in range(len(switchesTests)):
    numberOFswitches,connectionsbetweenSwitches = eachTestComponent(test,switchesTests)
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
    print("*"*70)
    print("*"*70)
    print()

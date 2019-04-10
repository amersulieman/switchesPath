class Switch():
    def __init__(self,id):
        self.id=id
        self.root=id
        self.switchesConnectedTo =list()
        self.numOFhubs =0
        self.packetsReceived =list()


fileInput = list()
with open("input.txt") as myFile:
    for line in myFile:
        fileInput.append(line)

def createSwitches(problemLine,problemsList):
    listOFSwitches = dict()
    numberOFswitches = int(problemsList[problemLine][0])
    for i in range(1,numberOFswitches+1):
        listOFSwitches[i]=Switch(i)
    return listOFSwitches

def switchesConnection(problemNum,listOFproblems,switches):
    connectionSetup = listOFproblems[problemNum][2:].split()
    switchesConnections = list()
    for connection in connectionSetup:
        switchesConnections.append(tuple(connection.split("-")))
    for a,b in switchesConnections: 
        switches[int(a)].switchesConnectedTo.append(switches[int(b)])
        switches[int(b)].switchesConnectedTo.append(switches[int(a)])

def sending(switches):
    for switch in switches.values():
        for x in range(0,len(switch.switchesConnectedTo)): 
            port = x+1
            packet =[switch.id,switch.root,switch.numOFhubs,port]
            switches[switch.switchesConnectedTo[x].id].packetsReceived.append(tuple(packet))

def validateOnePortPerTwoSwitchConnections(switches):
    for switch in switches.values():
        packetsSources =[a for a,b,c,d in switch.packetsReceived]
        sourcesWithMultiplePacketsSent = set([x for x in packetsSources if packetsSources.count(x)>1])
        for x in sourcesWithMultiplePacketsSent:
            portsOfTheseSources = [i for i,z in enumerate(switch.switchesConnectedTo) if z.id == x]
            for port in portsOfTheseSources[1:]:
                switch.switchesConnectedTo[port]=-1



        
def receiving(switches):
    for switch in switches.values():
        for (a,b,c,d) in switch.packetsReceived:
            if b < switch.root:
                print("updating ",switch.id)
                switch.root = b
                switch.numOFhubs = c+1
            switch.packetsReceived.remove((a,b,c,d))

myswitches = createSwitches(1,fileInput)
switchesConnection(1,fileInput,myswitches)
sending(myswitches) 
print(1,myswitches[1].packetsReceived)
print(2,myswitches[2].packetsReceived)
print(3,myswitches[3].packetsReceived)
print(4,myswitches[4].packetsReceived)
print(5,myswitches[5].packetsReceived)
print(1,myswitches[1].switchesConnectedTo)
print(2,myswitches[2].switchesConnectedTo)
print(3,myswitches[3].switchesConnectedTo)
print(4,myswitches[4].switchesConnectedTo)
print(5,myswitches[5].switchesConnectedTo)

validateOnePortPerTwoSwitchConnections(myswitches)
print("after")
print(1,myswitches[1].switchesConnectedTo)
print(2,myswitches[2].switchesConnectedTo)
print(3,myswitches[3].switchesConnectedTo)
print(4,myswitches[4].switchesConnectedTo)
print(5,myswitches[5].switchesConnectedTo)

'''
print(1,myswitches[1].root,myswitches[1].numOFhubs)
print(2,myswitches[2].root,myswitches[2].numOFhubs)
print(3,myswitches[3].root,myswitches[3].numOFhubs)
print(4,myswitches[4].root,myswitches[4].numOFhubs)
print(5,myswitches[5].root,myswitches[5].numOFhubs)

receiving(myswitches)
print("After first round receivng")
print(1,myswitches[1].root,myswitches[1].numOFhubs)
print(2,myswitches[2].root,myswitches[2].numOFhubs)
print(3,myswitches[3].root,myswitches[3].numOFhubs)
print(4,myswitches[4].root,myswitches[4].numOFhubs)
print(5,myswitches[5].root,myswitches[5].numOFhubs)'''
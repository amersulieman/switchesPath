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
            if switch.switchesConnectedTo[x]==-1:
                continue
            else:
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
for x in myswitches.values():
    print(x.id,x.packetsReceived)

print()
for switch in myswitches.values():
    l20 =list()
    for switch2 in switch.switchesConnectedTo:
        if switch2 == -1:
            l20.append(switch2)
        else:
            l20.append(switch2.id)
    print(switch.id,l20)  

validateOnePortPerTwoSwitchConnections(myswitches)
print()
for switch in myswitches.values():
    l20 =list()
    for switch2 in switch.switchesConnectedTo:
        if switch2 == -1:
            l20.append(switch2)
        else:
            l20.append(switch2.id)
    print(switch.id,l20)     

for x in myswitches.values():
    print(x.id,x.packetsReceived)
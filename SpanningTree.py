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
        switches[int(a)].switchesConnectedTo.append(int(b))
        switches[int(b)].switchesConnectedTo.append(int(a))

def sending(switches):
    for switch in switches.values():
        for physicalConnection in switch.switchesConnectedTo:
            port = switch.switchesConnectedTo.index(physicalConnection)+1
            packet =[switch.id,switch.root,switch.numOFhubs,port]
            switches[physicalConnection].packetsReceived.append(tuple(packet))

myswitches = createSwitches(1,fileInput)
switchesConnection(1,fileInput,myswitches)
sending(myswitches)











print(1,myswitches[1].packetsReceived)
print(2,myswitches[2].packetsReceived)
print(3,myswitches[3].packetsReceived)
print(4,myswitches[4].packetsReceived)
print(5,myswitches[5].packetsReceived)
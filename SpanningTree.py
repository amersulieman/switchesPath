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

def receiving(switches):
    for switch in switches.values():
        l10 =list()
        counter=0
        packets = switch.packetsReceived[:]
        for (a,b,c,d) in packets:
            if a in l10:
                switch.switchesConnectedTo[counter]=-1
                switches[a].switchesConnectedTo[counter-1]=-1
                del(switches[a].packetsReceived[d-1])
            else:
                l10.append(a)
                if b < switch.root:
                    print("updating ",switch.id)
                    switch.root = b
                    switch.numOFhubs = c+1
            counter+=1
            switch.packetsReceived.remove((a,b,c,d))
myswitches = createSwitches(2,fileInput)
switchesConnection(2,fileInput,myswitches)
sameRootAll =False
while(sameRootAll==False):
    print("in loop ")
    sending(myswitches) 
    receiving(myswitches)
    for x in myswitches.values():
        if x.root!=1:
            break
    else:
        sameRootAll=True
        print("Done")

for x in myswitches.values():
    print(x.id,x.root,x.numOFhubs)
    



'''for switch in myswitches.values():
    l20 =list()
    for switch2 in switch.switchesConnectedTo:
        if switch2 == -1:
            l20.append(switch2)
        else:
            l20.append(switch2.id)
    print(switch.id,l20)  '''
class Switch():
    def __init__(self,id):
        self.id=id
        self.root=id
        self.neighbors =list()
        self.hubsToRoot =0
        self.packetsBuffer =list()

switchesTests = list()
with open("input.txt") as myFile:
    for line in myFile:
        switchesTests.append(line)

def eachTestComponent(testNumber,testsList):
    myTest = testsList[testNumber]
    numOFswitches = int(myTest[0])
    if myTest[2] == "R":
        #connectionList = randomTestBuilder()
        pass
    else:
        connectionList = myTest[2:].split()
        connectionList = [tuple( map(int,pair.split("-")) ) for pair  in connectionList]
    return numOFswitches,connectionList

def randomTestBuilder():
    pass


def buildSwitches(amount):
    switchObjects= dict()
    for i in range(1,amount+1):
        switchObjects[i]=Switch(i)
    return switchObjects   

def switchesConnection(switches,connectionsToBeMade):
    for leftSwitch,rightSwitch in connectionsToBeMade:
        switchA = switches[leftSwitch]
        switchB = switches[rightSwitch] 
        switchA.neighbors.append(switchB)
        switchB.neighbors.append(switchA)

def sending(switches):
    for switch in switches.values():
        for x in range(0,len(switch.neighbors)):
            port = x+1
            packet =[switch.id,switch.root,switch.hubsToRoot,port]
            if switch.neighbors[x]==-1:
                continue
            else:
                switches[switch.neighbors[x].id].packetsBuffer.append(tuple(packet))

def receiving(switches):
    for switch in switches.values():
        l10 =list()
        counter=0
        packets = switch.packetsBuffer[:]
        for (a,b,c,d) in packets:
            if a in l10:
                switch.neighbors[counter]=-1
                switches[a].neighbors[counter-1]=-1
                del(switches[a].packetsBuffer[d-1])
            else:
                l10.append(a)
                if b < switch.root:
                    print("updating ",switch.id)
                    switch.root = b
                    switch.hubsToRoot = c+1
            counter+=1
            switch.packetsBuffer.remove((a,b,c,d))

numberOFswitches,connectionsbetweenSwitches = eachTestComponent(1,switchesTests)
myswitches = buildSwitches(numberOFswitches)
switchesConnection(myswitches,connectionsbetweenSwitches)
'''switchesConnection(2,switchesTests,myswitches)
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
    print(x.id,x.root,x.hubsToRoot)
    



for switch in myswitches.values():
    l20 =list()
    for switch2 in switch.neighbors:
        if switch2 == -1:
            l20.append(switch2)
        else:
            l20.append(switch2.id)
    print(switch.id,l20)  '''
import copy


class cleaner:
    def __init__(self, initialroom):
        self.currentRoom = initialroom

    def getCurrentRoom(self):
        return self.currentRoom

    def setCurrentRoom(self, room):
        self.currentRoom = room

    def suckDirt(self, roomNo, environment):
        if roomNo == 1:
            environment.setRoom1Clean()
        else:
            environment.setRoom2Clean()


class environment:
    def __init__(self):
        self.room1Clean = False
        self.room2Clean = False

    def isRoom1Clean(self):
        return self.room1Clean

    def isRoom2Clean(self):
        return self.room2Clean

    def setRoom1Clean(self):
        self.room1Clean = True

    def setRoom2Clean(self):
        self.room2Clean = True


class state:

    def __init__(self, environment, cleaner, label):
        self.environment = environment
        self.cleaner = cleaner
        self.label = label
        self.parent = None

    def getLabel(self):
        return self.label

    def cleanerLocation(self):
        return self.cleaner.getCurrentRoom()

    def getenvironment(self):
        return self.environment

    def getCleaner(self):
        return self.cleaner

    def getParent(self):
        return self.parent

    def setParent(self, p):
        self.parent = p


def returnNewState(room1Clean, room2Clean, agentPos, stateLabel):
    tmpState = state(environment(), cleaner(agentPos), stateLabel)
    if room1Clean is True:
        tmpState.environment.room1Clean = True
    else:
        tmpState.environment.room1Clean = False
    if room2Clean is True:
        tmpState.environment.room2Clean = True
    else:
        tmpState.environment.room2Clean = False

    tmpState.cleaner.currentRoom = agentPos
    tmpState.label = stateLabel
    return copy.deepcopy(tmpState)


def returnStateSpaceAndActions(state1):
    tmpList = []
    # state after initial state
    state2 = returnNewState(False, False, 2, 2)  # in room2 with both rooms dirty
    state3 = returnNewState(True, False, 1, 3)  # in room1 with only room 1 clean and the  other one dirty
    state4 = returnNewState(True, False, 2, 4)  # in room2 with only room 1 clean and the  other one dirty
    state5 = returnNewState(False, True, 1, 5)  # in room1 with only room 2 clean
    state6 = returnNewState(False, True, 2, 6)  # in room 2 with only room 2 clean
    state7 = returnNewState(True, True, 1, 7)  # in room 1 with both rooms clean
    state8 = returnNewState(True, True, 2, 8)  # in room2 with both rooms clean

    l1 = state1.label
    l2 = state2.label
    l3 = state3.label
    l4 = state4.label
    l5 = state5.label
    l6 = state6.label
    l7 = state7.label
    l8 = state8.label
    transitions = {
        tuple[l1, "R"]: state2,
        tuple[l1, "L"]: state1,
        tuple[l1, "S"]: state3,
        tuple[l2, "L"]: state1,
        tuple[l2, "R"]: state2,
        tuple[l2, "S"]: state6,
        tuple[l3, "S"]: state3,
        tuple[l3, "L"]: state3,
        tuple[l3, "R"]: state4,
        tuple[l4, "R"]: state4,
        tuple[l4, "L"]: state3,
        tuple[l4, "S"]: state8,
        tuple[l5, "R"]: state6,
        tuple[l5, "S"]: state5,
        tuple[l5, "L"]: state7,
        tuple[l6, "R"]: state6,
        tuple[l6, "S"]: state6,
        tuple[l6, "L"]: state5,
        tuple[l7, "S"]: state7,
        tuple[l7, "L"]: state7,
        tuple[l7, "R"]: state8,
        tuple[l8, "S"]: state8,
        tuple[l8, "R"]: state8,
        tuple[l8, "L"]: state7
    }

    tmpList.append(state1)
    tmpList.append(state2)
    tmpList.append(state3)
    tmpList.append(state4)
    tmpList.append(state5)
    tmpList.append(state6)
    tmpList.append(state7)
    tmpList.append(state8)
    return transitions, tmpList


def main():
    global path
    agent = cleaner(1)
    env = environment()
    initialState = state(env, agent, 1)
    Transitions, stateSpace = returnStateSpaceAndActions(initialState)
    printAllStates(stateSpace)
    initStateIndex, algo = takeInput()
    initialState = stateSpace[initStateIndex - 1]
    if algo == 1:
        path = breadthfirstsearch(initialState, Transitions)
    elif algo == 2:
        print("Performing depth first search...")
        path = depthfirstSearch(initialState, Transitions)

    if path.__len__() != 0:
        print(" ")
        print("Path to goal state is : ")
        for node in path:
            print(node.label)

def printAllStates(stateSpace):
    cleanStatus = ""
    cleanStatus2 = ""
    roomNo = ""
    for node in stateSpace:
        print("State#" + str(node.label))
        if node.environment.room1Clean:
            cleanStatus = " is Clean"
        else:
            cleanStatus = " is not Clean"
        if node.environment.room2Clean:
            cleanStatus2 = " is Clean"
        else:
            cleanStatus2= " is not Clean"
        roomNo = node.cleaner.currentRoom

        print("Room1: " + cleanStatus )
        print("Room2: " + cleanStatus2)
        print("Agent is in room#" + str(roomNo))
        print("")

def takeInput():
    print("Select an initial state(1 to 8): ")
    tmpInput = input()
    print("Select one of the following search algorithms: ")
    print("1. Breadth First Search")
    print("2. Depth First Search")
    tmpAlgo = input()

    return int(tmpInput), int(tmpAlgo)


def depthfirstSearch(initialState, transitions):
    stack = [initialState]
    discovered = []
    finalNode = None
    sentinelVal = 1
    while stack and sentinelVal:
        node = stack.pop()
        if goalTest(node):
            print("Visited " + str(node.label))
            print("Goal discovered as the initial state#" + str(node.label))
            break
        if not discovered.__contains__(node):
            print("Visited " + str(node.label))
            discovered.append(node)
            t_l = node.label
            tmpactions = returnSuccessors(t_l, transitions)
            for child in tmpactions:
                if goalTest(child):
                    if child.label != node.label:
                        child.parent = node
                    print("Goal state discovered as state#" + str(child.label))
                    finalNode = child
                    sentinelVal = 0
                    break
                if child.label != node.label and (discovered.__contains__(child) == False):  # if our transition for an action doesn't end up on the same node
                    child.parent = node  # updating the parent reference
                    stack.append(child)

    # GETTING THE PATH
    pathQueue = []
    stack = []
    while finalNode is not None:
        stack.append(finalNode)
        finalNode = finalNode.getParent()

    while stack.__len__() != 0:
        pathQueue.append(stack.pop())

    return pathQueue


def returnSuccessors(stateLabel, transitions):
    tmpactions = [transitions.get(tuple[stateLabel, "S"]), transitions.get(tuple[stateLabel, "R"]),
                  transitions.get(tuple[stateLabel, "L"])]
    return tmpactions


def breadthfirstsearch(initialState, transitions):
    node = initialState
    if goalTest(node):
        print("Goal discovered as the initial state")
        return [node]
    queue = []
    explored = []
    finalNode = None
    queue.append(node)
    print("Starting from the initial state#" + str(initialState.label))

    sentinelVal = 1
    while queue and sentinelVal:
        node = queue.pop(0)
        explored.append(node)
        t_l = node.label
        actions = returnSuccessors(t_l, transitions)
        for child in actions:
            if child not in explored and child not in queue:
                if child.label != node.label:  # if not the same node
                    child.setParent(node)

                if goalTest(child) is True:
                    finalNode = child
                    sentinelVal = 0
                    print("Discovered State#" + str(child.label) + " as the goal state")
                    break
                print("Discovered State#" + str(child.label))
                queue.append(child)
        # GETTING THE PATH
    pathQueue = []
    stack = []
    while finalNode is not None:
        stack.append(finalNode)
        finalNode = finalNode.getParent()
    while stack.__len__() != 0:
        pathQueue.append(stack.pop())

    return pathQueue


def goalTest(state):
    return state.environment.room2Clean is True and state.environment.room1Clean is True


if __name__ == '__main__':
    main()

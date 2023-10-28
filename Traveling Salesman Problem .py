def solution(times,times_limit):
    # Your code here
    return getMaxBunniesWeCanRescueWithinTimeLimit( times, times_limit )
def getMaxBunniesWeCanRescueWithinTimeLimit( adjacencyMatrix, timeLimit ):

    validateInputs( adjacencyMatrix, timeLimit )

    bulkheadIndex = len(adjacencyMatrix) - 1
    numBunnies = bulkheadIndex - 1
    if numBunnies == 0: return []
    convertAdjacencyMatrixToAllPairsShortestPaths( adjacencyMatrix )

    startIndex = 0
    if adjacencyMatrix[startIndex][bulkheadIndex] > timeLimit: return []

    rangeOfBunnyIndexes = range( startIndex + 1, bulkheadIndex )
    allBunniesSaved = {}

    def getMaxBunniesWeCanRescueWithinTimeLimit( currentNode, timeTakenSoFar, bunniesVisitedSoFar, bunniesSavedSoFar ):

        if 1 in allBunniesSaved: return bunniesSavedSoFar
        elif len(bunniesSavedSoFar) == numBunnies:
            allBunniesSaved[1] = True
            return bunniesSavedSoFar

        maxBunniesSavedTotal = list(bunniesSavedSoFar)

        for nextBunnyIndex in rangeOfBunnyIndexes:
            if nextBunnyIndex in bunniesVisitedSoFar: continue

            nextBunniesVisitedSoFar = bunniesVisitedSoFar.copy()
            nextBunniesVisitedSoFar.add(nextBunnyIndex)

            timeToReachNextBunny = adjacencyMatrix[currentNode][nextBunnyIndex]
            timeToEscapeWithNextBunny = adjacencyMatrix[nextBunnyIndex][bulkheadIndex]

            if timeTakenSoFar + timeToReachNextBunny + timeToEscapeWithNextBunny > timeLimit: continue

            nextBunniesSaved = list(bunniesSavedSoFar)
            nextBunniesSaved.append(nextBunnyIndex-1)

            maxBunniesIfWeSaveNextBunny = getMaxBunniesWeCanRescueWithinTimeLimit(
                currentNode = nextBunnyIndex,
                timeTakenSoFar = timeTakenSoFar + timeToReachNextBunny,
                bunniesVisitedSoFar = nextBunniesVisitedSoFar,
                bunniesSavedSoFar = nextBunniesSaved
            )
            if len(maxBunniesIfWeSaveNextBunny) > len(maxBunniesSavedTotal): maxBunniesSavedTotal = maxBunniesIfWeSaveNextBunny

        return maxBunniesSavedTotal

    maxBunniesWeCanRescueWithinTimeLimit = getMaxBunniesWeCanRescueWithinTimeLimit(
        currentNode = startIndex,
        timeTakenSoFar = 0,
        bunniesVisitedSoFar = set(),
        bunniesSavedSoFar = []
    )

    maxBunniesWeCanRescueWithinTimeLimit.sort()
    return maxBunniesWeCanRescueWithinTimeLimit

Infinite = float('inf')
NegativeInfinite = float('-inf')

def convertAdjacencyMatrixToAllPairsShortestPaths( adjacencyMatrix ):
    rangeOfNodes = range( len(adjacencyMatrix) )
    for reductionPass in [1, 2]:
        for intermediateNodeIndex in rangeOfNodes:
            for row in rangeOfNodes:
                for col in rangeOfNodes:
                    pathLengthViaIntermediateNode = adjacencyMatrix[row][intermediateNodeIndex] + adjacencyMatrix[intermediateNodeIndex][col]
                    if pathLengthViaIntermediateNode < adjacencyMatrix[row][col]:
                        adjacencyMatrix[row][col] = pathLengthViaIntermediateNode if reductionPass == 1 else NegativeInfinite

def validateInputs( adjacencyMatrix, timeLimit ):
    if not type(timeLimit) is int or timeLimit < 0 or timeLimit > 999:
        raise Exception( "timeLimit must be a non-negative integer that is at most 999" )

    adjacencyMatrixExceptionMessage = "The adjacencyMatrix must be a square matrix of integers ( or Infinite if an edge is disconnected ); "\
        "the size must be at least 2 ( ie there must be at least a starting point and the bulkhead ) and no more than 7 ( ie 0-5 optional bunnies )"
    numMatrixRows = len(adjacencyMatrix)
    if numMatrixRows < 2 or numMatrixRows > 7:
        raise Exception( adjacencyMatrixExceptionMessage )

    for row in range(numMatrixRows):
        col = adjacencyMatrix[row]
        colLength = len(col)
        if colLength != numMatrixRows: raise Exception( adjacencyMatrixExceptionMessage )
        for col in range(colLength):
            colValue = adjacencyMatrix[row][col]
            if not type(colValue) is int and not ( type(colValue) is float and colValue in [Infinite, NegativeInfinite] ):
                raise Exception( adjacencyMatrixExceptionMessage )
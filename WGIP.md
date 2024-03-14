# Improvement Proposal
My proposal is to optimize the current breadth-first-search algorithm by allowing it to search from the start node and the 
finish node simultaneously. This optimization is referred to as *bidirectional BFS*. This will allow for the search algorithm to find a common path much more time and space efficiency. 
The implementation would involve using two *deques* to store the discovered pages from each node, rather than a set which is currently being used, in order to append and pop pages from both ends more efficiently. 

# Psuedocode for BFS
```python 
BidirectionalBFS(start, finish):
    if start == finish:
        return [start]

    Initialize startQueue with [start], finishQueue with [finish]
    Initialize visitedFromStart with {start}, visitedFromFinish with {finish}

    while startQueue and finishQueue are not empty:
        pathFromStart = Expand(startQueue, visitedFromStart, visitedFromFinish)
        if pathFromStart is not empty:
            return pathFromStart + Reverse(Expand(finishQueue, visitedFromFinish, visitedFromStart))

        pathFromFinish = Expand(finishQueue, visitedFromFinish, visitedFromStart)
        if pathFromFinish is not empty:
            return Expand(startQueue, visitedFromStart, visitedFromFinish) + Reverse(pathFromFinish)

    return "No path found"

Expand(queue, visitedThisSide, visitedOtherSide):
    currentPage, path = queue.dequeue()

    for each link in GetLinks(currentPage):
        if link not in visitedThisSide:
            visitedThisSide.add(link)
            newPath = path + [link]
            if link in visitedOtherSide:
                return newPath
            else:
                queue.enqueue(link, newPath)

    return []

GetLinks(page):
```
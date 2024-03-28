# Improvement Proposal
Convert the current algorithm into a **bidirectional breadth-first search**. Also utilize wikipedia API instead of scraping for urls.

**Mitchell Toney** *(solo)*
## High-level Description
It would optimize the current breadth-first search algorithm by allowing it to search from the start node and the finish node simultaneously.
This allows for the search algorithm to find a common path much more time and space efficiency. The implementation would involve using two *deques* to store the discovered pages from each node, rather than a set which is currently being used, in order to append and pop pages from both ends more efficiently. It would finish the search when a common page is found rather than reaching the final or start page. 

As for the API utilization, I will reference the implementation done [here](https://github.com/jwngr/sdow/blob/master/sdow/helpers.py).
## Psuedocode for BFS
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

## Milestones
1. Rework the `find_paths` method from `crawler.py` to search from both the initial and final page.
I plan to utilize aider, 6 degrees of wikipedia, and my current python knowledge to implement the changes for the first two milestones. I may need more resources for milestone two.
Deadline: 04/11/24
2. Allow for the completion of a path if there is a shared page that has been found during the search from both the start and final page. (harder part)
Deadline: 04/25/24
3. Utilize the Wikipedia API in the `get_links` method from `crawler.py` rather than url scraping for more efficiency.
Deadline: 05/08/24
I plan to use ChatGPT for assistance in using the Wikipedia API documentation.
*Deadlines subject to change*

## Progress
I attempted to make a working version bi-directional BFS with a few detailed aider prompts but after 10 versions that ended up breaking, I decided I would need a different approach.
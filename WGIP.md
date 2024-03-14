# Improvement Proposal
My proposal is to optimize the current breadth-first-search algorithm by allowing it to search from the start node and the 
finish node simultaneously. This optimization is reffered to as *bidirectional BFS*. This will allow for the search algorithm to find a common path much more time and space efficiency. 
The implementation would involve using two *deques* to store the discovered pages from each node, rather than a set which is currently being used, in order to append and pop pages from both ends more efficiently. 
# WikipediaGame

## Installation

(these instructions should work under GNU/Linux and Macos and WSL)

Prerequisites: Python

```
git clone https://github.com/mitchelltoney/WikipediaGame.git
cd WikipediaGame/server
source setup.sh
```

Starting the server:

```
python server.py
```


Play the game on [`localhost:5001`](http://127.0.0.1:5001/) (this link will only work after you started the server on your machine (watch the console in case the port number changed to eg `5000`)).


## Description

- The `crawler.py` file was modified to utilize the Wikipedia API in order to obtain forward and backwards links for any wikipedia pages. Two methods were implemented in order to request these links from the API.
- The `find_path` method from `crawler.py` was modified in order to utilize both the forwards links and back links to create two seperate queues for each direction. This search algorithm is labeled **bidirectional breadth-first search** It simultaneously searches from both the `start_page` and the `finish_page` in order to find a page that has been reached in both queues. It then constructs the complete path in the form of forward links.

## Project Testing

- Run the installation steps above to start the server, the go to the game at the printed link. 
- In the game UI, enter two wikipedia page links in both the "Start Page URL:" and "Finish Page URL:" fields. 
- The `crawler.py` should find a path between these two pages and print out each of the wikipedia page titles to represent the path

## Limitations and Future Work

- It seems as though the API occasionally is not correctly representing the titles webpages as sometimes there will be an outputted path, found with the `find_path` algorithm, that does not seem to connect through the wikipedia pages, despite it logically making sense to exist. This makes me think that the link does exist and that the title is wrong, or maybe that the link was recently removed from the wikipedia page, or maybe not able to be found with my "cmd+F" search for the page. I of course tried to fix this but was not able to do so. This would be the first thing I would want to fix in the future

- Updating the UI of the website to be more interactive or entertaining could be an addition to make the game more fun, although not relating to the speed or efficiency of the algorithm.


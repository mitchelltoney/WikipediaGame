# Contributions


## About the Project

The project is built off of the [WikipediaGame](https://github.com/alexhkurz/WikipediaGame) from alexhkurz. The goal of the project was to rework the method of finding links to be more efficient as well as optimizing the search algorithm more efficiently find a connection between the start and end page. The vast majority of the changes are located in `crawler.py`, although some small changes were made to the log output as well as javascript and html files.

## Main Changes

### Getting Links

The `crawler.py` has been modified to utilize the [wikipedia API](https://en.wikipedia.org/w/api.php) to get both forwards links and backword links to pages in order to accomodate the bidirectional search, as well as to improve the speed of link acquisition. 

### Search Algorithm

The find path algorithm was modified to use two queues and two sets in order to document the visited pages as well as the path from either the `start_page` or the `finish_page` to a connecting page. After a connecting page has been found, the algorithm will construct and return the complete forward path from the `start_page` to the `finish_page`.

### Benchmark

Common benchmark tests that I would run would be between two wikipedia pages of common noun, as they were the easiest to find link titles of when checking the path.

Example: **Steak -> Mathematics**

Took around *6.5 seconds* to find the path of length 4 (s,m,m,f) with bidirectional search.

This same search took around 30 seconds for the forward search which used scraping to find web pages.

| Path | **Bidirectional** | Forward<sub>(Original)</sub> |
| ---- | ----------------- | ----------------- |
| Steak -> Mathematics | 6.5 seconds | 30 seconds |
| Couch -> Abstraction | 3.2 seconds | 32 seconds |
| Kitten -> Germany | 24 seconds | 25 seconds |
| Diamond -> Computer | 3 seconds | 29 seconds |

All of these tests were run on a MacBook Pro 2020 with 2 GHz Quad-Core Intel Core i5 processor and 16 GB 3733 MHz LPDDR4X RAM.

It was odd that the bidirectional search took 24 seconds to find a path from *Kitten* to *Germany*, which was about the same performance as the original search algorithm, but for most other search paths it was much faster.

Any of these can be used as **sample inputs** but any valid wikipedia pages will work as well.
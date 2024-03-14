import time
import requests
from bs4 import BeautifulSoup
import re

TIMEOUT = 20  # time limit in seconds for the search

def get_links(page_url):
    print(f"Fetching page: {page_url}")
    response = requests.get(page_url)
    print(f"Finished fetching page: {page_url}")
    soup = BeautifulSoup(response.text, 'html.parser')
    from urllib.parse import urljoin
    all_links = [urljoin(page_url, a['href']) for a in soup.find_all('a', href=True) if '#' not in a['href']]
    # print(f"All links found: {all_links}")
    links = [link for link in all_links if re.match(r'^https://en\.wikipedia\.org/wiki/[^:]*$', link) and '#' not in link]
    print(f"Found {len(links)} links on page: {page_url}")
    return links

def find_path(start_page, finish_page):
    queue_start = [(start_page, [start_page], 0)]
    queue_finish = [(finish_page, [finish_page], 0)]
    discovered_start = set()
    discovered_finish = set()
    logs = []

    # bidirectional breadth first search
    start_time = time.time()
    elapsed_time = time.time() - start_time
    while queue_start and queue_finish and elapsed_time < TIMEOUT:  
        (vertex_start, path_start, depth_start) = queue_start.pop(0)
        (vertex_finish, path_finish, depth_finish) = queue_finish.pop(0)
        links_start = set(get_links(vertex_start)) - discovered_start
        links_finish = set(get_links(vertex_finish)) - discovered_finish
        if links_start & links_finish:
            common_page = next(iter(links_start & links_finish))
            log = f"Found common page: {common_page}"
            print(log)
            logs.append(log)
            logs.append(f"Search took {elapsed_time} seconds.")
            print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
            logs.append(f"Discovered pages: {len(discovered_start) + len(discovered_finish)}")
            return path_start + [common_page] + path_finish[::-1], logs, elapsed_time, len(discovered_start) + len(discovered_finish) # return with success
        else:
            for next_start in links_start:
                log = f"Adding link to start queue: {next_start} (depth {depth_start})"
                print(log)
                logs.append(log)
                discovered_start.add(next_start)
                queue_start.append((next_start, path_start + [next_start], depth_start + 1))
            for next_finish in links_finish:
                log = f"Adding link to finish queue: {next_finish} (depth {depth_finish})"
                print(log)
                logs.append(log)
                discovered_finish.add(next_finish)
                queue_finish.append((next_finish, path_finish + [next_finish], depth_finish + 1))
        elapsed_time = time.time() - start_time
    logs.append(f"Search took {elapsed_time} seconds.")
    print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
    logs.append(f"Discovered pages: {len(discovered_start) + len(discovered_finish)}")
    raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(discovered_start) + len(discovered_finish))
class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered

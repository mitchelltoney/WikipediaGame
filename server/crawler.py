import time
import requests
from bs4 import BeautifulSoup
import re

TIMEOUT = 1200  # time limit in seconds for the search
abort = False  # flag to abort the search

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
    logs = []
    queue_start = [(start_page, [start_page], 0)]
    queue_finish = [(finish_page, [finish_page], 0)]
    discovered_start = set()
    discovered_finish = set()
    paths_start = {start_page: [start_page]}
    paths_finish = {finish_page: [finish_page]}

    # breadth first search
    start_time = time.time()
    elapsed_time = time.time() - start_time
    while queue_start and queue_finish and elapsed_time < TIMEOUT and not abort and not abort:  # Add abort condition to while loop
        for queue, discovered, other_discovered, paths in [(queue_start, discovered_start, discovered_finish, paths_start), (queue_finish, discovered_finish, discovered_start, paths_finish)]:
            (vertex, path, depth) = queue.pop(0)
            for next in set(get_links(vertex)) - discovered:
                if next in other_discovered:
                    log = f"Found common page: {next}"
                    print(log)
                    logs.append(log)
                    logs.append(f"Search took {elapsed_time} seconds.")
                    print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
                    logs.append(f"Discovered pages: {len(discovered)}")
                    if next in paths:
                        full_path = path + paths[next][::-1]  # concatenate the path from the start page to the common page with the reversed path from the finish page to the common page
                        abort = True  # Set abort flag to True
                        return full_path, logs, elapsed_time, len(discovered) # return with success
                    else:
                        logs.append(f"Key {next} not found in paths.")
                        print(f"Key {next} not found in paths.")
                        continue
                else:
                    log = f"Adding link to queue: {next} (depth {depth})"
                    print(log)
                    logs.append(log)
                    discovered.add(next)
                    paths[next] = path + [next]
                    queue.append((next, paths[next], depth + 1))
        elapsed_time = time.time() - start_time
    logs.append(f"Search took {elapsed_time} seconds.")
    print(f"Search took {elapsed_time} seconds.")  # Add a print statement to log the elapsed time
    logs.append(f"Discovered pages: {len(discovered)}")
    raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(discovered))
class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered

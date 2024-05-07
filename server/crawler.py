import time
import requests

TIMEOUT = 20  # Time limit in seconds for the search

class TimeoutErrorWithLogs(Exception):
    def __init__(self, message, logs, time, discovered):
        super().__init__(message)
        self.logs = logs
        self.time = time
        self.discovered = discovered

def format_title_for_url(title):
    return title.replace(' ', '_')

def extract_title_from_url(url):
    return url.split('/wiki/')[-1].replace('_', ' ')

def get_links_api(page_title):
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "titles": page_title,
        "prop": "links",
        "plnamespace": 0,
        "pllimit": "max"
    }

    links = []
    while True:
        response = session.get(url=url, params=params)
        data = response.json()
        pages = data['query']['pages']
        for k, v in pages.items():
            for l in v.get('links', []):
                links.append(format_title_for_url(l['title']))

        if 'continue' not in data:
            break
        else:
            params['plcontinue'] = data['continue']['plcontinue']

    return links

def get_backlinks_api(page_title):
    session = requests.Session()
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "list": "backlinks",
        "bltitle": page_title,
        "blnamespace": 0,
        "bllimit": "max"
    }

    backlinks = []
    while True:
        response = session.get(url=url, params=params)
        data = response.json()
        for b in data['query']['backlinks']:
            backlinks.append(format_title_for_url(b['title']))

        if 'continue' not in data:
            break
        else:
            params['blcontinue'] = data['continue']['blcontinue']

    return backlinks

def find_path(start_page, finish_page):
    start_title = extract_title_from_url(start_page)
    finish_title = extract_title_from_url(finish_page)

    forward_queue = [(start_title, [start_title])]
    backward_queue = [(finish_title, [finish_title])]
    forward_discovered = {start_title}
    backward_discovered = {finish_title}
    logs = []  # Initialize logs

    start_time = time.time()

    while forward_queue and backward_queue:
        elapsed_time = time.time() - start_time
        if elapsed_time >= TIMEOUT:
            raise TimeoutErrorWithLogs("Search exceeded time limit.", logs, elapsed_time, len(forward_discovered) + len(backward_discovered))

        # Forward search
        if forward_queue:
            current_title, path = forward_queue.pop(0)
            for next_title in set(get_links_api(current_title)) - forward_discovered:
                if next_title == finish_title:
                    complete_path = path + [next_title]
                    return complete_path, logs, elapsed_time, len(forward_discovered) + len(backward_discovered)
                forward_discovered.add(next_title)
                forward_queue.append((next_title, path + [next_title]))
                logs.append(f"Explored forward: {next_title}")

        # Backward search
        if backward_queue:
            current_title, path = backward_queue.pop(0)
            for next_title in set(get_backlinks_api(current_title)) - backward_discovered:
                if next_title in forward_discovered:
                    forward_path = next((item[1] for item in forward_queue if item[0] == next_title), None)
                    if forward_path is not None:
                        complete_path = forward_path + path[::-1][1:]
                        return complete_path, logs, elapsed_time, len(forward_discovered) + len(backward_discovered)
                backward_discovered.add(next_title)
                backward_queue.append((next_title, path + [next_title]))
                logs.append(f"Explored backward: {next_title}")


    return [], logs, elapsed_time, len(forward_discovered) + len(backward_discovered)

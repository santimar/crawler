class LRUCache:

    def __init__(self, max_size=100):
        self.url_list = []
        self.MAX_CACHE_SIZE = max_size

    def is_present_or_add(self, url):
        if url in self.url_list:
            return True
        self.url_list.append(url)
        if len(self.url_list) > self.MAX_CACHE_SIZE:
            self.url_list.pop(0)
        return False

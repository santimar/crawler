import time
import requests
import sieve
import page_parser
import lru_cache
import sys
import getopt

if __name__ == "__main__":
    initial_url = None
    max_pages = 500
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:m:")
    except getopt.GetoptError:
        print('crawler.py -u <initial url> [-m <max pages to download>]')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('crawler.py -u <initial url> [-m <max pages to download>]')
            sys.exit()
        elif opt == "-u":
            initial_url = arg
        elif opt == "-m":
            max_pages = arg

    if initial_url is None:
        print('crawler.py -u <initial url> [-m <max pages to download>]')
        sys.exit()

    sieve = sieve.Sieve()
    cache = lru_cache.LRUCache()
    logfile = open("./log.txt", 'w')
    sieve.add_url(initial_url)
    time.sleep(2)
    for i in range(max_pages):
        url = sieve.get_url()
        print("Downloading {0}".format(url))
        print("[{0}] Downloading {1}".format(time.strftime("%y/%m/%d %H:%M:%S"), url), file=logfile)
        logfile.flush()
        if url is None:
            time.sleep(5)
            continue
        try:
            content = requests.get(url).text
        except:
            continue

        links = page_parser.get_links(url, content)
        page_parser.parse_content(url, content)

        print("Found {0} links: {1}".format(len(links), links))
        for link in links:
            if cache.is_present_or_add(link):
                print("[SKIP] {0}".format(link))
            else:
                print("[VALID] {0}".format(link))
                sieve.add_url(link)
    logfile.close()

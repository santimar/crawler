import time
import requests
import sieve as s
import page_parser
import lru_cache
import argparse


def main(args):
    initial_url = args.url
    max_pages = args.max_pages

    sieve = s.Sieve()
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='A simple web crawler')
    parser.add_argument("url", help="Initial url")
    parser.add_argument("-m", metavar="MAX_PAGES", dest="max_pages",
                        help="Max number of pages to download", type=int, default=500)
    args = parser.parse_args()
    main(args)

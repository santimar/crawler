This is a simple web crawler, that starts from the given url and tries to follow all the links found during the crawling until it reaches &lt;max pages to download&gt; (default 500)<br>

There are few components:
- Sieve: avoids duplicate urls with constant memory space usage
- Delayed queue: prevents the crawler to flood a single host (and also a single IP) of requests
- Page parser: finds all the links in the page
- LRU cache: tries to speed up the system, preventing recent duplicate urls to enter the sieve

![Crawler schema](/docs/schema.png)

### Usage:
```
python crawler.py [-m <max pages to download>] <initial_url> 
```
<br>
Note: this project was made with learning purpose, so you probably shouldn't use it in the real world 

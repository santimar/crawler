import regex


def get_links(page_base_url, content):
    # Recovering links via regular expression
    links = regex.findall("href=\"(\S+)\"", content)
    for i in range(len(links)):
        links[i] = __get_complete_link(page_base_url, links[i])
    return links


def parse_content(url, content):
    # Simple page parsing, recovering all the email in the page
    mails = regex.findall("((?:[A-Za-z0-9]+)@(?:[A-Za-z0-9]+)\.(?:[a-z]{2,5}))", content)
    if len(mails) == 0:
        return
    try:
        file = open('./result.txt', 'a')
        for mail in mails:
            print("{0} -> {1}".format(url, mail), file=file)
        file.close()
    except:
        pass


def __get_complete_link(base, path):
    try:
        # try to strip content after #
        path = path[:path.index("#")]
        if len(path) == 0:
            return base
    except ValueError:
        pass
    if path.startswith("http"):
        return path
    if path.startswith("/"):
        if base.count("/") == 2:
            return base + path
        else:
            pos = base.replace("/", "", 2).find("/") + 2
            host = base[:pos]
            return host + path
    else:
        return base[:base.rindex("/") + 1] + path

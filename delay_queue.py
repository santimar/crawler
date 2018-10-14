import time
import regex
import requests


class DelayQueue:
    # Delay in seconds between two access
    HOST_DELAY = 300
    IP_DELAY = 20

    def __init__(self):
        self.ip_list = {}

    def get_url(self):
        for ip in self.ip_list:
            if time.time() < self.ip_list[ip]["ts"]:
                continue
            for host in self.ip_list[ip]["hosts"]:
                if time.time() < self.ip_list[ip]["hosts"][host]["ts"] or + \
                        len(self.ip_list[ip]["hosts"][host]["urls"]) == 0:
                    continue
                # this url is valid
                self.ip_list[ip]["ts"] += self.IP_DELAY
                self.ip_list[ip]["hosts"][host]["ts"] += self.HOST_DELAY
                return host + self.ip_list[ip]["hosts"][host]["urls"].pop()
        return None

    def add_url(self, host, url_path, timestamp=time.time()):
        if len(self.ip_list) == 0:
            timestamp = time.time()
        if not self._is_valid_host(host):
            print("[FORBIDDEN HOST] ", host)
            return
        ip = self._get_ip(host)
        if ip is None:
            print("[IP NOT FOUND] for ", host)
            return
        if self.ip_list.get(ip) is None:
            self.ip_list[ip] = {"ts": timestamp, "hosts": {}}
        if self.ip_list[ip]["hosts"].get(host) is None:
            self.ip_list[ip]["hosts"][host] = {"ts": timestamp, "urls": []}

        self.ip_list[ip]["hosts"][host]["urls"].append(url_path)

    def print_debug(self):
        for ip, val in self.ip_list.items():
            print("{0} -> ".format(ip))
            for host in self.ip_list[ip]["hosts"]:
                print("{0: <18}{1} -> {2}".format(" ", host, self.ip_list[ip]["hosts"][host]["urls"]))

    def _get_ip(self, objective_host):
        # I want to avoid making request to DNS if we already have the host's IP
        for ip in self.ip_list:
            for host in self.ip_list[ip]["hosts"]:
                if host == objective_host:
                    print("[IP FOUND] for ", objective_host)
                    return ip

        # We don't have the IP, need to aks to DNS
        try:
            print("Requesting ip of ", objective_host)
            content = requests.get(objective_host, stream=True)
            return content.raw._connection.sock.getpeername()[0]
        except:
            return None

    @staticmethod
    def _is_valid_host(host):
        invalid_hosts = ["(.*)google\.it", "(.*)google\.com", "(.*)twitter\.com",
                         "(.*)facebook\.com", "(.*)linkedin\.com", "(.*)youtube\.com",
                         "(.*)github\.com", "(.*)instagram\.com", "(.*)static\.xx\.fbcdn\.net",
                         "(.*)messenger\.com"]
        match = [x for x in invalid_hosts if regex.match(x, host)]
        return len(match) == 0

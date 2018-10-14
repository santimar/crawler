import hashlib

from delay_queue import DelayQueue


class Sieve:
    MAX_LENGTH = 100
    DUPLICATED_VALUE = -1

    def __init__(self):
        self.V = []
        self.Z = []
        self.A = []
        self.queue = DelayQueue()

    def get_url(self):
        res = self.queue.get_url()
        if res is None:
            self._merge_v_and_z()
            res = self.queue.get_url()
        return res

    def add_url(self, url):
        if len(self.V) >= self.MAX_LENGTH:
            self._merge_v_and_z()
        _hash = self._calculate_hash(url)
        self.V.append(_hash)
        self.A.append(url)

    def _merge_v_and_z(self):
        # We need to make an indirect sorting to preserve original V order
        K = self._indirect_sort(self.V)
        # Now we have a sorted K based on V values
        # print(K)
        # Then we need to mark the index of the first occurrence of a value and remove the subsequent ones
        _first_indexes = {}
        for i in range(len(self.V)):
            if _first_indexes.get(self.V[i]) is None:
                _first_indexes[self.V[i]] = i
            else:
                self.V[i] = self.DUPLICATED_VALUE
        # print(_first_indexes)
        url_to_recover = []
        self.Z = self._merge_vectors(K, url_to_recover)
        # Retrieving urls from A
        for index in url_to_recover:
            self._add_url(self.A[index])
        # Last operation is to empty the vectors
        self.V = []
        self.A = []

    def _merge_vectors(self, K, url_recover):
        x = []
        V = self.V
        Z = self.Z
        i = j = 0
        while i < len(V) and j < len(Z):
            if V[K[i]] == self.DUPLICATED_VALUE:
                i = i + 1
                continue
            if V[K[i]] < Z[j]:
                # Only in V
                el = V[K[i]]
                # Keeping this index since it's only in V and I will need to retrieve the original url
                url_recover.append(K[i])
                i = i + 1
            elif V[K[i]] > Z[j]:
                # Only in Z
                el = Z[j]
                j = j + 1
            else:
                # In both V and Z
                el = V[K[i]]
                i = i + 1
                j = j + 1
            x.append(el)
        # I finished one array, so i need to merge the remaining part of the other
        if i == len(V):
            for n in range(j, len(Z)):
                x.append(Z[n])
        if j == len(Z):
            for n in range(i, len(V)):
                if V[K[n]] != self.DUPLICATED_VALUE:
                    x.append(V[K[n]])
                    url_recover.append(K[n])
        return x

    def _add_url(self, url):
        pos = url.replace("/", "", 2).find("/") + 2 if url.count("/") > 2 else len(url)
        host = url[:pos]
        path = url[pos:] if pos < len(url) else "/"
        self.queue.add_url(host, path)

    @staticmethod
    def _calculate_hash(s):
        return hashlib.sha1(s.encode('utf-8')).hexdigest()

    @staticmethod
    def _indirect_sort(original):
        # Creating temp array
        K = [i for i in range(0, len(original))]

        for i in range(0, len(K)):
            for j in range(i, len(K)):
                if original[K[i]] > original[K[j]]:
                    temp = K[i]
                    K[i] = K[j]
                    K[j] = temp
        return K

import hashlib
import os

from delay_queue import DelayQueue


def clean_str(string: str) -> str:
    return string.replace("\n", "")


class Sieve:
    MAX_LENGTH = 100
    DUPLICATED_VALUE = -1

    def __init__(self):
        self.V = []
        self.Z = open(self._get_file_path("Z"), "w+")
        self.A = open(self._get_file_path("A"), "w+")
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
        self.A.write(url + "\n")

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
        self._merge_vectors(K, url_to_recover)
        # Retrieving urls from A
        i = 0
        self.A.seek(0)
        for el in self.A:
            if i in url_to_recover:
                self._add_url(clean_str(el))
            i += 1
        # Last operation is to empty V and A
        self.V = []
        self.A.truncate(0)

    def _merge_vectors(self, K, url_recover):
        new_Z = open(self._get_file_path("new_Z"), "w")
        V = self.V
        i = 0
        j = clean_str(self.Z.readline())

        while i < len(V) and j != "":
            if V[K[i]] == self.DUPLICATED_VALUE:
                i += 1
                continue
            if V[K[i]] < j:
                # Only in V
                el = V[K[i]]
                # Keeping this index since it's only in V and I will need to retrieve the original url
                url_recover.append(K[i])
                i += 1
            elif V[K[i]] > j:
                # Only in Z
                el = j
                j = clean_str(self.Z.readline())
            else:
                # In both V and Z
                el = V[K[i]]
                i += 1
                j = clean_str(self.Z.readline())
            new_Z.write(el + "\n")
        # V array finished first
        if i == len(V) and j != "":
            # copy the remaining part of Z
            while j != "":
                new_Z.write(j + "\n")
                j = clean_str(self.Z.readline())
        # Z file finished first
        if j == "" and i != len(V):
            # copy the remaining part of V
            for n in range(i, len(V)):
                if V[K[n]] != self.DUPLICATED_VALUE:
                    new_Z.write(V[K[n]] + "\n")
                    url_recover.append(K[n])

        new_Z.close()
        self.Z.close()
        old_z_path = self._get_file_path("Z")
        new_z_path = self._get_file_path("new_Z")
        os.remove(old_z_path)
        os.rename(new_z_path, old_z_path)
        self.Z = open(old_z_path, "r+")

    def _add_url(self, url):
        pos = url.replace("/", "", 2).find("/") + 2 if url.count("/") > 2 else len(url)
        host = url[:pos]
        path = url[pos:] if pos < len(url) else "/"
        self.queue.add_url(host, path)

    @staticmethod
    def _get_file_path(filename):
        os.makedirs(os.path.realpath("sieve/"), exist_ok=True)
        return os.path.realpath("sieve/" + filename + ".txt")

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

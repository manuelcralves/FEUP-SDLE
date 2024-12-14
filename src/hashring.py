import hashlib
from bisect import bisect_left

class HashRing:
    def __init__(self, servers=None, replicas=5):
        self.ring = {}
        self.sorted_keys = []
        self.replicas = replicas
        self.servers = set(servers) if servers else set()
        if servers:
            for server in servers:
                self.add_server(server)

    def _hash(self, key):
        return int(hashlib.md5(key.encode('utf-8')).hexdigest(), 16)

    def add_server(self, server):
        if server in self.servers:
            return
        self.servers.add(server)
        for i in range(self.replicas):
            replica_key = f"{server.name}-{i}"
            hash_value = self._hash(replica_key)
            self.ring[hash_value] = server
            self.sorted_keys.append(hash_value)
        self.sorted_keys.sort()

    def remove_server(self, server):
        if server not in self.servers:
            return
        self.servers.remove(server)
        for i in range(self.replicas):
            replica_key = f"{server.name}-{i}"
            hash_value = self._hash(replica_key)
            del self.ring[hash_value]
            self.sorted_keys.remove(hash_value)

    def get_server(self, key):
        if not self.ring:
            return None
        hash_value = self._hash(key)
        idx = bisect_left(self.sorted_keys, hash_value)
        if idx == len(self.sorted_keys):
            idx = 0 
        return self.ring[self.sorted_keys[idx]]

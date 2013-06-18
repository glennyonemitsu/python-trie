

class Trie(object):

    def __init__(self):
        self.path = {}
        self.value = None
        self.value_valid = False

    def __setitem__(self, key, value):
        head, tail = key[0], key[1:]
        if head in self.path:
            node = self.path[head]
        else:
            node = Trie()
            self.path[head] = node

        if tail:
            node[tail] = value
        else:
            node.value = value
            node.value_valid = True

    def __delitem__(self, key):
        head, tail = key[0], key[1:]
        if head in self.path:
            node = self.path[head]
            if tail:
                del node[tail]
            else:
                node.value_valid = False
                node.value = None
            if len(node) == 0:
                del self.path[head]

    def __getitem__(self, key):
        head, tail = key[0], key[1:]
        try:
            if head in self.path:
                node = self.path[head]
                if tail:
                    return node[tail]
                elif node.value_valid:
                    return node.value
            raise KeyError(key)
        except KeyError:
            # reraised since recursion causes key to shrink
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __len__(self):
        n = 1 if self.value_valid else 0
        for k in self.path.iterkeys():
            n = n + len(self.path[k])
        return n

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def nodeCount(self):
        n = 0
        for k in self.path.iterkeys():
            n = n + 1 + self.path[k].nodeCount()
        return n

    def keys(self, prefix=[]):
        result = []
        if self.value_valid:
            isStr = True
            val = ""
            for k in prefix:
                if type(k) != str or len(k) > 2:
                    isStr = False
                    break
                else:
                    val += k
            if isStr:
                result.append(val)
            else:
                result.append(prefix)
        for k in self.path.iterkeys():
            next = []
            next.extend(prefix)
            next.append(k)
            result.extend(self.path[k].keys(next))
        return result

    def __iter__(self):
        for k in self.keys():
            yield k
        raise StopIteration

    def __add__(self, other):
        result = Trie()
        result += self
        result += other
        return result

    def __sub__(self, other):
        result = Trie()
        result += self
        result -= other
        return result

    def __iadd__(self, other):
        for k in other:
            self[k] = other[k]
        return self

    def __isub__(self, other):
        for k in other:
            del self[k]
        return self

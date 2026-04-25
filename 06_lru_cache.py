
import time

class Node:
    def __init__(self, key: int, value: int): #a 5 seconds ttl for every node init
        self.key = key
        self.value = value
        self.timestamp = time.time() + 5.0
        self.prev = None
        self.next = None    

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}
        self.left = Node(0, 0)
        self.right = Node(0, 0)
        self.left.next = self.right
        self.right.prev = self.left

    def remove(self, node: Node):
        prev = node.prev
        next = node.next
        prev.next = next
        next.prev = prev

    def insert(self, node: Node):
        prev = self.right.prev
        next = self.right
        prev.next = node
        next.prev = node
        node.prev = prev
        node.next = next

    def get(self, key: int) -> int:
        if key in self.cache:
            node = self.cache[key]
            if time.time() > node.timestamp:
                self.remove(node)
                del self.cache[key]
                return -1
            self.remove(node)
            self.insert(node)
            return node.value
        return -1
   
    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.remove(self.cache[key])
            del self.cache[key]
        node = Node(key, value)
        self.insert(node)
        self.cache[key] = node
        if len(self.cache) > self.capacity:
            lru = self.left.next
            self.remove(lru)
            del self.cache[lru.key]

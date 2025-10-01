class BFS:
    def __init__(self,t,g=[]):
        self.t = t
        self.v_n = []
        self.q = []
        self.g = g
    def enqueue(self,n):
        self.q.append(n)
    def dequeue(self):
        a = self.q.pop(0)
        return a
    def read_tree(self):
        self.enqueue(list(self.t)[0])
        while self.q:
            k = self.dequeue()
            self.v_n.append(k)
            if self.v_n[-1] == self.g:
                break
            v = self.t[k]
            if v:
                for i in v:
                    if i not in self.v_n and i not in self.q:
                        self.enqueue(i)
        return self.v_n
tree = {
    'A': ['B', 'F'],
    'B': ['A', 'C'],
    'C': ['B', 'D', 'E'],
    'D': ['C', 'E'],
    'E': ['C', 'D', 'F'],
    'F': ['A', 'E']
}
T1 = BFS(tree,"E")
print("Visited nodes:",T1.read_tree())
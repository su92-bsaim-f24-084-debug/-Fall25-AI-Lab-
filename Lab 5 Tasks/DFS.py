class DFS:
    def __init__(self, t):
        self.t = t
        self.stack = [list(t)[0]]
        self.v_n = []
    def push(self,n):
        if self.t[n]:
            self.stack.extend(reversed(self.t[n]))
    def pop(self):
        return self.stack.pop()
    def calVisited_Nodes(self):
        while self.stack:
            a = self.stack.pop()
            self.v_n.append(a)
            self.push(a)
    def display_Nodes(self):
        print(self.v_n)
tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F'],
    'D': [],
    'E': [],
    'F': ['G'],
    'G': []
}
            
Tree1 = DFS(tree)
Tree1.calVisited_Nodes()
Tree1.display_Nodes()

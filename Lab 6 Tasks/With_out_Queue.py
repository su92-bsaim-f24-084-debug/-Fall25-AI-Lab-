def bfs_tree(t, start,g=''):
    v_nodes = []
    s_level = [start]
    g = g.upper()
    while s_level:
        next_level = []
        for i in s_level:
            v_nodes.append(i)
            if v_nodes[-1] == g:
                print("Goal is present.")
                return v_nodes
            for j in t[i]:
                next_level.append(j)
        s_level = next_level
    return v_nodes

tree2 = {
    'P': ['Q', 'R'],
    'Q': ['S', 'T'],
    'R': ['U'],
    'S': [],
    'T': ['V', 'W'],
    'U': [],
    'V': [],
    'W': []
}
print(bfs_tree(tree2, 'P'))
import sys
input = lambda: sys.stdin.readline().rstrip()

# Number of commands
q = int(input())

class Node:
    def __init__(self, m_id, p_id, color, max_d, depth):
        self.id = m_id
        self.p_id = p_id
        self.color = color
        self.max_d = max_d
        self.depth = depth

tree = [[] for _ in range(100000)]
root = []

def dfs(x, color):
    tree[x][0].color = color
    # If this node has children, recolor them recursively
    for child in tree[x][1:]:
        dfs(child.id, color)

answer = 0

def score(x, colors_set):
    global answer
    # Include the color of the current node
    colors_set.add(tree[x][0].color)
    # If leaf node
    if len(tree[x]) == 1:
        answer += 1
        return
    # Otherwise, handle children
    for child in tree[x][1:]:
        child_colors = set()
        score(child.id, child_colors)
        # Merge child’s colors into our set
        colors_set |= child_colors
    # Add square of total number of colors
    answer += len(colors_set) * len(colors_set)

for _ in range(q):
    cmds = list(map(int, input().split()))
    cmd = cmds[0]

    if cmd == 100:
        # 100 m_id p_id color max_d
        _, m_id, p_id, color, max_d = cmds
        if p_id == -1:
            # Create a root node
            new_node = Node(m_id, p_id, color, max_d, 1)
            root.append(new_node)
            tree[m_id].append(new_node)
        else:
            # Attach child to existing node
            parent_node = tree[p_id][0]
            # Check if adding child exceeds parent's max_d
            if parent_node.depth + 1 <= parent_node.max_d:
                new_node = Node(m_id, p_id, color, max_d, parent_node.depth + 1)
                tree[m_id].append(new_node)
                tree[p_id].append(new_node)
            else:
                # If it violates max depth, do nothing or handle differently
                pass

    elif cmd == 200:
        # 200 m_id color
        _, m_id, color = cmds
        dfs(m_id, color)

    elif cmd == 300:
        # 300 m_id
        _, m_id = cmds
        print(tree[m_id][0].color)

    elif cmd == 400:
        # reset and compute answer across all roots
        answer = 0
        for rt in root:
            score(rt.id, set())
        print(answer)

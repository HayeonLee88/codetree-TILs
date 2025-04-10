import sys

input = lambda:sys.stdin.readline().rstrip()

q = int(input())


class Node():
    def __init__(self, id, p_id, color, max_d, p_depth):
        self.id = id
        self.p_id = p_id
        self.color = color
        self.max_d = max_d
        self.depth = p_depth + 1

    def set_color(self,color):
        self.color = color

    def set_subtree(self):
        self.subtree += 1

tree = [[] for _ in range(100000)]


def dfs(x, color):
    tree[x][0].color = color
    if len(tree[x]) == 1:
        return True
    else:
        for sub in tree[x][1:]:
            sub.color = color
            dfs(sub.id, color)
    return True  

answer = 0

def score(x, cnt):
    global answer
    cnt.add(tree[x][0].color)
    if len(tree[x]) == 1:
        answer += 1
        return True
    else:
        for sub in tree[x][1:]:
            tmp = set()
            cnt.add(sub.color)
            score(sub.id, tmp)
            cnt.update(list(tmp))
        answer += len(cnt) * len(cnt)
    return answer


root = []
for _ in range(q):
    cmds = list(map(int, input().split()))
    cmd = cmds[0]
    if cmd == 100:
        _, m_id, p_id, color, max_d = cmds
        if p_id == -1:
            root.append(Node(m_id, p_id, color, max_d, 0))
            tree[m_id].append(root[-1])
        else:
            if len(tree[p_id]) == 1:
                now = tree[p_id][0]
                check = True
                while True:
                    if now.depth + 1 > now.max_d:
                        check = False
                        break
                    if now.p_id == -1:
                        break
                    now = tree[now.p_id][0]
                    
                if check:
                    new = Node(m_id, p_id, color, max_d, tree[p_id][0].depth)
                    tree[m_id].append(new)
                    tree[p_id].append(new)
                    now = tree[p_id][0]
                    while True:
                        if now.p_id == -1:
                            break
                        now.depth += 1
                        now = tree[now.p_id][0]
            else:
                new = Node(m_id, p_id, color, max_d, tree[p_id][0].depth)
                tree[m_id].append(new)
                tree[p_id].append(new)

    elif cmd == 200:
        _, m_id, color = cmds
        dfs(m_id, color)
                  
    elif cmd == 300:
        _, m_id = cmds
        print(tree[m_id][0].color)
    else:
        answer = 0
        for x in root:
            score(x.id, set())
        print(answer)
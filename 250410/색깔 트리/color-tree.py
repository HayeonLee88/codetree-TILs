'''
12:55~
(1) 노드추가
Node: idx, parent_id, color, max_d
color: 빨 1, 주 2, 노 3, 초 4, 파 5
if Parent_id == -1: Node = root
max_depth: subtree의 최대 깊이, 자기자신은 1
    - 기존 노드의 Max_depth와 충돌이 되는 새로운 노드는 연결하지 않음
자신의 subtree를 알고 있어야 함.

100 idx p_id color max_d

(2) 색깔 변경
idx의 모든 subtree의 색을 idx 노드의 색으로 바꿈

200 idx color

(3) 색깔 조회
특정 노드 idx의 현재 색을 조회

300 idx

(4) 점수 조회
모든 노드의 가치를 계산하여 가치 제곱의 합을 출력
각 노드의 가치는 해당 노드를 루트로 하는 서브트리 내 서로 다른 색깔의 수로 정의

400
'''
import sys

input = lambda:sys.stdin.readline().rstrip()

q = int(input())


class Node():
    def __init__(self, id, p_id, color, max_d):
        self.id = id
        self.p_id = p_id
        self.color = color
        self.max_d = max_d
        self.depth = 1

    def set_color(self,color):
        self.color = color

    def set_subtree(self):
        self.subtree += 1

tree = [[] for _ in range(100000)]


def dfs(x, color):
    tree[x][0].color = color
    for sub in tree[x][1:]:
        dfs(sub.id, color)


'''
5(4): 19(3), 10(2): 1(1), 9(1) : 4(2) : 14(1)
2(1)
16(1)

'''
answer = 0

def score(x, cnt):
    global answer
    cnt.add(tree[x][0].color)
    if len(tree[x]) == 1:
        answer += 1
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
            root.append(Node(m_id, p_id, color, max_d))
            tree[m_id].append(root[-1])
        else:
            if len(tree[p_id]) == 1:
                depth = 1
                now = tree[p_id][0]
                check = True
                while True:
                    if depth + 1 > now.max_d:
                        check = False
                        break
                    if now.p_id == -1:
                        break
                    now = tree[now.p_id][0]
                    depth += 1
                    
                if check:
                    now = tree[p_id][0]
                    depth = 1
                    while True:
                        if depth + 1 > now.depth:
                            now.depth += 1
                        if now.p_id == -1:
                            break
                        now = tree[now.p_id][0]
                        depth += 1 
                    new = Node(m_id, p_id, color, max_d)
                    tree[m_id].append(new)
                    tree[p_id].append(new)

            else:
                new = Node(m_id, p_id, color, max_d)
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
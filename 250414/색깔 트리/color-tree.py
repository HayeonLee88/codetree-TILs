import sys

input = lambda:sys.stdin.readline().rstrip()

q = int(input())

# 트리의 노드
class Node():
		'''
		id: 노드 id
		p_id: 노드의 부모 id
		color: 노드의 색
		max_d: 노드의 서브트리가 가질 수 있는 최대 깊이
		depth: 노드의 현재 깊이
		'''
    def __init__(self, id, p_id, color, max_d):
        self.id = id
        self.p_id = p_id
        self.color = color
        self.max_d = max_d
        self.depth = 1

tree = [[] for _ in range(100001)]


# 모든 서브트리의 색 바꾸기
def dfs(x, color):
		'''
		x: 색을 바꿀 Node의 id
		color: 새로 바꿀 색
		'''
    tree[x][0].color = color
    for sub in tree[x][1:]:
        dfs(sub.id, color)

answer = 0

# 각 노드의 서브트리 색 종류에 따른 점수 합 구하기
def score(x, cnt):
		'''
		x: 서브트리의 점수를 구할 Node의 id
		cnt: 서브트리의 색 종류 가지수
		'''
    global answer
    cnt.add(tree[x][0].color)
    if len(tree[x]) == 1:
        answer += 1
    else:
        for sub in tree[x][1:]:
            tmp = set()
            cnt.add(sub.color)
            score(sub.id, tmp) # Node의 자식들의 색 종류에 따른 점수 구하기
            cnt.update(list(tmp))
        answer += len(cnt) * len(cnt)
    return answer


root = []
for _ in range(q):
    cmds = list(map(int, input().split()))
    cmd = cmds[0]
    if cmd == 100:
        _, m_id, p_id, color, max_d = cmds
        if p_id == -1: # 부모가 없는 root일 때
            root.append(Node(m_id, p_id, color, max_d))
            tree[m_id].append(root[-1])
        else: # 부모가 있을 때
            if len(tree[p_id]) == 1: # 부모의 자식이 아직 없는 상태라면
                depth = 1
                now = tree[p_id][0]
                check = True
                while True: # 상위 노드들의 최대 깊이 확인
                    if depth + 1 > now.max_d:
                        check = False
                        break
                    if now.p_id == -1:
                        break
                    now = tree[now.p_id][0]
                    depth += 1
                    
                if check: # 새로운 노드를 이을 수 있다면
                    now = tree[p_id][0]
                    depth = 1
                    while True: # 상위 부모 노드들의 depth 갱신
                        if depth + 1 > now.depth:
                            now.depth += 1
                        else: break
                        if now.p_id == -1:
                            break
                        now = tree[now.p_id][0]
                        depth += 1 
                    # 새로운 node 추가
                    new = Node(m_id, p_id, color, max_d)
                    tree[m_id].append(new)
                    tree[p_id].append(new)

            else: # 부모의 자식이 있는 상태라면 바로 새로운 node 추가
                new = Node(m_id, p_id, color, max_d)
                tree[m_id].append(new)
                tree[p_id].append(new)

    elif cmd == 200: # 서브트리를 지정된 색으로 모두 바꾸기
        _, m_id, color = cmds
        dfs(m_id, color)
                  
    elif cmd == 300: # id를 가진 node의 색을 출력하기
        _, m_id = cmds
        print(tree[m_id][0].color)
    else: # 모든 트리의 점수를 계산하기
        answer = 0
        for x in root:
            score(x.id, set())
        print(answer)
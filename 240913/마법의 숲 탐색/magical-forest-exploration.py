import sys
from collections import deque

input = lambda:sys.stdin.readline().rstrip()

r, c, k = map(int, input().split())

graph = []
graph2 = []
dirs = []

def reset():
    global graph, graph2, dirs
    graph = []
    graph.append([True] * (c + 2))
    for i in range(r):
        graph.append([False] + [True] * c + [False])
    graph.append([False] * (c + 2))

    graph2 = [[-1] * (c + 2) for _ in range(r + 2)]
    dirs = [[] for _ in range(k)]

reset()

dir = {0:[-1, 0], 1:[0, 1], 2:[1, 0], 3:[0, -1]}
m_type = {0: 0, 1: -1, 2: 1, 3: 0}
dx = [-1, 0, 1, 0]
dy = [0, 1, 0, -1]

def move_golem(x, y):
    global graph
    if x < 0:
        if graph[x + 2][y]:
            return [x + 1, y, 0]
        elif graph[x + 1][y - 2] and graph[x + 2][y - 1]:
            return [x + 1, y - 1, 1]
        elif graph[x + 1][y + 2] and graph[x + 2][y + 1]:
            return [x + 1, y + 1, 2]
        else:
            return [x, y, 3]
    else:
        if graph[x + 1][y - 1] and graph[x + 2][y] and graph[x + 1][y + 1]:
            return [x + 1, y, 0]
        elif graph[x - 1][y - 1] and graph[x][y - 2] and graph[x + 1][y - 1] and graph[x + 1][y - 2] and graph[x + 2][y - 1]:
            return [x + 1, y - 1, 1]
        elif graph[x - 1][y + 1] and graph[x][y + 2] and graph[x + 1][y + 1] and graph[x + 1][y + 2] and graph[x + 2][y + 1]:
            return [x + 1, y + 1, 2]
        else:
            return [x, y, 3]


def move_spirit(x, y, idx):
    answer = x
    q = deque()
    q.append([x, y, idx])
    while q:
        x, y, idx = q.popleft()
        ex, ey = dirs[idx]
        answer = max(x + 1, answer)
        for i in range(4):
            nx = ex + dx[i]
            ny = ey + dy[i]
            g_idx = graph2[nx][ny]
            if g_idx not in [idx, -1]:
                q.append([nx + dx[i], ny + dy[i], g_idx])
    return answer

answer = 0
for i in range(k):
    pos_x = -1
    pos_y, d = map(int, input().split())
    dirs[i] = [pos_x + dir[d][0], pos_y + dir[d][1]]
    while True:
        x, y, m = move_golem(pos_x, pos_y)
        d = (d + m_type[m]) % 4
        dirs[i] = [x + dir[d][0], y + dir[d][1]]
        if m == 3 or x == r - 1:
            if x < 2:
                reset()
                break
            graph[x][y] = False
            graph2[x][y] = i
            for j in range(4):
                graph[x + dx[j]][y + dy[j]] = False
                graph2[x + dx[j]][y + dy[j]] = i
            answer += move_spirit(x, y, i)
            break
        pos_x, pos_y = x, y


print(answer)
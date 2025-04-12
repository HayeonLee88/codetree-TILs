from collections import deque

K, M = map(int, input().split())
graph = [list(map(int, input().split())) for _ in range(5)]
wall = deque(map(int, input().split()))

visited = [[False] * 5 for _ in range(5)]
points = [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

answer = 0

def rotate_90(x):
    x = list(zip(*x[::-1]))
    return x

def rotate_180(x):
    x = list(zip(*x[::-1]))
    x = list(zip(*x[::-1]))
    return x

def rotate_270(x):
    x = list(zip(*x))[::-1]
    return x

def bfs1(x, y, map1, visited):
    set_ = set()
    q = deque()
    q.append((x, y))
    set_.add((x, y))
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx > 4 or ny < 0 or ny > 4:
                continue
            if not visited[nx][ny] and map1[nx][ny] == map1[x][y]:
                q.append((nx, ny))
                visited[nx][ny] = True
                set_.add((nx, ny))
    if len(set_) >= 3:
        return len(set_)
    else:
        return 0
    
def bfs2(x, y, visited):
    set_ = set()
    q = deque()
    q.append((x, y))
    set_.add((x, y))
    while q:
        x, y = q.popleft()
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if nx < 0 or nx > 4 or ny < 0 or ny > 4:
                continue
            if not visited[nx][ny] and graph[nx][ny] == graph[x][y]:
                q.append((nx, ny))
                set_.add((nx, ny))
                visited[nx][ny] = True
    if len(set_) >= 3:
        return len(set_), set_
    else:
        return 0, set()
    
def sort_points(x):
    x.sort(reverse=True, key=lambda x: x[0])
    x.sort(key=lambda x: x[1])

def chain_gems(graph):
    global answer
    while True:
        set_ = set()
        visited = [[False] * 5 for _ in range(5)]
        cnt = 0
        for i in range(5):
            for j in range(5):
                visited[i][j] = True
                a, tmp = bfs2(i, j, visited) 
                cnt += a
                set_.update(tmp)
        if cnt > 0:
            set_ = list(set_)
            sort_points(set_)
            for x, y in set_:
                new = wall.popleft()
                graph[x][y] = new
            answer += cnt
        else:
            break

for i in range(K):
    answer = 0
    p = [-1, [-1, -1]]
    max_ = 0
    for num in range(3):
        for x, y in points:
            sub = []
            for j in range(x - 1, x + 2):
                sub.append(graph[j][y - 1: y + 2])
            if num == 0:
                sub = rotate_90(sub)
            elif num == 1:
                sub = rotate_180(sub)
            else:
                sub = rotate_270(sub)
            tmp_g = [row[:] for row in graph]
            for k in range(x - 1, x + 2):
                for l in range(y - 1, y + 2):
                    tmp_g[k][l] = sub[k + 1 - x][l + 1 - y]
            visited = [[False] * 5 for _ in range(5)]
            tmp = 0
            for k in range(5):
                for l in range(5):
                    visited[k][l] = True
                    tmp += bfs1(k, l, tmp_g, visited)
            if max_ < tmp:
                max_ = tmp
                p = [num, [x, y]]
    num, point = p
    x, y = point
    sub = []
    for j in range(x - 1, x + 2):
        sub.append(graph[j][y - 1: y + 2])
    if num == 0:
        sub = rotate_90(sub)
    elif num == 1:
        sub = rotate_180(sub)
    elif num == 2:
        sub = rotate_270(sub)
    else:
        break
    for k in range(x - 1, x + 2):
        for l in range(y - 1, y + 2):
            graph[k][l] = sub[k + 1 - x][l + 1 - y]
    chain_gems(graph)
    print(answer, end=' ')
    
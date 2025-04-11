from collections import deque
r, c, k = map(int, input().split())
graph = []

def new_map():
    global graph
    graph = [[0] * (c + 2) for _ in range(r + 3)]

    for i in range(r + 3):
        for j in [0, c + 1]:
            graph[i][j] = -1

for row in graph:
    for x in row:
        print(x, end=' ')
    print()


exit = []
g_dirs = {0: [(1, -1), (1, 1), (2, 0)], 1: [(-1, 0), (0, -2), (1, -1), (1, -2), (2, -1)], 2:[(-1, 1), (1, 1), (0, 2), (2, 1), (1, 2)]}
g_move = {0: [1, 0], 1: [1, -1], 2: [1, 1]}
e_dirs = {0: 0, 1: -1, 2: 1}
dirs = [0, 1, 2, 3]

dx = [-1, 0, 1, 0, 0]
dy = [0, 1, 0, -1, 0]

visited = []

def move_golrem(x, y, dir):
    for dx, dy in g_dirs[dir]:
        nx = dx + x
        ny = dy + y
        if graph[nx][ny] != 0:
            return False
    return True


def move_fairy(x, y):
    global visited
    q = deque()
    q.append((x, y))
    visited[x][y] = True
    answer = x - 2
    while q:
        x, y = q.popleft()
        now = graph[x][y]
        if now == -2:
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 < nx < r + 3 and 0 < ny < c + 1: 
                    if not visited[nx][ny]:
                        if graph[nx][ny] != 0:
                            answer = max(nx - 2, answer)
                            visited[nx][ny] = True
                            # 중앙으로 이동
                            for i in range(4):
                                tx = nx + dx[i]
                                ty = ny + dy[i]
                                if 0 < tx < r + 3 and 0 < ty < c + 1: 
                                    if not visited[tx][ty]:
                                        if graph[nx][ny] == graph[tx][ty]:
                                            answer = max(tx - 2, answer)
                                            visited[tx][ty] = True
                                            q.append((tx, ty))
                                            break
        else:               
            for i in range(4):
                nx = x + dx[i]
                ny = y + dy[i]
                if 0 < nx < r + 3 and 0 < ny < c + 1: 
                    if not visited[nx][ny]:
                        if graph[nx][ny] == -2:
                            q.append((nx, ny))
                        elif graph[nx][ny] == now:
                            pass
                        else:
                            continue
                        answer = max(nx - 2, answer)
                        visited[nx][ny] = True
    return answer

new_map()

answer = 0
for i in range(k):
    check = True # 골렘 위치 표시
    c_i, d_i = map(int, input().split())
    r_i = 1
    while r_i < r + 1:
        for j in range(3):
            if move_golrem(r_i, c_i, j):
                nr_i, nc_i = r_i + g_move[j][0], c_i + g_move[j][1]
                d_i = (d_i + e_dirs[j]) % 4
                break
        if nr_i == r_i: # 아래로 이동 불가
            if r_i < 4:
                check = False
            break
        r_i, c_i = nr_i, nc_i
    if check: 
        # 골렘이 멈춘 위치 표시하기
        for j in range(5):
            if d_i == j: # 출구
                graph[r_i + dx[j]][c_i + dy[j]] = -2
                continue
            graph[r_i + dx[j]][c_i + dy[j]] = i + 1
        visited = [[False] * (c + 2) for _ in range(r + 3)]
        exit.append([r_i, c_i, d_i])
        tmp = move_fairy(r_i, c_i)
        answer += tmp
    else:
        new_map()

print(answer)
import queue
import random


def bfs(adj, start):
    visited = set()
    q = queue.Queue()
    q.put(start)  # 把起始点放入队列
    while not q.empty():
        u = q.get()

        print('u',u)
        # print('adj.get(u, [])',adj.get(u, []))
        a=adj.get(u, [])

        random.shuffle(a)
        print('a', a)
        for v in a:
            # print('v',v)
            if v not in visited:
                visited.add(v)
                q.put(v)

if __name__=='__main__':
    nodes = [[], [2, 3], [3, 4, 5], [5, 6], [7, 8], [4, 6], [7, 9], [8, 9], [9, 10], [10]]
    graph={index:each for index ,each in enumerate(nodes)}
    # graph = {1: [4, 2], 2: [3, 4], 3: [4], 4: [5]}
    print('graph',graph)
    bfs(graph, 1)
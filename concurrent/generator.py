from collections import deque


def count_down(n):
    for i in range(n-1, -1, -1):
        yield i

def run():
    dq = deque()
    dq.extend([count_down(20),count_down(5),count_down(10)])
    while dq:
        task = dq.popleft()
        try:
            num = next(task)
            print(num)
            dq.append(task)
        except StopIteration:
            pass
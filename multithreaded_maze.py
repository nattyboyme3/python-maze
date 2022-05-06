from queue import Queue
import line_maze
from threading import Thread
import time

w = 50
h = 50
i = 500
t = 15


def generate_maze(q, output_length, output_maze):
    while not q.empty():
        job_id = q.get(block=False)
        m = line_maze.LineMaze(w, h, optimize=True)
        output_length[job_id] = m.length
        output_maze[job_id] = m
        q.task_done()


if __name__ == '__main__':
    q = Queue(maxsize=0)
    lengths = list()
    mazes = list()

    for x in range(i):
        lengths.append(None)
        mazes.append(None)
        q.put(x)

    for thread in range(t):
        worker = Thread(target=generate_maze, args=(q, lengths, mazes))
        worker.setDaemon(True)
        worker.start()
        time.sleep(0.1)

    while not q.empty():
        time.sleep(3)
        print(f"queue is length {q.qsize()}")

    time.sleep(10)
    best = -1
    for i in range(len(lengths)):
        if lengths[i] > best:
            best = i
    best_maze = mazes[best]
    best_maze.draw(solved=True)
    best_maze.draw(solved=False)
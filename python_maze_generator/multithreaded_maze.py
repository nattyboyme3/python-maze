import sys
from queue import Queue
from python_maze_generator.line_maze import LineMaze
from threading import Thread
import time
import argparse


def build_maze(q, output_length, output_maze, h, w):
    while not q.empty():
        job_id = q.get(block=False)
        m = LineMaze(h, w, optimize=True)
        output_length[job_id] = m.length
        output_maze[job_id] = m
        q.task_done()


def generate_mazes(height, width, iterations, threads) -> LineMaze:
    q = Queue(maxsize=0)
    lengths = list()
    mazes = list()
    for x in range(iterations):
        lengths.append(None)
        mazes.append(None)
        q.put(x)
    for thread in range(threads):
        worker = Thread(target=build_maze, args=(q, lengths, mazes, height, width))
        worker.setDaemon(True)
        worker.start()
        time.sleep(0.1)
    while q.unfinished_tasks > 0:
        time.sleep(3)
        any_finished = [x for x in lengths if x]
        if any_finished:
            print(f"Mazes yet to generate: {q.qsize()}. Best: {max(any_finished)}")
    best = -1
    for i in range(len(lengths)):
        if lengths[i] > lengths[best]:
            best = i
    return mazes[best]


if __name__ == '__main__':
    sys.setrecursionlimit(10**6)
    a = argparse.ArgumentParser()
    a.add_argument('-H', '--height', default=50, type=int, help='how high to make the maze')
    a.add_argument('-W', '--width', default=50, type=int, help='how wide to make the maze')
    a.add_argument('-I', '--iterations', default=100, type=int, help='how many times to try')
    a.add_argument('-T', '--threads', default=10, type=int, help='how many threads to spawn')
    args = a.parse_args()
    end = time.time()
    best_maze = generate_mazes(args.height, args.width, args.iterations, args.threads)
    start = time.time()
    best_maze.draw(solved=True)
    best_maze.draw(solved=False)
    e_time = int(end - start)
    a_time = float(e_time) / args.iterations
    print(f"Generated {args.iterations} {args.height} by {args.width} mazes in {e_time} seconds "
          f"using {args.threads} threads, average {a_time} seconds, solution length: {best_maze.length}")
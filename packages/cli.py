import argparse
import sqlite3
import time
from packages.rqg import get_random_query


def main():
    parser = argparse.ArgumentParser(
        description="A Command Line Tool for Fuzz Testing")
    parser.add_argument("path", metavar='path', type=str, help="database path")
    parser.add_argument('num', metavar='num', type=int,
                        help='number of random SQL quries')
    args = parser.parse_args()

    conn = sqlite3.connect(args.path)
    for _ in range(args.num):
        cursor = conn.cursor()
        q = get_random_query()
        print(f"Executing: {q}")
        start_time = time.time_ns()
        cursor.execute(q)
        end_time = time.time_ns()
        print(f"Number of entries: {len(cursor.fetchall())}")
        print(f"Execution time(ns): {end_time - start_time}")
        print("----------")
    conn.close()


if __name__ == '__main__':
    main()

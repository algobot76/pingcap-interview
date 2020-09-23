import argparse
import random
import sqlite3
import time
from packages.rqg import MAX_C_LENGTH, get_random_query
from packages.utils import get_random_string
from pathlib import Path


def fuzz():
    parser = argparse.ArgumentParser(
        description="A Command Line Tool for Fuzz Testing")
    parser.add_argument("path", metavar='path', type=str, help="database path")
    parser.add_argument('num', metavar='num', type=int,
                        help='number of random SQL quries')
    args = parser.parse_args()

    if not Path(args.path).is_file():
        print(f"The path \"{args.path}\" is not a file.")
        return

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


def seed():
    parser = argparse.ArgumentParser(
        description="A Command Line Tool for Generating a Databasae with Random Data")
    parser.add_argument("path", metavar='path', type=str, help="database path")
    parser.add_argument('num', metavar='num', type=int,
                        help='number of random entries')
    args = parser.parse_args()

    if Path(args.path).is_dir():
        print(f"The path \"{args.path}\" is a directory not a file.")
        return

    if Path(args.path).is_file():
        print(f"The database \"{args.path}\" already exists.")
        return

    conn = sqlite3.connect(args.path)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS t (a INTEGER, b INTEGER, c VARCHAR(10));")
    conn.commit()
    for _ in range(args.num):
        cursor.execute(
            f"INSERT INTO t (a, b, c) VALUES({random.randint(-100, 100)}, {random.randint(-100, 100)}, '{get_random_string(random.randint(1, MAX_C_LENGTH))}')")
        conn.commit()

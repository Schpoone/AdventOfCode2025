#!/usr/bin/python3

import requests
import os
import sys
from dotenv import load_dotenv

load_dotenv()
session_id = os.environ['session_id']

# Verify we're getting input
if len(sys.argv) != 2:
    print('Missing day number. Run e.g:')
    print('python3 setup_day.py 13')
    sys.exit(2)

day = str(sys.argv[1])
path = "day" + day

# Create folder for the day
if not os.path.isdir(path):
    os.mkdir(path)

# Create template files
if not os.path.exists(os.path.join(path, "script.py")):
    os.system(f"cp template.py {path}/{path}.py")

if not os.path.exists(os.path.join(path, "example1.txt")):
    os.system(f"touch {path}/example1.txt")

if not os.path.exists(os.path.join(path, "example2.txt")):
    os.system(f"touch {path}/example2.txt")

url = f"https://adventofcode.com/2025/day/{day}/input"

# Get the input
with open(f"{path}/input.txt", "w") as f:
    response = requests.get(url, cookies={"session": session_id})
    response.raise_for_status()
    f.write(response.text)

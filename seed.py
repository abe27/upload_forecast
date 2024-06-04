import os
from os.path import join, dirname
import subprocess

def main():
    sDir = join(dirname(__file__), '')
    dir = os.listdir(f"{sDir}/seed/")
    dir.sort()
    for dd in dir:
        files = [f for f in os.listdir(f"{sDir}/seed/{dd}")]
        files.sort()
        for f in files:
            fname = f"{sDir}/seed/{dd}/{f}"
            strCmd = f"python manage.py loaddata {fname}"
            print(strCmd)

if __name__ == '__main__':
    main()
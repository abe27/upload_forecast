import os
import subprocess

def main():
    dir = os.listdir("seed/")
    dir.sort()
    for dd in dir:
        files = [f for f in os.listdir(f"seed/{dd}")]
        for f in files:
            fname = f"seed/{dd}/{f}"
            strCmd = f"python manage.py loaddata {fname}"
            print(strCmd)

if __name__ == '__main__':
    main()
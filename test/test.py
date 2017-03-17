import sys
import subprocess

#params = [x for pair in d.items() if all(pair) for x in pair]
subprocess.check_call([sys.executable, "print.py", "hello"], shell=False)
import os
import sys
from io import StringIO
import time

import gui

<<<<<<< HEAD
gui.main()
=======

# gui.main()
f = open("test.py", "r")
content = f.readlines()
f.close()

f = open("test-Copy.py", "w+")
f.write(
    """\
import sys
from io import StringIO
class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio
        sys.stdout = self._stdout


with Capturing() as output:  
""")
for i in content:
    f.write("   " + i)

f.write(
"""\
try:
    assert output[0] == 30
    print("Correct!")
except AssertionError:
    print("Wrong!")
"""
)
f.close()

os.system('python test-Copy.py')
os.remove('test-Copy.py')
>>>>>>> 5f55b4f21b0f732513134ac9845c7978bdd29387

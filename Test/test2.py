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
    print('Hello')
try:    
    assert output[0] == 'Hello')
    print("Đúng!")
except AssertionError:
    print("Sai!")
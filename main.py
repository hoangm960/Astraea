import os
import gui


def main():

    def check_file(file, ans):
        def get_file_content():
            f = open(file, "r")
            content = f.readlines()
            f.close()
            return content

        def make_check_file():
            f = open(os.path.splitext(file)[0] + "-Copy.py", "w+")
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
            for i in get_file_content():
                f.write("   " + i)

            f.write(
"""\
try:
    assert output[0] == str(""" + str(ans) + ")\n"
"""\
    print("Correct!")
except AssertionError:
    print("Wrong!")
""")
            f.close()

        def run_check_file():
            os.system('python test-Copy.py')
            os.remove('test-Copy.py')

        make_check_file()
        run_check_file()


    check_file("test.py", 40)


# gui.Main()
main()

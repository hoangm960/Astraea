import os
import gui, Login



def main(file, inputs, ans, tests, vars):
    def get_file_content(file):
        f = open(file, "r")
        content = f.readlines()
        f.close()
        return content

    def get_testcases_file():
        f = open(os.path.splitext(inputs)[0] + "-Copy.txt", "w+")
        for i in get_file_content(inputs):
            f.write(i)

    def del_testcases_file():
        os.remove(os.path.splitext(inputs)[0] + "-Copy.txt")

    def check_file(file, ans):
        def make_check_file(test):
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
"""
            )
            for i in get_file_content(file):
                f.write("   " + i)

            f.write(
                """\
try:
    assert output[0] == str("""
                + open(ans, "r").readlines()[test]
                + ")\n"
                """\
    print("Đúng!")
except AssertionError:
    print("Sai!")
"""
            )
            f.close()

        def run_check_file():
            os.system(
                "python " + os.path.splitext(file)[0] + "-Copy.py" + " < " + os.path.splitext(inputs)[0] + "-Copy.txt"
            )
            os.remove("test-Copy.py")

        def delete_done_testcases():
            with open(os.path.splitext(inputs)[0] + "-Copy.txt", "r") as f:
                lines = f.readlines()
            for _ in range(vars):
                del lines[0]
            with open(os.path.splitext(inputs)[0] + "-Copy.txt", "w+") as f:
                for line in lines:
                    f.write(line)

        for test in range(tests):
            make_check_file(test)
            run_check_file()
            delete_done_testcases()

    get_testcases_file()
    check_file(file, ans)
    del_testcases_file()


# Login.main()
# gui.Main()

test_file = "test.py"
input_file = "Inputs.txt"
ans_file = "Ans.txt"
test_cases = 2
vars = 2
main(test_file, input_file, ans_file, test_cases, vars)

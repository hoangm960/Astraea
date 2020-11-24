import os
from subprocess import PIPE, Popen, TimeoutExpired, check_output, run


class MainFunc:
    results = []
    def __init__(
        self,
        filename,
        input_file,
        ans_file,
        tests,
        ex_file,
        timeout=2,
        vars=0,
        size_range=50,
    ):
        self.filename = filename
        self.input_file = input_file
        self.ans_file = ans_file
        self.tests = tests
        self.ex_file = ex_file
        self.timeout = timeout
        self.vars = vars
        self.size_range = size_range

    def get_file_content(self, file):
        f = open(file, "r")
        content = f.readlines()
        f.close()
        return content

    def get_copy_file(self, filename):
        with open(os.path.splitext(filename)[0] + "-Copy.txt", "w+") as f:
            for i in self.get_file_content(filename):
                f.write(i)
        return os.path.splitext(filename)[0] + "-Copy.txt"

    def del_copied_file(self, filename):
        os.remove(os.path.splitext(filename)[0] + "-Copy.txt")

    def get_input(self):
        input = ""
        input_copied_file = self.get_copy_file(self.input_file)
        with open(input_copied_file, "r") as f:
            lines = f.readlines()
            for _ in range(self.vars):
                input += lines[0]
                del lines[0]
        with open(input_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return input

    def get_ans(self):
        ans_copied_file = self.get_copy_file(self.ans_file)
        with open(ans_copied_file, "r") as f:
            lines = f.readlines()
            ans = lines[0]
            del lines[0]
        with open(ans_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return ans

    def check(self, input, ans):
        output = ""
        timeout = correct = optimize = False
        self.result = (timeout, correct, optimize)
        try:
            process = Popen(
                ["python", self.filename], stdin=PIPE, stdout=PIPE, encoding="utf8"
            )
            output = process.communicate(input=input, timeout=timeout)[0]
        except TimeoutExpired:
            self.check.result[0] = True

        self.check.result[1] = True if output.rstrip() == ans.rstrip() else False
        self.check_file_size()

    def check_file_size(self):
        file_size = os.stat(self.filename).st_size
        ex_file_size = os.stat(self.ex_file).st_size
        self.check.result[2] = (
            True
            if file_size
            in range(ex_file_size - self.size_range, ex_file_size + self.size_range)
            else False
        )

    def main(self):
        for _ in range(self.tests):
            self.check(self.get_input(), self.get_ans())
        self.del_copied_file(self.input_file)
        self.del_copied_file(self.ans_file)


if __name__ == "__main__":
    MainFunc(
        filename="test.py",
        ex_file="data/Lesson/example.py",
        input_file="data/check algorithm/Inputs.txt",
        ans_file="data/check algorithm/Ans.txt",
        tests=3,
        vars=2,
    ).main()


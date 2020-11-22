import os
from subprocess import PIPE, Popen


def main(filename, ex_file, size_range, input_file, ans_file, tests, vars):
    def get_file_content(file):
        f = open(file, "r")
        content = f.readlines()
        f.close()
        return content

    def get_copy_file(filename):
        with open(os.path.splitext(filename)[0] + "-Copy.txt", "w+") as f:
            for i in get_file_content(filename):
                f.write(i)
        return os.path.splitext(filename)[0] + "-Copy.txt"

    def del_copied_file(filename):
        os.remove(os.path.splitext(filename)[0] + "-Copy.txt")

    def get_input():
        input = ""
        input_copied_file = get_copy_file(input_file)
        with open(input_copied_file, "r") as f:
            lines = f.readlines()
            for _ in range(vars):
                input += lines[0]
                del lines[0]
        with open(input_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return input

    def get_ans():
        ans_copied_file = get_copy_file(ans_file)
        with open(ans_copied_file, "r") as f:
            lines = f.readlines()
            ans = lines[0]
            del lines[0]
        with open(ans_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return ans

    def check(input, ans):
        with open(input_file) as f:
            output = (
                Popen("python " + filename, stdout=PIPE, stdin=PIPE)
                .communicate(bytes(input, "utf8"))[0]
                .decode()
                .rstrip()
            )
        try:
            assert output == ans
            print("Đúng.")
        except AssertionError:
            print("Sai.")

    def check_file_size():
        file_size = os.stat(filename).st_size
        ex_file_size = os.stat(ex_file).st_size
        if file_size in range(ex_file_size - size_range, ex_file_size + size_range):
            print("Thuật toán đã tối ưu hóa.")
        else:
            print("Thuật toán chưa tối ưu hóa.")

    for _ in range(tests):
        check(get_input(), get_ans())
    del_copied_file(input_file)
    del_copied_file(ans_file)
    check_file_size()


if __name__ == "__main__":
    main(
        filename="test.py",
        ex_file="data/Lesson/example.py",
        size_range=10,
        input_file="data/check algorithm/Inputs.txt",
        ans_file="data/check algorithm/Ans.txt",
        tests=1,
        vars=2,
    )


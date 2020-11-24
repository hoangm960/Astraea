import os
from subprocess import PIPE, Popen, TimeoutExpired, check_output, run


def main(filename, input_file, ans_file, tests, ex_file, timeout=2, vars=0, size_range=50):
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
            output = ''
            try:
                process = check_output(["python", filename], input=input, timeout=timeout)
                output = process.rstrip()
            except TimeoutExpired:
                print("Chạy quá thời gian.\nSai.")
                return
        try:
            assert output == ans
            print("Đúng.")
            check_file_size()
        except AssertionError:
            print("Sai.")

    def check_file_size():
        file_size = os.stat(filename).st_size
        ex_file_size = os.stat(ex_file).st_size
        if file_size in range(ex_file_size - size_range, ex_file_size + size_range):
            print("Bài làm đã tối ưu hóa.")
        else:
            print("Bài làm chưa tối ưu hóa.")

    for _ in range(tests):
        check(get_input(), get_ans())
    del_copied_file(input_file)
    del_copied_file(ans_file)


if __name__ == "__main__":
    main(
        filename="test.py",
        ex_file="data/Lesson/example.py",
        input_file="data/check algorithm/Inputs.txt",
        ans_file="data/check algorithm/Ans.txt",
        tests=1,
        vars=2,
    )


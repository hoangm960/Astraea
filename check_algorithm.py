import os
from subprocess import PIPE, Popen, TimeoutExpired, check_output, run


def main(
    filename, input_file, ans_file, tests, ex_file, time_limit=1, vars=0, size_range=50
):
    main.results = []

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

    def get_input(input_copied_file):
        input = ""
        with open(input_copied_file, "r") as f:
            lines = f.readlines()
            for _ in range(vars):
                input += lines[0]
                del lines[0]
        with open(input_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return input

    def get_ans(ans_copied_file):
        with open(ans_copied_file, "r") as f:
            lines = f.readlines()
            ans = lines[0]
            del lines[0]
        with open(ans_copied_file, "w") as f:
            for line in lines:
                f.write(line)
        return ans

    def check(input, ans):
        output = ""
        time_err = correct = False
        check.result = [time_err, correct]
        try:
            process = Popen(
                ["python", filename], stdin=PIPE, stdout=PIPE, encoding="utf8"
            )
            output = process.communicate(input=input, timeout=time_limit)[0]
        except TimeoutExpired:
            check.result[0] = True

        check.result[1] = True if output.rstrip() == ans.rstrip() else False

    def check_file_size():
        file_size = os.stat(filename).st_size
        ex_file_size = os.stat(ex_file).st_size
        main.results.append(
            True
            if file_size in range(ex_file_size - size_range, ex_file_size + size_range)
            else False
        )

    copied_input_file = get_copy_file(input_file)
    copied_ans_file = get_copy_file(ans_file)
    for _ in range(tests):
        check(get_input(copied_input_file), get_ans(copied_ans_file))
        main.results.append(check.result)
    check_file_size()
    del_copied_file(input_file)
    del_copied_file(ans_file)
    return main.results


if __name__ == "__main__":
    print(
        main(
            filename="test.py",
            ex_file="data/Lesson/example.py",
            input_file="data/check algorithm/Inputs.txt",
            ans_file="data/check algorithm/Ans.txt",
            tests=1,
            vars=0,
        )
    )


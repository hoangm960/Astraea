import os
from subprocess import PIPE, Popen, TimeoutExpired, check_output, run


def main(filename, ex_file, tests, time_limit=2, size_range=50):
    main.results = []

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

    for test in tests:
        input = output = ''
        for i in test.inputs:
            input += i + "\n"
        for i in test.outputs:
            output += i + "\n"
        check(input, output)
        main.results.append(check.result)

    if (not result[1] for result in main.results):
        check_file_size()
    else:
        main.results.append(False)
    return main.results



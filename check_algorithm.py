import os
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired


def main(filename, ex_file, tests, time_limit=2, size_range=50):
    main.results = []

    def get_command():
        program_langs = {".py": "python", ".pas": "fpc"}
        command = [program_langs[os.path.splitext(filename)[1]], filename]
        return command

    def get_output(command, input=''):
        output = ''
        try:
            process = Popen(
                command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding = 'utf8'
            )
            output = process.communicate(input=input, timeout=time_limit)[0]
        except TimeoutExpired:
            check.result[0] = True

        return output

    def check(input, ans):
        time_err = correct = False
        check.result = [time_err, correct]

        command = get_command()
        output = get_output(command, input)
        base_file = os.path.splitext(filename)[0]
        if command[0] == "fpc":
            command = [base_file]
            output = get_output(command, input)
            os.remove(f'{base_file}.o')
            os.remove(f'{base_file}.exe')

        check.result[1] = True if output.rstrip() == ans.rstrip() else False

    def check_file_size():
        if True in [result[1] for result in main.results]:
            file_size = os.stat(filename).st_size
            ex_file_size = os.stat(ex_file).st_size
            main.results.append(
                True
                if file_size in range(ex_file_size - size_range, ex_file_size + size_range)
                else False
            )
        else:
            main.results.append("")

    for test in tests:
        input = output = ''
        for i in test.inputs:
            input += i + "\n"
        for i in test.outputs:
            output += i + "\n"
        check(input, output)
        main.results.append(check.result)

    check_file_size()
    return main.results

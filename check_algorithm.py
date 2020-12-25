import os
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired


def main(filename, inputs, outputs, time_limit=2):
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
        except Exception:
            return False
        finally:
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

    input, output = '\n'.join(inputs) if inputs else '', '\n'.join(outputs)
    check(input, output)
    main.results.append(check.result)

    return main.results

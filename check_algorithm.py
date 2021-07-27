import os
import re
from subprocess import PIPE, STDOUT, Popen, TimeoutExpired

ANSWer = ''
Cor = ''

def main(filename, tests, infos, time_limit=2):
    main.results = []

    def get_command():
        program_langs = {".py": "python", ".pas": "fpc"}
        command = [program_langs[os.path.splitext(filename)[1]], filename]
        return command

    def get_output(command, input=''):
        output = ''
        try:
            process = Popen(
                command, stdin=PIPE, stdout=PIPE, stderr=STDOUT, encoding='utf8'
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
        if not check.result[1]:
            with open('./data/results/comment.txt', 'r', encoding='utf-8', errors='ignore') as f:
                list_file = f.readlines()
                if 'SAI' not in list_file[-1]:
                    with open('./data/results/comment.txt', 'a+', encoding='utf-8', errors='ignore') as file_error_w:
                        file_error_w.write('\n>>> SAI ĐÁP ÁN: "'+output.rstrip()+'" phải là "'+ans.rstrip()+'"...')
                        
    def check_info(info):
        key, message, num = (i for i in info)
        data = open(filename, encoding='utf8').read()
        data = [i for i in re.split('[;()\s]\s*', data) if i]
        if data.count(key) < int(num):
            check_info.info.append(message)

    for test in tests:
        inputs, outputs = (test[i] for i in range(len(test)))
        input = '\n'.join(inputs) if inputs else ''
        if outputs:
            output = '\n'.join(outputs)
        else:
            break
        check(input, output)
        check_info.info = []
        if infos:
            for info in infos:
                check_info(info)
        main.results.append(check.result)

    return main.results, check_info.info


if __name__ == "__main__":
    filename = "C:/Users/Admin/Desktop/test.py"
    tests = [[["10", "20"], ["165"]]]
    infos = [["int", "Chưa dùng hàm int() để chuyển sang số nguyên", ["2"]], [
        "print", "Chưa in ra màn hình", ["1"]]]
    print(main(filename, tests, infos))

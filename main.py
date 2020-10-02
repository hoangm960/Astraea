import test

import gui

test_x_list = [1, 20, 40]
test_y_list = [20, 80, 64]
for i in test_x_list:
    for j in test_y_list:
        result = test.main(i, j)
        ans = i + j
        try:
            assert result == ans
            print("Pass.")
        except AssertionError:
            print("Wrong Answer")

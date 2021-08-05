import sys

from PyQt5 import QtWidgets

from connect import ConnectWindow
from doc import DocWindow
from edit_main import EditWindow
from loading_screen import LoadingScreen
from login_main import LoginWindow
from Main import screen_resolution
from main_ui import MainWindow
from pad import PadWindow
from quit import QuitFrame
from result_main import ResultWindow
from room import RoomWindow
from user_profile import ProfileWindow

SCREEN_WIDTH, SCREEN_HEIGHT = screen_resolution()


class Controller:
    def __init__(self, version):
        self.version = version
        self.main = None

    def show_loading(self):
        self.loading = LoadingScreen(self.version)
        self.loading.switch_window.connect(self.show_login)
        self.loading.show()

    def show_login(self, pg=None):
        if pg:
            self.pg = pg
        self.login = LoginWindow(self.pg)
        self.login.switch_window_main.connect(self.reset_login)
        self.login.switch_window_main.connect(self.show_main)
        self.login.switch_window_quit.connect(self.show_quit)
        self.loading.close()
        self.login.show()
        self.login.raise_()

    def show_main(self, role=None):
        if role is not None:
            self.role = role

        if not self.main:
            self.main = MainWindow(self.role, self.pg)
            self.main.move(SCREEN_WIDTH - self.main.width(), 0)
            self.main.switch_window_edit.connect(self.show_edit)
            self.main.switch_window_doc.connect(self.show_doc)
            self.main.switch_window_connect.connect(self.show_connect)
            self.main.switch_window_profile.connect(self.show_profile)
            self.main.switch_window_result.connect(self.show_result)
            self.main.switch_window_quit.connect(self.show_quit)

        self.main.show()

    def show_edit(self):
        self.edit = EditWindow()
        self.edit.switch_window.connect(self.reset_main)
        self.edit.switch_window.connect(self.show_main)
        self.edit.switch_window.connect(self.edit.close)
        self.disable_windows(True)
        self.edit.show()

    def show_doc(self):
        self.doc = DocWindow(self.role)
        self.doc.switch_window_pad.connect(self.show_pad)
        self.doc.switch_window_main.connect(self.show_main)
        self.doc.switch_window_main.connect(self.doc.close)
        self.doc.switch_window_main.connect(lambda: self.disable_windows(False))
        self.main.hide()
        self.doc.show()

    def show_pad(self):
        self.pg.maximize()
        self.pad = PadWindow()
        self.pad.switch_window.connect(self.show_doc)
        self.doc.close()
        self.pad.show()

    def show_connect(self):
        self.connect = ConnectWindow(self.role)
        self.connect.switch_window_main.connect(lambda: self.disable_windows(False))
        self.connect.switch_window_main.connect(self.connect.close)
        self.connect.switch_window_room.connect(self.show_room)
        self.disable_windows(True)
        self.connect.show()

    def show_room(self, room_id):
        self.room_id = room_id
        self.room = RoomWindow(self.role, self.room_id)
        self.room.switch_window.connect(self.room.close)
        self.room.switch_window.connect(self.reset_main)
        self.room.switch_window.connect(self.show_main)
        self.connect.close()
        self.main.hide()
        self.room.show()

    def show_profile(self):
        self.profile = ProfileWindow()
        self.profile.switch_window_main.connect(
            lambda: self.main.profile_btn.setDisabled(False)
        )
        self.profile.switch_window_login.connect(self.profile.close)
        self.profile.switch_window_login.connect(self.close_main)
        self.profile.switch_window_login.connect(self.show_login)
        self.main.profile_btn.setDisabled(True)
        self.profile.show()

    def show_result(self):
        self.result = ResultWindow()
        self.result.switch_window.connect(self.result.close)
        self.result.switch_window.connect(lambda: self.disable_windows(False))
        self.disable_windows(True)
        self.result.show()

    def show_quit(self):
        self.quit = QuitFrame()
        self.quit.reset_state.connect(lambda: self.disable_windows(False))
        self.quit.close_window.connect(self.close_pg)
        self.disable_windows(state=True, all_main=True)
        self.quit.show()

    def disable_windows(self, state, all_main=False):
        if self.login:
            self.login.setDisabled(state)
        if self.main:
            self.main.setDisabled(
                state
            ) if all_main else self.main.frame_func_btn.setDisabled(state)

    def reset_main(self):
        self.main.close()
        self.main = None

    def close_main(self):
        self.reset_main()
        self.pg.minimize()

    def reset_login(self):
        self.login.close()
        self.login = None

    def close_pg(self):
        if self.pg:
            self.pg.close()
        sys.exit()


def main(version):
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller(version)
    controller.show_loading()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main("3.1.3")

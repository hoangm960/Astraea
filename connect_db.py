import mysql.connector


class DBConnection:
    def __init__(self):

        self = mysql.connector.connect(
            host="sql6.freesqldatabase.com",
            user="sql6442582",
            password="DMd7vFtXQs",
            database="sql6442582",
        )

    def close_connection(self):
        self.commit()
        self.close()
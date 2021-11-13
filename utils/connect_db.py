import mysql.connector


def get_connection():
    return mysql.connector.connect(
            host="sql6.freesqldatabase.com",
            user="sql6442582",
            password="DMd7vFtXQs",
            database="sql6442582",
        )

if __name__ == "__main__":
    print(get_connection())
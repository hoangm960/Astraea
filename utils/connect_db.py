import mysql.connector


def get_connection():
    return mysql.connector.connect(
            host="khktdb.ddns.net",
            user="minh",
            password="nhatminhb5/2901",
            database="astraea_sql",
        )

if __name__ == "__main__":
    print(get_connection())
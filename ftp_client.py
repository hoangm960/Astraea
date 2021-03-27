import os
from ftplib import FTP


def directory_exists(dir):
    filelist = []
    ftp.retrlines("LIST", filelist.append)
    return any(f.split()[-1] == dir for f in filelist)


def chdir(dir):
    if directory_exists(dir) is False:
        ftp.mkd(dir)
    ftp.cwd(dir)


def get_file(dir, des):
    if directory_exists(dir):
        with open(des, "wb") as f:
            ftp.retrbinary("RETR " + dir, f.write, 1024)
    else:
        print("Dir not found!")


def upload_file(dir, des):
    if os.path.exists(dir):
        des_dir, filename = tuple(os.path.split(des))
        if des_dir:
            chdir(des_dir)
        with open(dir, "rb") as f:
            ftp.storbinary("STOR " + filename, f)


host = "123.19.151.58"
user = "Administrator"
password = "nhatminhb5/2901"

with FTP(host) as ftp:
    ftp.login(user=user, passwd=password)
    print(ftp.getwelcome())
    upload_file("Test/test.docx", "bruh/test.docx")
    ftp.quit()

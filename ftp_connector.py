import ftplib


def ftp_login():
    ftp = ftplib.FTP("10.0.124.73")
    ftp.login("anonymous", "")
    ftp.cwd('/Users/Public/Documents/FTP')

    return ftp


def get_contents(ftp):
    data = []
    ftp.dir(data.append)
    for pos, line in enumerate(data):
        print(line)
        data[pos] = line.split(" ")[-1]
    return data


def ftp_upload(filename):
    ftp = ftp_login()

    with open(filename, 'rb') as file:
        ftp.storbinary(f"STOR {filename.split('/')[-1]}", file)

    # get_contents(ftp)
    ftp.close()


def ftp_retrieve_contents():
    ftp = ftp_login()
    data = get_contents(ftp)
    ftp.close()
    return data


# ftp_upload("files/test2.txt")
# d = ftp_retrieve_contents()

# print("______________")
# print(d)

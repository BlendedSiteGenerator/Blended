import os
import sys

from ftplib import FTP, error_perm

def placeFiles(ftp, path):
    """Upload the built files to FTP"""
    for name in os.listdir(path):
        if name != "config.py" and name != "config.pyc" and name != "templates" and name != "content":
            localpath = os.path.join(path, name)
            if os.path.isfile(localpath):
                print("STOR", name, localpath)
                ftp.storbinary('STOR ' + name, open(localpath, 'rb'))
            elif os.path.isdir(localpath):
                print("MKD", name)

                try:
                    ftp.mkd(name)

                # ignore "directory already exists"
                except error_perm as e:
                    if not e.args[0].startswith('550'):
                        raise

                print("CWD", name)
                ftp.cwd(name)
                placeFiles(ftp, localpath)
                print("CWD", "..")
                ftp.cwd("..")

def sendFTP():
    config_file_dir = os.path.join(cwd, "data", "ftp.json")
    if not os.path.exists(config_file_dir):
        sys.exit("You do not have an ftp settings file!")
    else:
        with open(config_file_dir) as config_file:
            ftp_config = json.load(config_file)

    server = ftp_config['server']
    username = ftp_config['username']
    password = ftp_config['password']
    port = ftp_config['port']

    ftp = FTP()
    ftp.connect(server, port)
    ftp.login(username, password)
    filenameCV = os.path.join(cwd, outdir)

    try:
        ftp.cwd(ftp_upload_path)
        placeFiles(ftp, filenameCV)
    except:
        ftp.quit()
        sys.exit("Files not able to be uploaded! Are you sure the directory exists?")

    ftp.quit()

    print("\nFTP Done!")

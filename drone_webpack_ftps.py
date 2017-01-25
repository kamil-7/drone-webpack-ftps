import os

from ftplib import FTP_TLS
from subprocess import call

from ftp_utils import upload_files

github_username = os.environ['PLUGIN_GITHUB_USERNAME']
ftp_server = os.environ['PLUGIN_FTP_SERVER']
ftp_username = os.environ['PLUGIN_FTP_USERNAME']
ftp_password = os.environ['PLUGIN_FTP_PASSWORD']
tag = os.environ['PLUGIN_TAG']
project = os.environ['PLUGIN_PROJECT']

working_directory = '/drone/src/github.com/{}/{}'.format(github_username, project)

call(["npm", "install"], cwd=working_directory)
call(["webpack", "-p"], cwd=working_directory)

ftp = FTP_TLS(ftp_server)
ftp.login(user=ftp_username, passwd=ftp_password)

ftp.cwd(project)
ftp.mkd(tag)
ftp.cwd(tag)

directories = os.environ['PLUGIN_DIRECTORIES'].split(",")
for directory in directories:
    upload_files(ftp, '{}/{}'.format(working_directory, directory))

ftp.quit()

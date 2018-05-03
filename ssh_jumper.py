"""
SSH跳板机
使用远程主机爬取网页

示例:
if __name__ == "__main__":
    conn = SSHConnection('100.100.100.100', 22, 'user', 'password')
    print(conn.exec_command('ls -ll'))
    print(conn.exec_command('curl google.com'))
"""

import paramiko


"""SSH隧道"""
class SSHConnection(object):
    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self._transport = None
        self._sftp = None
        self._client = None
        self._connect()  # 建立连接

    def _connect(self):
        transport = paramiko.Transport((self._host, self._port))
        transport.connect(username=self._username, password=self._password)
        self._transport = transport

        # 下载

    def download(self, remotepath, localpath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.get(remotepath, localpath)

        # 上传

    def put(self, localpath, remotepath):
        if self._sftp is None:
            self._sftp = paramiko.SFTPClient.from_transport(self._transport)
        self._sftp.put(localpath, remotepath)

        # 执行命令

    def exec_command(self, command):
        if self._client is None:
            self._client = paramiko.SSHClient()
            self._client._transport = self._transport
        stdin, stdout, stderr = self._client.exec_command(command)
        data = stdout.read()
        if len(data) > 0:
            #print(data.strip())  # 打印正确结果
            return data
        err = stderr.read()
        if len(err) > 0:
            #print(err.strip())  # 输出错误结果
            return err

    def close(self):
        if self._transport:
            self._transport.close()
        if self._client:
            self._client.close()

###################
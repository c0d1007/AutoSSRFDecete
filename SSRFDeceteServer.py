#   coding:utf-8

import socket
from Crypto.Cipher import AES


class findTheFileName():

    def __init__(self,port,passKey,logFilePath,password):
        self.port = port
        self.passKey = passKey
        self.logFilePath = logFilePath
        self.password = password

    def receiveData(self):
        # create an INET, STREAMing socket
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # bind the socket to a public host, and a well-known port
        serverSocket.bind(('0.0.0.0', self.port))
        # become a server socket
        serverSocket.listen(10)
        print('Beginning to listenl : ' + str(('0.0.0.0', self.port)))

        while True:
            conn, addr = serverSocket.accept()
            method_Content_Encrypt = conn.recv(4096)
            method_Content_Decrypt = self.decrypt(content=method_Content_Encrypt)
            method_Content = method_Content_Decrypt.split(':')
            if method_Content[0] == 'GET':
                if self.password == method_Content[1]:
                    print('Welcome')
                    successReceive = self.findFileNameForLog(method_Content[2:])
                    conn.send(bytes(str(successReceive),encoding='utf-8'))
                else:
                    conn.send(bytes('Password is error ...',encoding='utf-8'))

    def decrypt(self,content):
        #秘钥,此处需要将字符串转为字节
        passKey = bytes(self.passKey,encoding='utf-8')
        #加密秘钥需要长达16位字符，所以进行空格拼接
        def pad_key(passKey):
            while len(passKey) % 16 != 0:
                passKey += b' '
            return passKey
        aesDecrypt = AES.new(pad_key(passKey), AES.MODE_ECB)
        #用aes对象进行解密，将字节类型转为str类型，错误编码忽略不计
        decryptContent = str(aesDecrypt.decrypt(content),encoding='utf-8',errors="ignore")
        return decryptContent.strip()

    def findFileNameForLog(self,fileNameList):
        successReceive = []
        with open(self.logFilePath,'r') as fs:
            for line in fs:
                for fileName in fileNameList:
                    if fileName in line:
                        successReceive.append(fileName)
                        successReceive = list(set(successReceive))  # 去重

        # 当没有找到关键词时才赋值
        if successReceive == []:
            successReceive = 'Not Found'
        print('This SSRF Decete result is : ' + str(successReceive))
        return successReceive


if __name__ == '__main__':
    port = 12345
    logFilePath = 'test.txt'
    passKey = 'sdjfkahd(*&HHDHweuuew'
    password = 'sdkDD.,JKJwieru_)('
    test = findTheFileName(port=port,passKey=passKey,logFilePath=logFilePath,password=password)
    test.receiveData()

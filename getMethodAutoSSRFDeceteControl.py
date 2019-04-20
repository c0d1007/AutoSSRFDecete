#   coding:utf-8

import random
import requests
from Crypto.Cipher import AES
import socket
import time


class getMethodSSRFDetect():

    def __init__(self,testURL,serverURL,method,passKey,serverIPAddr,serverPort,password):
        self.testURL = testURL
        self.serverURL = serverURL
        self.method = method
        self.passKey = passKey
        self.serverIPAddr = serverIPAddr
        self.serverPort = serverPort
        self.password = password    # 认证密码


    # 生成随机16位长的文件名
    def randomFileName(self):
        # 针对每个参数生成不一样的paylaod作为标记
        pars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                'y', 'z', '1', '2', '3', '4', '5', '6',
                '7', '8', '9', '0']

        fileName = ''
        for i in range(0,32):
            fileName += pars[random.randrange(0,25,1)]
        return fileName + '.jpg'

    def payloadURLGenerate(self):
        parameters = self.testURL.split('&')  # 将所有参数分开
        resutURL = ''   # 将payload插入到所有的参数中的URL，应将所有的参数值去掉，以免影响测试结果
        count = 0   # 计算参数的个数
        parameter_fileName = {}     # 保存所有参数与文件名对应的关系
        fileNameList = ''
        for par in parameters:
            count += 1
            parName = par.split('=')
            fileName = self.randomFileName()    # 生成的文件名
            fileNameList += fileName + ':'   # 文件列表
            parameter_fileName[parName[0]] = fileName
            resultPar = parName[0] + '=' + self.serverURL + '/' + fileName
            # 将所有参数重新使用&符号进行连接
            if count >= len(parameters):
                resutURL += resultPar
            else:
                resutURL += resultPar + '&'
        return resutURL,parameter_fileName,fileNameList


    def encrypt(self,fileName):
        # 秘钥,此处需要将字符串转为字节
        passKey = bytes(self.passKey, encoding='utf-8')

        # 加密秘钥需要长达16位字符，所以进行空格拼接
        def pad_key(passKey):
            while len(passKey) % 16 != 0:
                passKey += b' '
            return passKey

        # 进行加密算法，模式ECB模式，把叠加完16位的秘钥传进来
        aes = AES.new(pad_key(passKey), AES.MODE_ECB)

        # 加密提交方式和文件名，以分号隔开,需要将字符串转为字节
        content = bytes(self.method + ":" + fileName, encoding='utf-8')

        # 加密内容需要长达16位字符，所以进行空格拼接
        def pad_content(content):
            while len(content) % 16 != 0:
                content += b' '
            return content

        # 进行内容拼接16位字符后传入加密类中，结果为字节类型
        encrypted_text = aes.encrypt(pad_content(content))
        return encrypted_text

    def sendFileNameToServer(self,fileName):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((self.serverIPAddr, self.serverPort))
        encrypted_text = self.encrypt(self.password + ':' + fileName)
        client.send(encrypted_text)
        data = client.recv(4096)
        fileResult = str(data, encoding='utf-8')
        client.close()
        return fileResult

if __name__ == '__main__':
    print('SSRF Decete Beginning ...')
    testURL = 'http://www.xxxx.com/?test=1&tets2=2&test3=4&url=5'
    serverURL =  'http://www.testserver.com'
    serverIPAddr = '127.0.0.1'
    serverPort = 12345
    method = 'GET'
    passKey = 'sdjfkahd(*&HHDHweuuew'
    password = 'sdkDD.,JKJwieru_)('

    getMethodSSRFClass = getMethodSSRFDetect(testURL=testURL,serverURL=serverURL,method=method,
                                             passKey=passKey,serverIPAddr=serverIPAddr,serverPort=serverPort,
                                             password=password)
    resultURL,parameters_fileName,fileNameList = getMethodSSRFClass.payloadURLGenerate()
    getRequest = requests.get(url=resultURL)
    time.sleep(5)   # 以防网络时延导致不能正确判断
    fileResult = getMethodSSRFClass.sendFileNameToServer(fileNameList)
    print('[+] This result is : ' + fileResult)
    fileNameList = fileResult.split("'")
    fileResultList = []
    for fileName in fileNameList:
        if fileName.strip() in ['[',']',',']:
            continue
        else:
            fileResultList.append(fileName.strip())
    print('Server connection done !!!')
    bugParName = []
    for fileName in fileResultList:
        for parName in parameters_fileName:
            if parameters_fileName[parName] == fileName:
                bugParName.append(parName)
    print('[+] Existe bug parameters is : ' + str(bugParName))

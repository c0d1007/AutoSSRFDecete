# AutoSSRFDecete
SSRF自动化测试

# 依赖
python3 pycryptodemo

# 说明

## getMethodAutoSSRFDeceteControl

1、用于测试GET请求中的所有参数可能存在的SSRF情况，测试的方式只是简单的将参数赋值为URL进行的简单测试；

2、在使用过程中，需修改自己所要测试的参数：
testURL：被测试服务器；
serverURL：自建的web服务器访问地址；
serverIPAddr：自建服务器IP地址；
passKey：传输加密秘钥；
password：用于客户端和服务器端之间的简单认证。

## SSRFDeceteServer

1、自建服务器上运行，用户接收被测试服务器的请求；

2、在使用过程中，需修改自己所要测试的参数：
logFilePath：服务器的日志文件路径；
passKey、password：与客户端配置一样；


# 运行程序

1、在服务器上运行脚本(后台运行)

nohup python3 SSRFDeceteServer.py &

2、在测试主机运行：

python3 getMethodAutoSSRFDeceteControl.py

# 废话

未完善其他功能，未使用参数化输入，所以需要修改文件后运行，后续再说.......



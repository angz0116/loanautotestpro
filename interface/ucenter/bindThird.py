# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
interfaceNo = "bindThird"
name = "绑定第三方平台"

req = ConfigHttp()


@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 绑定第三方平台(unittest.TestCase):
    def setParameters(self, No, 测试结果, 请求报文, 返回报文, 测试用例, url, type, unionid, openid, 预期结果):
        self.No = str(No)
        self.url = str(url)
        self.type = str(type)
        self.unionid = str(unionid)
        self.openid = str(openid)

    def setUp(self):
        self.log = MyLog.get_log()
        self.logger = self.log.logger
        self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
        print(interfaceNo + name + "CASE " + self.No)

    """绑定第三方平台"""
    def test_body(self):
        req.httpname = "KPTEST"
        # 获取执行接口的url
        self.url = get_excel("url", self.No, interfaceNo)
        # 获取登录sheet页中token
        self.token = get_excel("token", self.No, "login")

        # 平台类型 1=微信 2=微博 3=QQ
        self.type = get_excel("type", self.No, interfaceNo)
        # 应用唯一标识
        self.unionid = get_excel("unionid", self.No, interfaceNo)
        # 其他页面
        self.openid = get_excel("openid", self.No, interfaceNo)
        self.data = {
            "type": self.type,
            "unionid": self.unionid,
            "openid": self.openid,
            "v": "3.11.0",
            "system": "5",
            "device_model": "HUAWEI P10",
            "system_version": "V1.0.0",
            "channel": "5"
        }
        print(self.data)
        if self.token=="":
            self.urlq = self.url
            self.logger.info(interfaceNo+">>>>token为空====="+self.urlq)
        else:
            self.urlq = self.url+"&&token="+self.token
            self.logger.info(interfaceNo + ">>>>token====="+self.urlq)
        req.set_url(self.urlq)
        req.set_data(self.data)
        self.response = req.post()
        print(self.response)
        try:
            self.retcode = self.response["code"]
        except Exception:
            self.logger.error("报文返回为空！")
            print("报文返回为空！")
        self.check_result()
        self.wr_excel()

    # 检查数据结果
    def check_result(self):
        try:
            self.assertEqual(self.retcode, 0, self.logger.info("是否绑定第三方平台"))
            set_excel("pass", "测试结果", self.No, interfaceNo)
            self.logger.info("测试通过")
        except AssertionError:
            set_excel("fail", "测试结果", self.No, interfaceNo)
            self.msg = self.response["msg"]
            self.logger.error("测试失败")
        self.msg = self.response["msg"]
        self.logger.info(self.msg)

    # 写入xls文件中
    def wr_excel(self):
        set_excel(r'"'+str(self.data)+'"', "请求报文", self.No, interfaceNo)
        set_excel(r'"'+str(self.response)+'"', "返回报文", self.No, interfaceNo)
        set_excel(self.msg, "预期结果", self.No, interfaceNo)

    def tearDown(self):
        self.log.build_case_line("请求报文", self.data)
        self.log.build_case_line("返回报文", self.response)
        self.log.build_case_line("预期结果", self.msg)
        self.log.build_end_line(interfaceNo + "--CASE" + self.No)


if __name__ == '__main__':
    unittest.main()


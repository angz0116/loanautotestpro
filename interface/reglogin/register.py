# -*- coding:utf-8 -*-

from utils.baseLog import MyLog
from utils.baseHttp import ConfigHttp
from utils.baseUtils import *
import unittest
import paramunittest
from utils.baseDB import ConfigDB
import datetime
from service.gainPhone import createPhone
from service.gainName import getFullName
from datadao.verifyCode import getVerifyCode
interfaceNo = "register"
name = "用户注册register"

req = ConfigHttp()
sqldb = ConfigDB()

@paramunittest.parametrized(*get_xls("interfaces.xls", interfaceNo))
class 注册(unittest.TestCase):
	def setParameters(self, No, 测试结果, 测试用例, 请求报文, 返回报文,url, mobile, regtype, countrycode, verifycode, 预期结果):
		self.No = str(No)
		self.url = str(url)
		self.mobile = str(mobile)
		self.regtype = str(regtype)
		self.countryCode = str(countrycode)
		self.verifycode = str(verifycode)


	def setUp(self):
		self.log = MyLog.get_log()
		self.logger = self.log.logger
		self.log.build_start_line(interfaceNo + name + "CASE " + self.No)
		print(interfaceNo + name + "CASE " + self.No)
	def test_body(self):
		req.httpname = "KPTEST"
		self.url = get_excel("url", self.No, interfaceNo)
		self.mobile = get_excel("mobile", self.No, interfaceNo)
		if(self.mobile==""):
			# 获取手机号
			self.telphone = createPhone()
		else:
			self.telphone = self.mobile
		# 获取姓名
		self.nick = getFullName()
		# 注册类型 1=普通密码注册 2=短信验证码
		self.regtype = get_excel("reg_type", self.No, interfaceNo)
		# 国家编码，86中国，其他国外
		self.countryCode = get_excel("countrycode", self.No, interfaceNo)
		# 获取验证码的方法
		self.virifyCode = getVerifyCode(self.No,interfaceNo,self.telphone)
		# 根据注册类型判断是输入验证码或密码
		print("用户注册接口手机号==" + self.telphone)
		self.data = {
			"mobile": self.telphone,
			"nick": self.nick,
			"reg_type": self.regtype,
			"verify": self.virifyCode,
			"pass": "abc123456",
			"source": "1",
			"country_code": self.countryCode,
			"yk_token": "5",
			"app_version": "8.0.0",
			"system": "3",
			"device_model": "HUAWEI P10",
			"system_version": "V1.0.0",
			"channel": "5"
		}
		req.set_url(self.url)
		req.set_data(self.data)
		self.response = req.post()
		try:
			self.retcode = self.response["code"]
		except Exception:
			self.logger.error("报文返回为空！")
			print("报文返回为空！")
		self.check_result()
		self.wr_excel()
	
	def check_result(self):
		try:
			self.assertEqual(self.retcode, 0, self.logger.info("检查是否注册成功"))
			#注册成功后，则把手机号写入“检查是否注册”的接口中
			if self.retcode==0:
				set_excel(self.telphone, "mobile", self.No, "getMobileStatus")
			set_excel("pass", "测试结果", self.No, interfaceNo)
			self.logger.info("测试通过")
		except AssertionError:
			set_excel("fail", "测试结果", self.No, interfaceNo)
			self.logger.error("测试失败")
		self.msg = self.response["msg"]
		self.logger.info(self.msg)
	# 写入xls文件中
	def wr_excel(self):
		set_excel(self.data, "请求报文", self.No, interfaceNo)
		set_excel(self.response, "返回报文", self.No, interfaceNo)
		set_excel(self.telphone, "mobile", self.No, interfaceNo)
		set_excel(self.msg, "预期结果", self.No, interfaceNo)
	
	def tearDown(self):
		self.log.build_case_line("请求报文", self.data)
		self.log.build_case_line("返回报文", self.response)
		self.log.build_case_line("预期结果", self.msg)
		self.log.build_end_line(interfaceNo + "--CASE" + self.No)

if __name__ =='__main__':
	unittest.main()

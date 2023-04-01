import requests
import random

from PyQt5.QtCore import QThread, pyqtSignal

from GUI.utils.language import *

# generate random ip address
def random_ip():
	a = random.randint(1, 255)
	b = random.randint(1, 255)
	c = random.randint(1, 255)
	d = random.randint(1, 255)
	return str(a) + '.' + str(b) + '.' + str(c) + '.' + str(d)

# generate header for request
def add_header():
	return {
        "Referer" : "https://app-api.pixiv.net/",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Proxy-Connection": "keep-alive",
		'User-Agent': 'Mozilla/5.0 (Windows NT 7.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
		'X-Forwarded-For': random_ip()
    }


class GoogleTranslation_API(QThread):
	get_translated_signal = pyqtSignal()		# signal to send the translated of question 

	def __init__(self, url, text):
		super().__init__()
		# infos
		self.url = url
		self.text = text

	def __del__(self):
		self.wait()

	def judge_language(self, text):
		dest = "zh-cn"
		for c in text:
			if is_chinese(c):
				dest = "en"
		return dest

	def run(self):
		# get data for post
		data = {
			"text" : self.text,
			"dest" : self.judge_language(self.text),
		}
		print(data, self.url)

		# post
		response = requests.post(url=self.url + "/translate", headers=add_header(), data=data)

		# translated
		self.translated = response.content
		if type(self.translated) == bytes:
			self.translated = self.translated.decode()

		# signal for return
		self.get_translated_signal.emit()


if __name__ == "__main__":
	url = "http://23.254.230.133:12346/translate"

	# data = {
	# 	"text" : "电脑",
	# 	"dest" : "en",
	# }
	# response = requests.post(url=url, headers=add_header(), data=data)
	# print(response.content.decode())

	# data = {
	# 	"text" : "电脑",
	# 	"dest" : "ja",
	# }
	# response = requests.post(url=url, headers=add_header(), data=data)
	# print(response.content.decode())

	# data = {
	# 	"text" : "电脑",
	# 	"dest" : "zh-cn",
	# }
	# response = requests.post(url=url, headers=add_header(), data=data)
	# print(response.content.decode())

	def is_chinese(uchar):
		if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
			return True
		else:
			return False
	
	def judge_language(text):
		dest = "zh-cn"
		for c in text:
			if is_chinese(c):
				dest = "en"
		return dest
	
	def auto_trans(text):
		data = {
			"text" : text,
			"dest" : judge_language(text),
		}
		response = requests.post(url=url, headers=add_header(), data=data)
		print(text, response.content.decode())

	auto_trans("电脑")
	auto_trans("computer")
	auto_trans("compute game")
	auto_trans("电脑 game")
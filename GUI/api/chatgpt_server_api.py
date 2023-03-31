import requests
import random
import json
import time
from threading import Thread

from PyQt5.QtCore import QThread, pyqtSignal
from threading import Thread
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


class ChatGPT_API(QThread):
	signal = pyqtSignal()

	def __init__(self, info_path="data/info.json", *args, **kwargs):
		super().__init__()

		self.info = json.load(open(info_path))
		self.url = self.info["url"]
		self.uid = self.info["uid"]

		self.main_win = kwargs.get('main_win')

	def __del__(self):
		self.wait()

	def run(self):
		# data = {
		# 	"uid" : self.uid,
		# 	"new_chat" : self.new_chat,
		# 	"question" : self.question
		# }
		data = {
			"uid" : f"000{self.question[0]}",
			"new_chat" : self.new_chat,
			"question" : self.question[1:]
		}
		print(data, self.url)
		response = requests.post(url=self.url + "/chat", headers=add_header(), data=data)
		self.answer = response.content
		if type(self.answer) == bytes:
			self.answer = self.answer.decode()
		print(self.answer)
		self.signal.emit()

if __name__ == "__main__":
	url = "http://23.254.230.133:12346/chat"
	data = {
		"uid" : "0000",
		"new_chat" : "0",
		"question" : "Hi"
	}
	response = requests.post(url=url, headers=add_header(), data=data)
	print(response.content)
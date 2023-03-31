import requests
import random

from PyQt5.QtCore import QThread, pyqtSignal

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
	get_answer_signal = pyqtSignal()		# signal to send the answer of question 

	def __init__(self, url, uid, hash_password, new_chat, question):
		super().__init__()
		# infos
		self.url = url
		self.uid = uid
		self.hash_password = hash_password
		self.new_chat = new_chat
		self.question = question

	def __del__(self):
		self.wait()

	def run(self):
		# get data for post
		data = {
			"uid" : self.uid,
			"hash_password" : self.hash_password,
			"new_chat" : self.new_chat,
			"question" : self.question
		}
		print(data, self.url)

		# post
		response = requests.post(url=self.url + "/chat", headers=add_header(), data=data)

		# answer
		self.answer = response.content
		if type(self.answer) == bytes:
			self.answer = self.answer.decode()

		# signal for return
		self.get_answer_signal.emit()


if __name__ == "__main__":
	url = "http://23.254.230.133:12346/chat"
	data = {
		"uid" : "0000",
		"new_chat" : "0",
		"question" : "Hi"
	}
	response = requests.post(url=url, headers=add_header(), data=data)
	print(response.content)
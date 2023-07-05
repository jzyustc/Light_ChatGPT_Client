from PyQt5.QtCore import QThread, pyqtSignal

import socket

# get ip address
def get_ip():
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    return ip


class FileTransferServer_API(QThread):
	get_answer_signal = pyqtSignal()		# signal to send the answer of question 

	def __init__(self, port):
		super().__init__()
		# infos
		self.ip = get_ip()
		self.port = port

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
	print(get_ip())
	# url = "http://23.254.230.133:12346/chat"
	# data = {
	# 	"uid" : "0000",
	# 	"new_chat" : "0",
	# 	"question" : "Hi"
	# }
	# response = requests.post(url=url, headers=add_header(), data=data)
	# print(response.content)
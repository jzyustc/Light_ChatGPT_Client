import time

from PyQt5.QtCore import QThread, pyqtSignal


class Timer(QThread):
	timer_signal = pyqtSignal(int)		# send signal of the timer

	def __init__(self, time_interval):
		super().__init__()
		# infos
		self.time_interval = time_interval
		self.num = 0

	def __del__(self):
		self.wait()

	def run(self):
		while True:
			print(self.num)
			self.timer_signal.emit(self.num)
			self.num += 1
			time.sleep(self.time_interval)

			if self.num >= 20:
				return


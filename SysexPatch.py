import mido
import time

class SysexPatch(object):
	TIMEOUT_DURATION = 3.0
	SLEEP_DURATION = 0.25

	VERIFY_INVALID = 0
	VERIFY_VALID = 1
	VERIFY_COMPLETE = 2

	DEFAULT_PORT_NAME = None

	_data = []
	_in_port = None
	_out_port = None

	def __init__(self, port):
		if port is None:
			self._receive(self.DEFAULT_PORT_NAME)
		else:
			self._receive(port)

	def _open_input(self, port):
		if self._in_port is None:
			self._in_port = mido.open_input(port)
		else:
			assert self._in_port.name == port
		return self._in_port

	def _open_output(self, port):
		if self._out_port is None:
			self._out_port = mido.open_output(port)
		else:
			assert self._out_port.name == port

		return self._out_port

	def get_name(self):
		if len(self._data) > 0:
			return "(no name)"
		else:
			return None

	@classmethod
	def _verify(cls, msg_list):
		"""Determine if data in msg_list is either 1. valid so far or 2. a complete, valid patch"""
		raise NotImplementedError()

	def _send_request(self, port):
		print "No request command available, please initiate sysex on instrument"

	def _receive(self, port):
		assert len(self._data) == 0

		in_port = self._open_input(port)
		self._send_request(port)

		timeout = time.time() + self.TIMEOUT_DURATION
		while time.time() < timeout:
			for message in in_port.iter_pending():
				if message.type == 'sysex':
					print('Received {}'.format(message))
					if self._verify([message]) >= self.VERIFY_VALID:
						self._data.append(message)
						timeout = time.time() + self.TIMEOUT_DURATION + self.SLEEP_DURATION

		if self._verify(self._data) == self.VERIFY_COMPLETE:
			print "Received patch %s, done" % self._get_name()
		else:
			print "Incomplete patch data received"

	def write_syx(self, filename):
		assert (self._verify(self._data) == self.VERIFY_COMPLETE)
		mido.write_syx_file(filename, self._data, plaintext=False)

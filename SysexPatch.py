import mido
import time

class SysexPatch(object):
	TIMEOUT_DURATION = 3.0
	SLEEP_DURATION = 0.25

	VERIFY_INVALID = 0
	VERIFY_VALID = 1
	VERIFY_COMPLETE = 2

	_data = []
	_in_port = None
	_out_port = None

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

	def _get_name(self):
		return "(no name)"

	@classmethod
	def _verify(cls, data):
		raise NotImplementedError()

	def _send_request(self, port):
		print "No request command available, please initiate sysex on instrument"

	def _receive(self, port):
		assert len(self._data) == 0

		in_port = self._open_input(port)
		self._send_request(port)

		timeout = time.time() + self.TIMEOUT_DURATION
		msg_iterator = in_port.__iter__()
		while time.time() < timeout:
			try:
				#FIXME: midi port has some kind of built in sleep
				message = msg_iterator.next()
				if message.type == 'sysex':
					print('Received {}'.format(message))
					if self._verify([message.data]) >= self.VERIFY_VALID:
						self._data.append(message.data)
						timeout = time.time() + self.TIMEOUT_DURATION + self.SLEEP_DURATION

			except StopIteration:
				time.sleep(SLEEP_DURATION)
				msg_iterator = in_port.__iter__()
		if self._verify(self._data) == self.VERIFY_COMPLETE:
			print "Received patch %s, done" % self._get_name()
		else:
			print "Incomplete patch data received"

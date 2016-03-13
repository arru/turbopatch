import importlib
import re
import sys
import time
import mido


def load_device_class(device_name, port_name=None):
	module_name = re.match("^[a-zA-Z0-9_]+$", device_name).group(0)
	class_name = "%sPatch" % (module_name)

	module = importlib.import_module(module_name)

	return getattr(module, class_name)




class SysexPatch(object):
	TIMEOUT_DURATION = 8.0
	SLEEP_DURATION = 0.25

	VERIFY_INVALID = 0
	VERIFY_VALID = 1
	VERIFY_COMPLETE = 2

	DEFAULT_PORT_NAME = None

	CHAR_SUBSTITUTES = {0: "", 47: "-"}

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
			try:
				self._in_port = mido.open_input(port)
			except IOError:
				print "Couldn't open input port '%s'. The following MIDI ports are available:" % port
				for p in mido.get_input_names():
					print "'%s'" % p
				raise
		else:
			assert self._in_port.name == port
		return self._in_port

	def _open_output(self, port):
		if self._out_port is None:
			try:
				self._out_port = mido.open_output(port)
			except IOError:
				print "Couldn't open output port '%s'. The following MIDI ports are available:" % port
				for p in mido.get_output_names():
					print "'%s'" % p
				raise
		else:
			assert self._out_port.name == port

		return self._out_port

	def get_name(self):
		"""Return patch name as string, or None if objects lacks a complete patch (program) dump."""
		if self._verify(self._data) != self.VERIFY_COMPLETE:
			return None

		name_data = self._name_bytes()

		if name_data is not None:
			name = ""
			for c in name_data:
				if c in self.CHAR_SUBSTITUTES:
					name = name + self.CHAR_SUBSTITUTES[c]
				else:
					name = name + chr(c)

			name = name.strip()

			return name
		else:
			return "(no name)"

	def _name_bytes(self):
		"""Will only be called when patch data verifies to VERIFY_COMPLETE. Returns mere unconverted bytes that make up patch name. Either override this, or get_name() if
		name extraction is more complicated than slicing a part of the byte stream"""
		return None

	@classmethod
	def _verify(cls, msg_list):
		"""Determine if data in msg_list is either 1. valid so far or 2. a complete, valid patch"""
		raise NotImplementedError()

	def _request_data(self):
		return None

	def _send_request(self, port):
		req_data = self._request_data()

		if req_data is None:
			print "No request command available, please initiate sysex on instrument"
		else:
			request = mido.Message('sysex', data=req_data)
			out_port = self._open_output(port)
			out_port.send(request)

	def _receive(self, port):
		assert len(self._data) == 0

		in_port = self._open_input(port)
		self._send_request(port)

		timeout = time.time() + self.TIMEOUT_DURATION
		while time.time() < timeout:
			for message in in_port.iter_pending():
				if message.type == 'sysex':
					if self._verify([message]) >= self.VERIFY_VALID:
						self._data.append(message)
						timeout = time.time() + self.TIMEOUT_DURATION + self.SLEEP_DURATION

		if not self._verify(self._data) == self.VERIFY_COMPLETE:
			print "Incomplete patch data received"

	def write_syx(self, filename):
		assert (self._verify(self._data) == self.VERIFY_COMPLETE)
		mido.write_syx_file(filename, self._data, plaintext=False)

	def dump(self):
		"""Send comma-separated SysEx data to stdout"""
		for message in self._data:
			for byte in message.data:
				sys.stdout.write("%d, " % byte)
			sys.stdout.write("\n")

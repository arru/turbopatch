import SysexPatch
import mido


class StreichfettPatch(SysexPatch.SysexPatch):
	DEVICE_ID = 0x3E
	BANK_PRESET = 0x00  # Flash stored preset
	BANK_ALL = 0x7e  # All presets
	BANK_PANEL = 0x7f  # Play / edit buffer
	NULL_DEVICE = 0x7f

	DEFAULT_PORT_NAME = "Streichfett"

	BANK_LETTERS = ['A', 'B', 'C']


	def _send_request(self, port):
		request = mido.Message('sysex', data=[self.DEVICE_ID, 0x19, self.NULL_DEVICE, 0x00, self.BANK_PANEL])
		out_port = self._open_output(port)
		out_port.send(request)

	def _get_name(self):
		patch_code = list(self._data[0].data)[4]

		if patch_code == 127:
			return "(panel)"
		else:
			bank_num = patch_code // 4
			patch_num = (patch_code % 4) + 1
			bank = self.BANK_LETTERS[bank_num]
			return "%s%d" % (bank, patch_num)

	@classmethod
	def _verify(cls, msg_list):
		if len(msg_list) == 1 and list(msg_list[0].data)[0] == cls.DEVICE_ID and len(msg_list[0].data) == 30:
			return cls.VERIFY_COMPLETE

		return cls.VERIFY_INVALID

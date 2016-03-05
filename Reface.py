import SysexPatch
import mido



class RefacePatch(SysexPatch.SysexPatch):
	DEVICE_ID = 0x43
	GROUP_ID = [0x7f, 0x1c]
	REFACE_CP_ID = 0x04
	REFACE_CS_ID = 0x03
	REFACE_DX_ID = 0x05
	REFACE_YC_ID = 0x06

	DEFAULT_PORT_NAME = "reface DX"
	REFACE_DX_BANK_PANEL = [0x0E, 0x0F, 0x00]

	REFACE_DX_BULK_HEADER = (67, 0, 127, 28, 0, 4, 5, 0x0E, 0x0F, 0, 94)
	REFACE_DX_BULK_FOOTER = (67, 0, 127, 28, 0, 4, 5, 0x0F, 0x0F, 0, 93)

	def _send_request(self, port):
		device_number = 0x20

		req = [self.DEVICE_ID, device_number] + self.GROUP_ID + \
			  [self.REFACE_DX_ID] + self.REFACE_DX_BANK_PANEL

		request = mido.Message('sysex', data=req)
		out_port = self._open_output(port)
		out_port.send(request)

	def get_name(self):
		name = ""

		for c in self._data[1].data[10:20]:
			name = name + chr(c)

		name = name.strip()
		return name

	@classmethod
	def _verify(cls, msg_list):
		if len(msg_list) == 0:
			return cls.VERIFY_INVALID
		else:
			for item in msg_list:
				# TODO checksum
				data = item.data
				if not (data[0] == cls.DEVICE_ID and list(data[2:4]) == cls.GROUP_ID and data[6] == cls.REFACE_DX_ID):
					return cls.VERIFY_INVALID

			if len(msg_list) >= 3 and msg_list[0].data == cls.REFACE_DX_BULK_HEADER and msg_list[
				-1].data == cls.REFACE_DX_BULK_FOOTER:
				return cls.VERIFY_COMPLETE

			return cls.VERIFY_VALID

import SysexPatch
import mido



class RefacePatch(SysexPatch.SysexPatch):
	DEVICE_ID = 0x43
	GROUP_ID = [0x7f, 0x1c]
	REFACE_CP_ID = 0x04
	REFACE_CS_ID = 0x03
	REFACE_DX_ID = 0x05
	REFACE_YC_ID = 0x06

	#dumprequest to get the currently selected patch:
	REFACE_DX_BANK_PANEL = [0x0E, 0x0F, 0x00]

	REFACE_DX_BULK_HEADER = (67, 0, 127, 28, 0, 4, 5, 0x0E, 0x0F, 0, 94)
	REFACE_DX_BULK_FOOTER = (67, 0, 127, 28, 0, 4, 5, 0x0F, 0x0F, 0, 93)

	def __init__(self, port):
		self._receive(port)

	def _send_request(self, port):
		device_number = 0x20

		req = [self.DEVICE_ID, device_number] + self.GROUP_ID +\
			  [self.REFACE_DX_ID] +  self.REFACE_DX_BANK_PANEL

		request = mido.Message('sysex', data=req)
		out_port = self._open_output(port)
		out_port.send(request)


	@classmethod
	def _verify(cls, data):
		if len (data) == 0:
			return cls.VERIFY_INVALID
		else:
			for item in data:
				#TODO checksum
				if not (item[0] == cls.DEVICE_ID and list(item[2:4]) == cls.GROUP_ID and item[6] == cls.REFACE_DX_ID):
					return cls.VERIFY_INVALID

			if len (data) >= 3 and data[0] == cls.REFACE_DX_BULK_HEADER and data[-1] == cls.REFACE_DX_BULK_FOOTER:
				return cls.VERIFY_COMPLETE

			return cls.VERIFY_VALID

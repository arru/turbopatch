from __future__ import print_function

import mido

import SysexPatch


class Z1Patch(SysexPatch.SysexPatch):
	DEVICE_ID = 0x42
	GROUP_ID = 0x46

	BANK_PANEL = 0x10  # Current program - only works when SysExXmit is set to On
	BANK_PROGRAM_UNIT = 0x1c  # A selection of programs depending on spec below
	BANK_ALL_DATA = 0x50  # All  programs, multi, arp patterns, Global, MIDI

	PROGRAM_UNIT_PROG = 0x00000000  # One program, selected by following byte
	PROGRAM_UNIT_BANK = 0x00010000  # One bank, specified by bank nibble
	PROGRAM_UNIT_ALL = 0x00100000  # All programs
	BANK_PROGRAM_UNIT_BANK_A = 0b00000000
	BANK_PROGRAM_UNIT_BANK_B = 0b00000001

	BANK_PANEL_FUNC = 0x40
	BANK_PROGRAM_FUNC = 0x4C

	CHAR_SUBSTITUTES = {0: "", 47: "-"}

	def _request_data(self):
		device_number = 0x30  # 0x3n n = global midi channel

		function_code = self.BANK_PANEL
		unit_code = self.PROGRAM_UNIT_PROG + self.BANK_PROGRAM_UNIT_BANK_A
		program_number = 99  # Ignored except with PROGRAM_UNIT_PROG

		req_data = [self.DEVICE_ID, device_number, self.GROUP_ID, function_code]
		if function_code == self.BANK_PROGRAM_UNIT:
			req_data.extend([unit_code, program_number])
		req_data.append(0x00)

		return req_data

	def _get_name(self):
		name = ""
		data = self._data[0].data

		if data[3] == self.BANK_PANEL_FUNC:
			name_offset = 6
		elif data[3] == self.BANK_PROGRAM_FUNC:
			name_offset = 8
		else:
			raise NotImplementedError("Can't extract name from unsupported patch format (%x)" % data[3])

		for c in data[name_offset:(name_offset + 18)]:
			if c in self.CHAR_SUBSTITUTES:
				name = name + self.CHAR_SUBSTITUTES[c]
			else:
				name = name + chr(c)

		name = name.strip()
		return name

	@classmethod
	def _verify(cls, msg_list):
		if len(msg_list) == 0:
			return cls.VERIFY_INVALID
		else:
			data = msg_list[0].data

			if not (data[0] == cls.DEVICE_ID):
				return cls.VERIFY_INVALID

			if data[3] == cls.BANK_PANEL_FUNC:
				if len(data) == 664:
					return cls.VERIFY_COMPLETE

			if data[3] == cls.BANK_PROGRAM_FUNC:
				if len(data) == 666:
					return cls.VERIFY_COMPLETE

			return cls.VERIFY_INVALID

#!/usr/bin/env python

import sys
import mido
import SysexPatch

device_name = sys.argv[1]
if len(sys.argv) == 2:
	portname = None
else:
	portname = sys.argv[2]

device_class = SysexPatch.load_device_class(device_name, portname)

try:
	patch = device_class(portname)
except IOError:
	"\n".join(mido.get_input_names())
	raise

print "Received patch %s, done" % patch.get_name()

patch.write_syx("%s.syx" % patch.get_name())

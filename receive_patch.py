#!/usr/bin/env python

import importlib
import mido
import sys
import re

module_name = re.match("^[a-zA-Z_]+$", sys.argv[1]).group(0)
class_name = "%sPatch" % (module_name)
if len(sys.argv) == 2:
	portname = None
else:
	portname = sys.argv[2]

module = importlib.import_module(module_name)

device_class = getattr(module, class_name)
try:
	patch = device_class(portname)
except IOError:
	"\n".join(mido.get_input_names())
	raise

print "Received patch %s, done" % patch.get_name()

patch.write_syx("%s.syx" % patch.get_name())

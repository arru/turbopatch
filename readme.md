TurboPatch
==========

Convenient, automated SysEx patch archive and restore.

Features
--------
Easy, scriptable computer-initiated downloading of sysex data to .syx file. Files named from name set in patch.

Supported instruments
---------------------
* Waldorf Streichfett
* Yamaha Reface DX

…and the utility has been designed for maximum ease when writing new support classes.

receive_patch.py usage
----------------------
```
receive_patch.py instrument [MIDI port name]

Receive SysEx patch from MIDI instrument, write .syx file in working directory

positional arguments:
  instrument            Instrument type - 'Streichfett' or 'Reface'

optional arguments:
  MIDI port name        Name of the MIDI port to communicate with. Can be omitted if only one instrument of its kind is connected through USB.

```

Requirements
------------
* [MIDO python module](https://pypi.python.org/pypi/mido/1.1.3) `pip install mido`
* Your choice of the three backends supported by MIDO. I recommend RTMIDI for ease of installation.

Compatibility
-------------

This is third party hobbyist software. No guarantee is made about its accuracy, quality or feature-coverage.

License
-------
TurboPatch project copyright © 2016 Arvid Rudling.

This Source Code Form is subject to the terms of the Modified BSD License. If a copy of the Modified BSD License was not distributed with this file, You can obtain one at https://opensource.org/licenses/BSD-3-Clause.

All trademarks are the property of their respective owners.

The software is developed without any affiliation to Yamaha, Waldorf or other manufacturers of supported instruments.

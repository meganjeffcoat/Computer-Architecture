#!/usr/bin/env python3
#Main

"""Main."""

import sys
from cpu import *

if len(sys.argv) == 2:

    cpu = CPU()

    cpu.load(sys.argv[1])
    cpu.run()
else:
    print("Please provide filename to execute instrustions")
    sys.exit(1)
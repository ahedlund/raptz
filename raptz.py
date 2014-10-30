#!/usr/bin/python2

# BSD New Licence (c) 2012 Jonas Zetterberg

import sys

sys.path.append("/usr/share/pyshared/")

from Raptz import Raptz, RaptzError
import atexit


def raptz_exit(raptz):
	raptz.umount_all()

if __name__=="__main__":
	debug = False
	ret = 1
	try:
		raptz = Raptz()
		atexit.register(raptz_exit, raptz)
		debug = raptz.args.debug
		ret = raptz.start()
	except KeyboardInterrupt:
		print ""
		print ""
		print "It looks like you have canceled the Sysroot installation. Installation is not complete."
	except RaptzError, why:
		print ""
		print ""
		print "Failed to create sysroot: " + str(why)
	except BaseException,why:
		print ""
		print ""
		print "Got Base exception ", repr(why), ". Installation failed."
		if debug:
			raise
	except Exception, why:
		print ""
		print ""
		print "Got exception", repr(why), ". Installation failed."
		if debug:
			raise
	exit(ret)

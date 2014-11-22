#!/usr/bin/python

import sys
import os
import select
from cbpoller import CbPoller
from chroot import FakeRoot, ChRoot
from ui import UiLog, UiTerm
from fs import FakeFs, RootFs
from raptzerror import RaptzException

from config import config

class Host():
	def __init__(self):
		self._stdoutfd = sys.stdout.fileno()
		self._stderrfd = sys.stderr.fileno()
		self._log = open(config.args.logfile, "w")
		self._outcb = {}
		self._errcb = {}
		self._outline = ""
		self._errline = ""
		self.poller = CbPoller()
		if config.args.ui == "term":
			self._ui = UiTerm()
			self.redirout()
		else:
			self._ui = UiLog()
		if config.args.mode == "fake":
			self.fs = FakeFs(self)
			self.runner = FakeRoot(self)
		elif config.args.mode == "root":
			if os.getuid() != 0:
				raise RaptzException("You shall be root to run in root mode")
			self.fs = RootFs(self)
			self.runner = ChRoot(self)

	def redirout(self):
		pin, self._stdoutfd = os.pipe()
		self.poller.add(pin, self._stdout)
		pin, self._stderrfd = os.pipe()
		self.poller.add(pin, self._stderr)

	def set_parts(self, parts):
		self._ui._parts = parts

	def add_outcb(self, cb, *kargs):
		if cb:
			self._outcb[cb] = kargs	
	def add_errcb(self, cb, *kargs):
		if cb:
			self._errcb[cb] = kargs

	def remove_outcb(self, cb):
		if cb and cb in self._outcb:
			del self._outcb[cb]

	def remove_errcb(self, cb):
		if cb and cb in self._errcb:
			del self._errcb[cb]

	ENDMARKERS = ["\n", "\r"]
	def _stderr(self, fd, ev):
		if ev != select.POLLIN:
			return True
		ch = os.read(fd,1)
		self._log.write(ch)
		if ch not in self.ENDMARKERS:
			self._errline += ch
			return True
		self._log.flush()
		for cb, kargs in self._errcb.items():
			if not cb(self._errline, *kargs):
				self.remove_errcb(cb)
		self._errline=""
		return True

	def _stdout(self, fd, ev):
		if ev != select.POLLIN:
			return True
		ch = os.read(fd,1)
		self._log.write(ch)
		if ch not in self.ENDMARKERS:
			self._outline += ch
			return True
		self._log.flush()
		self._ui.text(self._outline)
		for cb, kargs in self._outcb.items():
			if not cb(self._outline, *kargs):
				self.remove_outcb(cb)
		self._outline=""
		return True

	def stdoutfd(self):
		return self._stdoutfd

	def stderrfd(self):
		return self._stderrfd

	def start(self, name):
		self._ui.start(name)
		self._log.write("*** " + name + " ***\n")
		return self

	def warn(self, text):
		self._ui.warn(text)

	def dbg(self, text):
		if config.args.debug:
			self._ui.dbg(text)

	def progress(self, prog, text=None):
		self._ui.progress(prog)

	def text(self, text):
		self._log.write("** " + text + "\n")
		self._ui.text(text)

	def done(self):
		self._ui.done()




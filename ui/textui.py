
from baseui import BaseUI
import time as ttt
from time import time

ANIM=(
	"  (^_^/)  ",
	" <(^_^<)  ",
	" <(^_^ )> ",
	" <( ^_^)> ",
	"  (>^_^)> ",
	"  (\\^_^)  ",
	None)

def animate():
	global v
	try:
		v = v + 1
	except NameError:
		v = 0
	if ANIM[v / 3] == None:
		v = 0
	return ANIM[v / 3]

class Group():
	def __init__(self, label="Init", subgroup=0, lines=0):
		"""
		Initialize a Group as a top most child
		"""
		self.label = label
		self.subgroup = subgroup
		self.totlines = lines
		self.child = None
		self.lines = lines
		self.cline = 0
		self.time = 0.0

	def set_lines(self, lines):
		if self.child:
			self.child.set_lines(lines)
		else:
			self.lines = lines
			self.cline = 0
	
	def line(self, text, pre=""):
		"""
		Top most child will print the text
		"""
		if self.child:
			return self.child.line(text, pre + self.label + ":")
		self.cline = self.cline + 1
		t = time()
		if t - self.time < 1.0/60:
			return
		self.time = t
		print "\r\033[K",
		if not self.lines:
			print "".join([animate()]*3 + [ pre, self.label, ": ", str(self.cline) , " lines"]),
		else:
			print "".join([animate()]*3 + [ pre, self.label, ": ", str(self.cline * 100 / self.lines) , "%"]),
			

	def done(self):
		"""
		Removes the top most child. If a child returns True it wants to be removed
		"""
		if not self.child:
			print "\r\033[K", self.label, "Done ", self.cline, " lines"
			return True
		if self.child.done():
			self.child = None
		return False

	def sub(self, text, lines):
		"""
		Generates a new child and returns the new child
		"""
		if self.child:
			return self.child.sub(text, lines)
		self.child = Group(text, self.subgroup + 1, lines)
		return self.child

class UI(BaseUI):
	def __init__(self, logfile):
		BaseUI.__init__(self, logfile)
		self.group = None

	def set_lines(self, lines):
		self.group.set_lines(lines)

	def start(self, text, lines=None):
		BaseUI.start(self, text, lines)
		if self.group:
			self.group.sub(text, lines)
		else:
			self.group = Group(text, 0, lines)

	def stop(self):
		BaseUI.stop(self)
		if not self.group:
			print "No print group!"
			raise
		if self.group.done():
			self.group = None

	def line(self, text):
		BaseUI.line(self, text)
		self.group.line(text)
	
	def message(self, text):
		BaseUI.message(self, text)
		print ""
		print text
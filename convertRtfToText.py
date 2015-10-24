from pyth.plugins.rtf15.reader import Rtf15Reader
from pyth.plugins.plaintext.writer import PlaintextWriter

def convertRtfToText(path):
	doc = Rtf15Reader.read(open(path))
	return PlaintextWriter.write(doc).getvalue()
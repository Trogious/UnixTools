#!/usr/bin/python

import glob, sys, re

reGroup = re.compile('{[^{}]*}', re.I)

def expandBraces(entry):
	if entry is None:
		return None
	expandedEntries = []
	print('e ' + entry)
	match = reGroup.search(entry)
	if match is not None:
		group = match.group()
		items = group[1:-1].split(',')
		for item in items:
			#print('i: ' + item)
			expanded = entry[:match.start()] + item + entry[match.end():]
			#print('e: ' + expanded)
			expandedEntries = expandedEntries + expandBraces(expanded)
	else:
		if entry in expandedEntries:
			expandedEntries = []
		else:
			expandedEntries = [entry]
	return expandedEntries

if len(sys.argv) > 1:
	for arg in sys.argv[1:]:
		for expanded in expandBraces(arg):
			print('expanded: ' + str(expanded))
			for g in glob.glob(expanded):
				print(g)


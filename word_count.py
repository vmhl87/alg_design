from frequency_analyzer import *

freq = FrequencyAnalyzer()

f = open(input("input file path: "), "r")

only_alpha = True

for line in f:
	buf = ""
	for c in line:
		if ord(c) >= ord("a") and ord(c) <= ord("z"): buf += c
		elif ord(c) >= ord("A") and ord(c) <= ord("Z"): buf += c
		elif not only_alpha and c != " " and c!= "\n": buf += c
		else:
			if len(buf) > 0: freq.add(buf)
			buf = ""
	
	if len(buf) > 0: freq.add(buf)

def n_lines(start, end=False):
	a,b=0,start
	if end:
		a,b=start,end
	for i in range(a,b):
		print(str(i)+": "+freq.nthMostCommon(i)+", occurs "+str(freq.occurencesOf(freq.nthMostCommon(i)))+" times")

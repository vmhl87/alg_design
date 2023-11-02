import time

def GenericSort(arr):
	# analyze array and merge sort or counting sort
	# it actually turns out that my hybrid counting sort
	# implementation not only can work on datasets with
	# a lot of variance in key value (i.e. float arrays)
	# but also has worst case time complexity barely above
	# plain mergesort (it uses mergesort for key ordering)
	
	# however, it requires our data to be able to be stringified
	if not callable(getattr(arr[0], "__str__")):
		# bailout
		return MergeSort(arr).arr
	
	# we now want to analyze our dataset and decide whether or
	# not it will be worth it to countingsort. To do this we
	# will look at the string representations of the first few
	# elements and see how long they are and how much they vary
	
	# we will store a temporary previous string and a seperate
	# string of 0/1's to represent which values in the string
	# will vary
	tempString = ""
	variance = ""
	for i in range(min(len(arr), 3 + max(50,int(len(arr)/50)))):
		j = str(arr[i])
		
		if len(j) > len(variance):
			tempString += j[len(variance):]
			
			for _ in range(len(j)-len(variance)):
				variance += "0"
		
		for i in range(len(j)):
			if variance[i] == "0":
				if j[i] != tempString[i]:
					variance = variance[:i] + "1" + variance[i+1:]
	
	uniqueChars = 0
	for i in range(len(j)):
		if variance[i] == "1":
			uniqueChars += 1
	
	# we now will do analysis on the approximate # of possibilities
	# of a string of length uniqueChars vs. the length of our data
	
	# essentially we take 26 ^ uniqueChars and see if it is greater
	# than the length of the array
	product = 1
	for i in range(uniqueChars):
		product *= 26
		if product > len(arr):
			return MergeSort(arr).arr
	
	return CountingSort(arr).arr


class CountingSort:
	def __init__(self, arr):
		# we do not want to assume that our data is linearizable
		# into a range of integers, so we must find a different way
		# to represent our data in an array-like form. A hashmap
		# seems like the obvious choice, however, we lose the ability
		# to pre-sort our keys (when using a dataset that maps its
		# keys directly to indexes of an array, it is trivial to
		# compile the sorted array from the buffer array). To combat
		# this we store a separate array of individual keys (sortableKeys)
		# and use it to pull the count values out of our HashMap in the
		# correct order.
		self.keyMap, self.sortableKeys, self.keys = {}, [], 0
		self.arr = arr
		
		self._generateKeyMap()
		
		self._combineKeys()
	
	def _generateKeyMap(self):
		# iterate through our input array
		for i in self.arr:
			# we call str() to generate a value we can use as
			# a key in our hashmap - if we are working with custom
			# data classes, they must implement an __str__ method
			# if str() is not implemented we must bailout into standard
			# mergesort
			if not callable(getattr(i, "__str__")):
				# bailout!
				self._bailout()
			
			# if this key has not been put into the keymap, do so,
			# if not increment its count
			if str(i) not in self.keyMap:
				self.keyMap[str(i)] = {"count": 0, "id": self.keys}
				self.sortableKeys.append(i)
				self.keys += 1
			
			self.keyMap[str(i)]["count"] += 1
		
		# sort self.sortableKeys (mergesort works fine)
		self.sortableKeys = MergeSort(self.sortableKeys).arr
	
	def _bailout(self):
		# apparently our data is unable to be sorted properly
		# with counting sort, so we will default to mergesort
		
		# first we wipe keymap, keys, etc
		self.keyMap = {}
		self.sortableKeys = []
		self.keys = 0
		
		# then we fill in self.arr (_combineKeys will bailout too)
		final = MergeSort(self.arr).arr
		self.arr = final
	
	def _combineKeys(self):
		# check if bailout happened
		if self.keys == 0:
			return
		
		# overwrite self.arr (it was previously used to store
		# values of original array as a buffer)
		self.arr = []
		
		# iterate through the sorted keys and append each value the
		# corresponding number of times
		for i in self.sortableKeys:
			# keyMap tells us how many times this key has appeared through
			# our dataset, and str(i) is the key we search for
			for _ in range(self.keyMap[str(i)]["count"]):
				self.arr.append(i)


class MergeSort:
	def __init__(self, arr):
		self.arr = self._mergeSort([i for i in arr])
	
	def _mergeSort(self, arr):
		# mostly reused from our earlier mergesort implementation homework
		if len(arr) == 1: return arr
		
		split_index = int(len(arr)/2)
		
		sub_array_1 = self._mergeSort(arr[:split_index])
		sub_array_2 = self._mergeSort(arr[split_index:])
		
		return self._mergeArrays(sub_array_1, sub_array_2)
	
	def _mergeArrays(self, a, b):
		final = []
		
		look_index_1, look_index_2 = 0, 0
		
		while look_index_1 < len(a) and look_index_2 < len(b):
			# if we are working with custom data classes they must implement
			# an __lt__ method (<) - but other than that this is essentially
			# unchanged
			if a[look_index_1] < b[look_index_2]:
				final.append(a[look_index_1])
				look_index_1 += 1
			else:
				final.append(b[look_index_2])
				look_index_2 += 1
		
		for i in range(look_index_1, len(a)): final.append(a[i])
		for i in range(look_index_2, len(b)): final.append(b[i])
		
		return final


class Birthday:
	def __init__(self, month, day, occurances):
		self.date = Birthday.dayNumber(month, day)
		self.month = month
		self.day = day
		self.occurances = occurances
	
	# we will make these utilities class methods in case we
	# want to use them elsewhere in our code
	
	@classmethod
	def dayNumber(Birthday, month, day):
		totalDays = day
		
		# pretty simple - just sum up all the days in all the months leading up to month
		for i in range(1, month):
			totalDays += Birthday.daysInMonth(i)
		
		return totalDays
	
	@classmethod
	def daysInMonth(Birthday, month):
		if month == 2: return 28
		
		# a cool pattern - I noticed that all the months with 31 days are
		# exactly both {odd numbered months, before August} or none of the two
		# implemented with xor and ternary operator
		return 30 if (month%2 > 0)^(month < 8) else 31
	
	# __lt__ and __str__ methods must be implemented for
	# mergesort and countingsort to work effectively; specifically,
	# __str__ must generate string-based representation of the data
	# contained in this class such that for any two instances of this
	# class which represent the same date, their string-based representation
	# will be identical, and for any two instances of this class which
	# represent distinct dates, their representations will be distinct.
	
	# we reverse this operator to sort highest to lowest rather than
	# lowest to highest
	def __lt__(self, other):
		return self.occurances > other.occurances
	
	def __str__(self):
		return str(self.date)

# open file
f = open("in.csv", "r")
print("opened file")

# initialize an array to store occurances of each birthday
a = time.time_ns()
birthdayCounts = [{"count": 0, "month": 0, "day": 0} for i in range(365)]
print("array init ("+str(int((time.time_ns()-a)/1000000))+" ms)")

# read the input file and increment birthday counts
print("initializing data...")
a = time.time_ns()
for date in f:
	pair = date.split(",")
	index = Birthday.dayNumber(int(pair[0]), int(pair[1])) - 1
	birthdayCounts[index]["count"] += 1
	birthdayCounts[index]["month"] = int(pair[0])
	birthdayCounts[index]["day"] = int(pair[1])
print("data init ("+str(int((time.time_ns()-a)/1000000))+" ms)")

# format our counting array into an array of data structures compatible with genericSort
a = time.time_ns()
sortableCounts = [Birthday(i["month"], i["day"], i["count"]) for i in birthdayCounts]
print("processed array ("+str(int((time.time_ns()-a)/1000000))+" ms)")

# sort our array
print("sorting...")
a = time.time_ns()
sortedCounts = GenericSort(sortableCounts)
print("sorted! ("+str(int((time.time_ns()-a)/1000000))+" ms)")

# write out to file
f = open("birthdays_sorted.txt", "w")
for i in sortedCounts:
	f.write(str(i.month) + "," + str(i.day) + "," + str(i.occurances) + "\n")

f.close()
print("done")

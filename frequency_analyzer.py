
class FrequencyAnalyzer:
	def __init__(self):
		self._counts = {}
		self._keys = []
		self._analyzed = False
	
	def add(self, item):
		self._analyzed = False
		
		itemKey = str(item)
		
		if itemKey not in self._counts:
			self._counts[itemKey] = 0
			self._keys.append(item)
		
		self._counts[itemKey] += 1

	def extend(self, itemArr):
		for item in itemArr:
			self.add(item)

	def _analyze(self):
		self._keys = self._mergeSort(self._keys)
		
		self._analyzed = True
	
	def _mergeSort(self, arr):
		if len(arr) < 2: return arr
		
		splitIndex = int(len(arr)/2)

		arr1, arr2 = self._mergeSort(arr[:splitIndex]), self._mergeSort(arr[splitIndex:])

		final = []

		index1, index2 = 0, 0

		while index1 < len(arr1) and index2 < len(arr2):
			if self._counts[str(arr1[index1])] > self._counts[str(arr2[index2])]:
				final.append(arr1[index1])
				index1 += 1
			else:
				final.append(arr2[index2])
				index2 += 1

		for i in range(index1, len(arr1)): final.append(arr1[i])
		for i in range(index2, len(arr2)): final.append(arr2[i])
		
		return final

	def frequencyOf(self, item):
		itemKey = str(item)

		for i in range(len(self._keys)):
			if self._keys[i] == itemKey:
				return i

		return 0	
	
	def occurencesOf(self, item):
		if not self._analyzed:
			self._analyze()

		itemKey = str(item)

		if itemKey not in self._counts:
			return 0

		return self._counts[itemKey]

	def nthMostCommon(self, n):
		if not self._analyzed:
			self._analyze()

		if n < 0 or n >= len(self._keys):
			if len(self._keys) == 0:
				return False

			return self._keys[0]
		
		return self._keys[n]

	def getAll(self):
		if not self._analyzed:
			self._analyze()
		
		outArr = []

		for item in self._keys:
			outArr.append({"count": self._counts[str(item)], "item": item})

		return outArr

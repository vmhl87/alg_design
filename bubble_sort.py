import random # necessary for random number generation

def bubble_sort(arr):
	# Essentially we will pass over the array, from start to finish, and
	# swap out-of-place elements, until we encounter a pass in which we
	# find 0 out-of-place elements, and then we return the sorted array
	
	# First we clone the original array so that we have a mutable array
	# to work with - we label it sorted even though it isn't fully yet
	sorted_array = []
	for i in arr: sorted_array.append(i)
	
	# Because we do not know how many times we must iterate over the
	# array, we will use a while loop, and keep track of whether or not
	# we are still unsorted with a variable - which we assume to be true
	# at the start
	is_unsorted = True
	
	while is_unsorted:
		# We assume that the array is sorted until we find that it isn't
		is_unsorted = False
		
		# We are comparing pairs of elements, so we will only need to
		# iterate length - 1 times
		for i in range(len(arr)-1):
			# The elements being compared are arr[i] and arr[i+1], but
			# we reference our local copy sorted_array
			if sorted_array[i]>sorted_array[i+1]:
				# Rather than creating a temporary variable for storing
				# the value of the elements while swapping, we can use
				# this interesting algorithm:
				
				# Compute the difference between the two values, and set
				# the first value to this value
				sorted_array[i] -= sorted_array[i+1]
				
				# Add the difference to the second value, converting it
				# into what the first value used to be
				sorted_array[i+1] += sorted_array[i]
				
				# Compute the previous value of the second value by sub-
				# -tracting the difference
				sorted_array[i] = sorted_array[i+1] - sorted_array[i]
				
				# Because we found elements out of place, we must set
				# unsorted indicator to true
				is_unsorted = True
	
	return sorted_array

# --- driver code ---

def display_array(arr):
	values_string = ""
	vertical_table = []
	
	for i in arr:
		values_string += str(i) + " "
		i_str = ""
		
		for j in range(int(len(arr)*.6)):
			if j<i*.6: i_str = "#" + i_str
			else: i_str = " " + i_str
		
		vertical_table.append(i_str)
	
	horizontal_table = []
	for i in range(int(len(arr)*.6)):
		i_str = ""
		
		for j in range(len(arr)):
			i_str += vertical_table[j][i:i+1]
			
		horizontal_table.append(i_str)
	
	print("Raw values:\n" + values_string)
	print("\nTable:")
	for i in horizontal_table: print(i)

unsorted_array = []

for i in range(25):
	unsorted_array.append(random.randint(0, 25))

print("=== Unsorted array ===")
display_array(unsorted_array)
print("\n")

sorted_array = bubble_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

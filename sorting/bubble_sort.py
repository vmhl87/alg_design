# bubble_sort.py
# GOAL: implement bubble sort on an integer array
# Code Author: Vincent Loh


import random # necessary for random number generation

def bubble_sort(arr):
	# Essentially we will pass over the array, from start to finish, and
	# swap out-of-place elements, until we encounter a pass in which we
	# find 0 out-of-place elements, and then we return the sorted array
	
	# First we clone the original array so that we have a mutable array
	# to work with - we label it sorted even though it isn't fully yet
	sorted_array = [i for i in arr]
	
	# Because we do not know how many times we must iterate over the
	# array, we will use a while loop, and keep track of whether or not
	# we are still unsorted with a variable - which we assume to be true
	# at the start
	is_sorted = False
	
	while not is_sorted:
		# We assume that the array is sorted until we find that it isn't
		is_sorted = True
		
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
				# tracting the difference
				sorted_array[i] = sorted_array[i+1] - sorted_array[i]
				
				# Because we found elements out of place, we must set
				# sorted indicator to false
				is_sorted = False
	
	return sorted_array

# --- driver code ---  (I may have overdone the array visualization code)

def display_array(arr):
	# print out raw values and a visualized table (this utility has been
	# refactored multiple times, which is why it is stylistically dense)
	print(
		"Raw values:\n" + " ".join([str(i) for i in arr]) + "\nTable:\n" +
		"\n".join([
			"".join([
				"#" if (len(arr)*.6-i-1)<j*.6 else " " for j in arr
			]) for i in range(int(len(arr)*.6))
		]))

unsorted_array = [random.randint(0,25) for i in range(25)]

print("=== Unsorted array ===")
display_array(unsorted_array)
print("\n")

sorted_array = bubble_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)
# --- driver code ---  (I may have overdone the array visualization code)

def display_array(arr):
        # print out raw values and a visualized table (this utility has been
        # refactored multiple times, which is why it is stylistically dense)
        print(
                "Raw values:\n" + " ".join([str(i) for i in arr]) + "\nTable:\n" +
                "\n".join([
                        "".join([
                                "#" if (len(arr)*.6-i-1)<j*.6 else " " for j in arr
                        ]) for i in range(int(len(arr)*.6))
                ]))

unsorted_array = [random.randint(0,25) for i in range(25)]

print("=== Unsorted array ===")
display_array(unsorted_array)
print("\n")

sorted_array = bubble_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)


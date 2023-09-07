# ss_loh.py
# GOAL: implement selection sort on an integer array
# Code Author: Vincent Loh

import random

# We will implement selection sort:
# Essentially, we want to partition our array into two sections, unsorted, and sorted
# We will then iterate through the unsorted, finding the smallest value, and append it
# to the end of the sorted array. We will do this until we have sorted the entire array.
def selection_sort(arr):
	# Because we do not want to modify the initial array, we will clone it
	sorted_array = [i for i in arr]
	
	# Rather than create a new array for the sorted partition, we can divide the
	# array into two parts and specify the index of the separator
	partition_index = 0
	
	# Iterate until the partition index has reached the end of the array
	while partition_index < len(arr):
		# We will keep a running count of the smallest array by storing it as
		# a pair [index, value]
		smallest_index = [partition_index, sorted_array[partition_index]]
		
		# Iterate through all the values of the unsorted array
		for j in range(partition_index, len(arr)):
			# If this value is smaller than the current smallest index, set smallest_index to match
			if sorted_array[j] < smallest_index[1]: smallest_index = [j, sorted_array[j]]
		
		# If smallest index is the first index of the unsorted array, we don't need to swap
		if smallest_index[0] != partition_index:
			# swap the elements of the array
			sorted_array[partition_index], sorted_array[smallest_index[0]] = sorted_array[smallest_index[0]], sorted_array[partition_index]
		
		# We added a new value to sorted_array, so we must increment the partition index to match
		partition_index += 1
	
	# Return the hopefully sorted array!
	return sorted_array

# --- driver code ---  (reused from bubble_sort.py)

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

sorted_array = selection_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

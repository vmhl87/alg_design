# is_loh.py
# GOAL: implement insertion sort on an integer array
# Code Author: Vincent Loh

import random

# Implement insertion sort:
# Similarly to selection sort, we partition the array into unsorted and sorted
# However, rather than finding smallest values and appending to the sorted array,
# we will go in reverse, taking the first value from the unsorted array, and placing
# it in its appropriate place in sorted_array
def insertion_sort(arr):
	# Similarly to selection_sort we must clone the array
	sorted_array = [i for i in arr]
	
	# Again, we must store the index of the separator between unsorted and sorted
	partition_index = 0
	
	# Technically we only need to iterate len(arr) times, but a while loop is
	# more error-proof
	while partition_index < len(arr):
		# We will select the first index of the unsorted array, and because
		# of the way that we are partitioning our array, this index will be
		# directly to the right of the sorted partition. We will iterate down
		# this sorted partition until this element is in the right place.
		
		# To keep track of how far we have iterated down the sorted array, we
		# will set a variable current_index for the current index (and therefore
		# pair of values) that we are looking at
		current_index = partition_index
		
		# we can save an iteration by bounding current_index at 1, because if
		# current_index is 0, we know that this value must be in the right place
		while current_index > 0:
			# If the element before current_index is smaller than the element at
			# current_index, we have found the appropriate position for our value
			if sorted_array[current_index] > sorted_array[current_index - 1]: break
			
			# Swap the array values
			sorted_array[current_index], sorted_array[current_index - 1] = sorted_array[current_index - 1], sorted_array[current_index]
			
			# Because we swapped the current index down by 1, we must update current_index to match
			current_index -= 1
		
		# Because we have added one more value to the sorted array, we must increase its size
		partition_index += 1
	
	# Return our hopefully sorted array!
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

sorted_array = insertion_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

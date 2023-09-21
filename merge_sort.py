# ms_loh.py
# GOAL: implement merge sort on an integer array
# Code Author: Vincent Loh

import random

# We will be implementing Merge Sort, an efficient (n log n) sorting algorithm.
# This algorithm recursively subdivides and sorts the input array into subarrays, and
# then merges them together - hence the name merge sort.
def merge_sort(arr):
	# If the length of the array is 1, it naturally is already sorted.
	# Because this sorting algorithm is recursive, we naturally must have a base case -
	# length 1 is the base case, as it cannot be subdivided further.
	if len(arr) == 1: return arr
	
	# We will create an empty array and push values onto it - the merging algorith is
	# not run in-place.
	sorted_array = []
	
	# Merge sort recursively divides the array in half, and sorts each half. We want to
	# split the array at its midpoint for optimal efficiency.
	split_index = int(len(arr)/2)
	
	# Before we merge the subarrays, we must sort them. We simply call merge_sort to do this.
	sub_array_1, sub_array_2 = merge_sort(arr[:split_index]), merge_sort(arr[split_index:])
	
	# Merging the arrays is relatively simple - assuming that the two subarrays are
	# already sorted, which they should be, we simply have to look at the smallest values
	# in each subarray, and remove the smallest one, putting it into the sorted final array,
	# and repeat. Because removing values from an array is computationally intense, we will
	# store a position for the virtual beginning of each array, and rather than actually
	# delete elements from each subarray, we will just increment each counter. Naturally,
	# they start at 0.
	look_index_1, look_index_2 = 0, 0
	
	# If one of these counters reaches the end of its respective array, we do not need to keep
	# comparing values between arrays. Instead, because we know that a) the remaining subarray
	# is sorted, and b) its values are all larger than the values in our output array, (which
	# we can prove by nature of the merge algorithm), we can simply append all of the values
	# in our remaning subarray onto the output array in order, and they will be in their
	# correct position. Therefore we use a while loop.
	while look_index_1 < len(sub_array_1) and look_index_2 < len(sub_array_2):
		# Because look_index_n indicates the virtual beginning of sub_array_n, we can access
		# the virtual first index of sub_array_n with sub_array_n[look_index_n].
		if sub_array_1[look_index_1] < sub_array_2[look_index_2]:
			# Because the value in sub_array_1 is smaller, this will be the one we push
			# to the output array.
			sorted_array.append(sub_array_1[look_index_1])
			
			# Naturally we must increment the virtual beginning of subarray 1, because
			# by "taking" its first value, its second value is the new first value, and
			# hence should be the next value compared.
			look_index_1 += 1
		else:
			# If sub_array_1 is greater than or equal to sub_array_2 (first value), push
			# the value of sub_array_2. If the two values are equal, it makes no difference.
			sorted_array.append(sub_array_2[look_index_2])
			
			# Similarly we must increment the counter for subarray 2.
			look_index_2 += 1
	
	# Because the while loop completed, we know that at least one of the counters
	# has reached its ending point. We now will append all remaining values to the
	# output array.
	# Though it looks like we are appending elements from both arrays, we will not have any
	# reordering problems, because at least one of these look indexes will be equal to the
	# length of their respective array (due to exit conditions of the while loop) and therefore
	# the subarray associated with it will not push any of its values onto the output array.
	# If we think of these virtual counters as representing removing the end value of the
	# subarray, look_index_n == len(sub_array_n) would indicate that subarray n is empty.
	for i in range(look_index_1, len(sub_array_1)): sorted_array.append(sub_array_1[i])
	for i in range(look_index_2, len(sub_array_2)): sorted_array.append(sub_array_2[i])
	
	# Now we return the hopefully sorted array!
	# Due to the recursive nature of this algorithm, this is not necessarily the final return.
	# Each recursive subdivision and sort calls merge_sort itself, so this could be returning
	# the final array, the first subdivision, the second one, etc.
	return sorted_array

# --- driver code ---

def display_array(arr):
        # standard display code I use in all my sorts
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

sorted_array = merge_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

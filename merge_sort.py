
# ms_loh.py
# GOAL: implement merge sort on an integer array
# Code Author: Vincent Loh

import random

def merge_sort(arr):
	if len(arr) == 1: return arr
	
	sorted_array = []
	
	split_index = int(len(arr)/2)
	
	#sub_array_1, sub_array_2 = arr[:split_index], arr[split_index:]
	sub_array_1, sub_array_2 = merge_sort(arr[:split_index]), merge_sort(arr[split_index:])
	
	look_index_1, look_index_2 = 0, 0
	
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

sorted_array = merge_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

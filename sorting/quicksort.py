
import random

def quick_sort(arr):
	

# --- driver code ---

def display_array(arr):
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

sorted_array = quick_sort(unsorted_array)

print("=== Sorted array ===")
display_array(sorted_array)

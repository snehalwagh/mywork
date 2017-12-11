#Author: Snehal Wagh
#Date: 2017-12-07
#Problem Statement: Implement merge sort in python.
#Solution: Use divide and conqure algorithm to implement this.

#Merge sort is very good example of divide and conquer algorithms

#1. Divide array into two halves
#2. Recursively sort each half
#3. merge 2 halves


#MergeSort(arr[], l, r)
#where l : left index, r : right index

#    if r > l:
#        1. Find middle index to divide given input array
#               mid_element = len(arr)/2
#        2. Call mergeSort for the first half:
#                mergesort(arr, l, m)
#        3. Call mergeSort for the second half:
#                mergesort(arr, m+1, r)
#        4. Merge two halves sorted in step 2 and 3
#                merge(arr, l, m, r)

#Time complexity: nlogn(worst, average and best) as merge sort always divides the array in two halves and take linear time to merge two halves.


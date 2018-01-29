#Author: Snehal Wagh
import sys

def rotate_arr(arr, n):
    for i in range(n-1):
        if i == 0:
            temp = arr[n-1]
            global temp
            arr[n-1] = arr[i]
        else:
            arr[i-1] = arr[i]
    arr[n-2] = temp
    return arr


if __name__=="__main__":
    arr = raw_input('Enter input list:').split(',')
    d = input('rotate array by elemenets:')
    n = len(arr)
    if n <= 1:
        if d == 1:
            print arr
        else:
            print "Not able to rotate"
        sys.exit(0)
    for i in range(d):
        out = rotate_arr(arr, n)
    print "Before rotation: " arr
    print "After rotation:" out


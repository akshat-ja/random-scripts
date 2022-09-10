import random
import time


def naive_search(l, target):
    for i,x in enumerate(l):
        if x == target:
            return i
    return -1

def binary_search(l, target, min_bound=None, max_bound=None):
    # print(l[min_bound:max_bound])
    if min_bound is None:
        min_bound = 0
    if max_bound is None:
        max_bound = len(l) - 1
    mid_point = (max_bound+min_bound) // 2
    if min_bound > max_bound:
        # print(f'Did not find {target}!')
        return -1
    if l[mid_point] == target:
        # print(f'Found {target}!')
        return mid_point
    elif target < l[mid_point]:
        return binary_search(l, target, min_bound, mid_point-1)
    elif target > l[mid_point]:
        return binary_search(l, target, mid_point+1, max_bound)

def main():
    if __name__ == '__main__':
        # l = [1,2,3,4,5,6,7,9,11]
        # target = l[random.randint(0, len(l) - 1)]
        # print(l, target)
        # binary_search(l, target)
        
        length = 10000
        sorted_list = set()
        while len(sorted_list) < length:
            sorted_list.add(random.randint(-3*length, 3*length))
        sorted_list = sorted(list(sorted_list))
        target = sorted_list[random.randint(0, len(sorted_list) - 1)]
        
        start_time = time.time()
        naive_search(sorted_list, target)
        end_time = time.time()
        print("Naive search time is ", (end_time - start_time)/length)
        
        start_time = time.time()
        binary_search(sorted_list, target)
        end_time = time.time()
        print("Binary search time is ", (end_time - start_time)/length)

if __name__ == "__main__":
    main()
import heapq

def heap_sort(arr):

    heapq.heapify(arr)

    sorted_arr = []

    while arr:
        sorted_arr.append(heapq.heappop(arr))

    return sorted_arr


arr = [5, 2, 8, 1, 3]

print(heap_sort(arr))
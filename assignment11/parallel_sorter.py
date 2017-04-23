import numpy as np
from mpi4py import MPI

comm = MPI.COMM_WORLD ## the communicator
rank = comm.Get_rank() ## the rank of the calling process within the communicator
size = comm.Get_size() ## the total number of processes contained in the communicator

N=10000 ## the number of element
low=-10000 ## lower bound
high=10000 ## higher bound

def parallel_sorter():
    ## random list of numbers
    list_numbers = np.random.randint(low,high,N)

    ## split the list
    range_numbers = max(list_numbers) - min(list_numbers)
    range_array = np.array(range(range_numbers+1))
    range_list = np.array_split(range_array, size)

    array_max = []
    for x in range_list:
        array_max.append(max(x))

    split_list=[]
    for i in range(size):
        single_list=[]
        if i == 0:
            for j in list_numbers:
                if j <= array_max[i]:
                    single_list.append(j)
        else:
            for j in list_numbers:
                if j <= array_max[i] and j > array_max[i-1]:
                    single_list.append(j)        
        split_list.append(single_list)

    ## sort the split lists
    if rank==0:
        split_list=split_list
    else:
        split_list=None

    split_list=comm.scatter(split_list, root=0) ## scatter the array to differnt processes

    single_sort=np.sort(split_list) ## sort each array

    final_sort=comm.gather(single_sort,root=0) ## gather all arrays from different processes
    
    if rank==0:
        sorted_list=np.concatenate(final_sort) #flatten sorted arrays
    
    return sorted_list

if __name__ == '__main__':
    main = parallel_sorter()
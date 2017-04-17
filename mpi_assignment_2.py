""" 
Author: Yu-Fen Chiu
Date: 04/16/2017
Question 2: 
Write an MPI program in which the first process get an integer less than 100 and send to the second process.
Then each process multiples the number with their ranks and continues to the last process. 
Then the final result is send to the first process and printed.
Command used: mpiexec -n <size> python mpi_assignment_2.py 
"""

from mpi4py import MPI
import numpy

comm = MPI.COMM_WORLD ## the communicator
rank = comm.Get_rank() ## the rank of the calling process within the communicator
size = comm.Get_size() ## the total number of processes contained in the communicator

randNum = numpy.zeros(1)

if rank == 0:
    while True:
    
        ## ask user to enter a number
        user_input = input("Tell me an integer less than 100: ") 
    
        ## verify that user-entered number is an integer
        try:
            number = int(user_input)
            ## verify that user-entered is less than 100
            if number < 100 and number > 0:
                break
            else:
                print('The number you enter is invalid. Please enter an integer between 0 and 100!')
                continue
        except ValueError:
            print('The number you enter is not an integer. Please try again!')
            continue

    randNum[0] = number
    
    ## send a message to process 1
    comm.Send(randNum, dest = 1)
    
    ## receive the final result
    comm.Recv(randNum, source = size - 1)
    print(randNum[0])

else:    
    ## receive a message from previous process
    comm.Recv(randNum, source = rank - 1)
    
    ## multiply by rank
    randNum *= rank
    
    ## check if it is the last one, then send a message to proper destination
    if rank == size - 1:
        comm.Send(randNum, dest = 0)
    else:
        comm.Send(randNum, dest = rank + 1)
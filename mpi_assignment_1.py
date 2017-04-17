""" 
Author: Yu-Fen Chiu
Date: 04/16/2017
Question 1: 
Write an MPI program in which the processes with EVEN rank print 'Hello' and the processes with ODD rank print 'Goodbye'.
Print the rank along with the message.
Command used: mpiexec -n <size> python mpi_assignment_1.py 
"""

from mpi4py import MPI

comm = MPI.COMM_WORLD ## the communicator
rank = comm.Get_rank() ## the rank of the calling process within the communicator
size = comm.Get_size() ## the total number of processes contained in the communicator

if rank % 2 == 0: ## even rank, print "Hello"
    print('Hello from process', rank)
else: ## odd rank, print "Goodbye"
    print('Goodbye from process', rank)
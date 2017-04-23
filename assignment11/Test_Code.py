import numpy as np
from mpi4py import MPI
import unittest
from parallel_sorter import parallel_sorter

comm = MPI.COMM_WORLD ## the communicator
rank = comm.Get_rank() ## the rank of the calling process within the communicator
size = comm.Get_size() ## the total number of processes contained in the communicator

class Test(unittest.TestCase): ## test whether the array is sorted or not
    def test(self):
        main = parallel_sorter()
        if rank == 0:
            self.assertEqual(np.asarray(sorted(main)).all(), main.all())
        else:
            self.assertEqual(main, None)

if __name__ == '__main__':
    unittest.main()
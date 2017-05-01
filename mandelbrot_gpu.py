# 
# A CUDA version to calculate the Mandelbrot set
#
from numba import cuda
import numpy as np
from pylab import imshow, show

@cuda.jit(device=True)
def mandel(x, y, max_iters):
    '''
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the 
    Mandelbrot set given a fixed number of iterations.
    '''
    c = complex(x, y)
    z = 0.0j
    for i in range(max_iters):
        z = z*z + c
        if (z.real*z.real + z.imag*z.imag) >= 4:
            return i

    return max_iters

@cuda.jit
def compute_mandel(min_x, max_x, min_y, max_y, image, iters):
    '''
    Calculate the mandel value for each element in each of the small 
    portions of the image array by first finding the starting x and y 
    coordinates using `cuda.grid()`, and then getting the strides in 
    x and y directions using `cuda.blockDim` and `cuda.gridDim`.
    The real and imag variables contain a value for each element 
    of the complex space defined by the X and Y boundaries 
    (min_x, max_x) and (min_y, max_y).
    '''
    
    # get image shape
    height = image.shape[0]
    width = image.shape[1]
    
    # calculate the smallest increments
    pixel_size_x = (max_x - min_x) / width
    pixel_size_y = (max_y - min_y) / height
    
    # get starting point
    ystart, xstart = cuda.grid(2)

    # get number of threads per block
    bw = cuda.blockDim.x 
    bh = cuda.blockDim.y

    # get total number of blocks
    gw = cuda.gridDim.x 
    gh = cuda.gridDim.y

    # calculate the stride in x and y direction
    xgrid = bw*gw
    ygrid = bh*gh

    for x in range(xstart, width, xgrid):
        real = min_x + x * pixel_size_x
        for yi in range(ystart, height, ygrid):
            imag = min_y + y * pixel_size_y
            image[y, x] = mandel(real, imag, iters)   
  
    
if __name__ == '__main__':
    image = np.zeros((1024, 1536), dtype = np.uint8)
    blockdim = (32, 8)
    griddim = (32, 16)

    image_global_mem = cuda.to_device(image)
    compute_mandel[griddim, blockdim](-2.0, 1.0, -1.0, 1.0, image_global_mem, 20) 
    image_global_mem.copy_to_host()
    imshow(image)
    show()
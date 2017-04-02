"""
    N-body simulation.
    
    1. Add @jit decorators and function signatures to all funcitons.
    2. Add afunction vec_deltas() that takes two NumPy arrays of floats and returns the difference between each element.
    
    Time: Average(74.060, 55.593, 68.151) = 65.93 sec
    Improvement: 310.4767/65.93 = 4.709187x
"""
import time
from itertools import combinations
import numpy as np
from numba import jit, void, int32, float64, vectorize

@vectorize([float64(float64, float64)]) ## update: decorator and signature
def vec_deltas(x, y): ## update: add new function to replace compute_delta
    '''
    compute difference between each element in arrays. 
    '''
    return x - y

@jit("void(float64[:,:,:], char[:,:], float64[:,:,:], float64)") ## update: decorator and signature
def report_energy(BODIES, body1_2, val, e=0.0):
    '''
        compute the energy and return it so that it can be printed
    '''
    for (body1,body2) in body1_2:             
        (x1y1z1, v1, m1) = BODIES[body1] ## update first element
        (x2y2z2, v2, m2) = BODIES[body2] ## update first element
        (dx, dy, dz) = vec_deltas(x1y1z1, x2y2z2) ## update: compute difference
        e -= (m1 * m2) / ((dx * dx + dy * dy + dz * dz) ** 0.5)     
    for body in val:
        (r, [vx, vy, vz], m) = body
        e += m * (vx * vx + vy * vy + vz * vz) / 2.    
    return e

@jit("void(int32, float64[:,:,:], float64, float64, float64)") ## update: decorator and signature
def offset_momentum(ref, val, px=0.0, py=0.0, pz=0.0):
    '''
        ref is the body in the center of the system
        offset values from this reference
    '''
    for body in val:
        (r, [vx, vy, vz], m) = body
        px -= vx * m
        py -= vy * m
        pz -= vz * m
        
    (r, v, m) = ref
    v[0] = px / m
    v[1] = py / m
    v[2] = pz / m

@jit("void(int32, char, int32, float64[:,:,:], float64 )") ## update: decorator and signature
def nbody(loops, reference, iterations, BODIES, dt=0.01):
    '''
        nbody simulation
        loops - number of loops to run
        reference - body at center of system
        iterations - number of timesteps to advance
        advance the system one timestep
    '''
    # Set up global state   
    offset_momentum(BODIES[reference], val)
    
    for _ in range(loops):
        report_energy(BODIES, body1_2[:], val)
        for _ in range(iterations):
            for (body1,body2) in body1_2:             
                (x1y1z1, v1, m1) = BODIES[body1] ## update first element
                (x2y2z2, v2, m2) = BODIES[body2] ## update first element
                (dx, dy, dz) = vec_deltas(x1y1z1, x2y2z2) ## update: compute difference
                mag = dt * ((dx * dx + dy * dy + dz * dz) ** (-1.5))
                b2 = m2 * mag
                b1 = m1 * mag
                v1[0] -= dx * b2
                v1[1] -= dy * b2
                v1[2] -= dz * b2
                v2[0] += dx * b1
                v2[1] += dy * b1
                v2[2] += dz * b1
            for body in val:
                (r, [vx, vy, vz], m) = body
                r[0] += dt * vx
                r[1] += dt * vy
                r[2] += dt * vz
        print(report_energy(BODIES, body1_2[:], val))

if __name__ == '__main__':
    t = time.time()

    PI = 3.14159265358979323
    SOLAR_MASS = 4 * PI * PI
    DAYS_PER_YEAR = 365.24

    ## update: first element of each tuple to a NumPy array
    BODIES = {
        'sun': (np.array([0.0, 0.0, 0.0],dtype=np.float64), [0.0, 0.0, 0.0], SOLAR_MASS),

        'jupiter': (np.array([4.84143144246472090e+00,
                     -1.16032004402742839e+00,
                     -1.03622044471123109e-01],dtype=np.float64),
                    [1.66007664274403694e-03 * DAYS_PER_YEAR,
                     7.69901118419740425e-03 * DAYS_PER_YEAR,
                     -6.90460016972063023e-05 * DAYS_PER_YEAR],
                    9.54791938424326609e-04 * SOLAR_MASS),

        'saturn': (np.array([8.34336671824457987e+00,
                    4.12479856412430479e+00,
                    -4.03523417114321381e-01],dtype=np.float64),
                   [-2.76742510726862411e-03 * DAYS_PER_YEAR,
                    4.99852801234917238e-03 * DAYS_PER_YEAR,
                    2.30417297573763929e-05 * DAYS_PER_YEAR],
                   2.85885980666130812e-04 * SOLAR_MASS),

        'uranus': (np.array([1.28943695621391310e+01,
                    -1.51111514016986312e+01,
                    -2.23307578892655734e-01],dtype=np.float64),
                   [2.96460137564761618e-03 * DAYS_PER_YEAR,
                    2.37847173959480950e-03 * DAYS_PER_YEAR,
                    -2.96589568540237556e-05 * DAYS_PER_YEAR],
                   4.36624404335156298e-05 * SOLAR_MASS),

        'neptune': (np.array([1.53796971148509165e+01,
                     -2.59193146099879641e+01,
                     1.79258772950371181e-01],dtype=np.float64),
                    [2.68067772490389322e-03 * DAYS_PER_YEAR,
                     1.62824170038242295e-03 * DAYS_PER_YEAR,
                     -9.51592254519715870e-05 * DAYS_PER_YEAR],
                    5.15138902046611451e-05 * SOLAR_MASS)}

    val = BODIES.values()
    body1_2 = np.array(list(combinations(BODIES, 2)))
    nbody(100, 'sun', 20000, BODIES)
    print("nbody_numba.py %.3f" % (time.time()-t))
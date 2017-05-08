'''
Name: Yu-Fen Chiu (yfc259)
Date: May,7,2017
Command: spark-submit squareroot_spark.py
Assignment 13-3:
    Calculate the average of the square root of all the numbers from 1 to 1000.
'''

from pyspark import SparkContext
from operator import add
from math import sqrt

if __name__ == '__main__':
    sc = SparkContext("local", "squareroot")
    nums = sc.parallelize(range(1,1000+1)) # create an RDD from 1 to 1000
    sqrts = nums.map(sqrt) # mapping with square root function
    average = sqrts.fold(0, add) / sqrts.count() # calculate the average
        
    print(average)

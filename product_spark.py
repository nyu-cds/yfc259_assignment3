'''
Name: Yu-Fen Chiu (yfc259)
Date: May,7,2017
Command: spark-submit product_spark.py
Assignment 13-2:
    Calculates the product of all the numbers from 1 to 1000 and prints the result.
'''

from pyspark import SparkContext
from operator import mul

if __name__ == '__main__':
    sc = SparkContext("local", "product")
    nums = sc.parallelize(range(1,1000+1)) # create an RDD from 1 to 1000
    product = nums.fold(1,mul) # get product via fold method
    
    print(product)
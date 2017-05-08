'''
Name: Yu-Fen Chiu (yfc259)
Date: May,7,2017
Command: spark-submit distinct_spark.py
Assignment 13-1:
    Count the number of distinct words in the input text.
'''
from pyspark import SparkContext
import re

# remove any non-words and split lines into separate words
# finally, convert all words to lowercase

def splitter(line):
    line = re.sub(r'^\W+|\W+$', '', line)
    return map(str.lower, re.split(r'\W+', line))

if __name__ == '__main__':
    sc = SparkContext("local", "distinct")
    
    text = sc.textFile('pg2701.txt') # read text file
    words = text.flatMap(splitter) # split lines into seperate words
    words_mapped = words.map(lambda x: (x,1)) # mapping
    words_distinct = words_mapped.distinct().count() # return distinct elements and count the number

    print(words_distinct)
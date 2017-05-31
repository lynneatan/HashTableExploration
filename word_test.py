import matplotlib.pyplot as plt 
import numpy as np
from HashTables import DoubleHashTable, HashTable

def word_test()
%matplotlib inline


	words = open('words.txt').readlines()
	words = words[0:len(words)/4]

	word_table = DoubleHashTable(len(words))
	counter = 0

	from timeit import default_timer as timer
	time_passed = [] 
	time_storer = 0

	for word in words:
	    start = timer()
	    word_table.insert(word)
	    end = timer()
	    
	    time_storer = time_storer + (end-start)
	    counter += 1
	    
	    if counter % 1000 == 0:
	        time_passed.append(time_storer) # appending to my list
	        
	        #print "{0}/{1} words inserted, time {2}".format(counter, len(words), time_storer)
	        time_storer = 0
	
	plt.plot(time_passed)
	plt.show()
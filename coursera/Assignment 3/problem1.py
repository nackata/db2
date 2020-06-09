import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
	
	value = record[1]
	key = record[0]



	for word in value.split():
		mr.emit_intermediate(word,key)
		
def check(key,list_of_values):
	count = 0
	for value in list_of_values:
		count+=value
	mr.emit((key,count))

def reducer(key, list_of_values):
	result=[]
	for document_ID in list_of_values:
		if document_ID not in result:
			result.append(document_ID)
	mr.emit((key, result))

inputdata = open(sys.argv[1])
mr.execute(inputdata,mapper,reducer)

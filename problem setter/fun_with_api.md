## Problem name
Fun with Api

## Problem Statement
Today was something different at work ,I was asked to deal with web pages & API rather than solving algorithmic problems.  
And yes even I was shocked to see the unnatural behavior of this web page.

Given a url='http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing=400'

Each time I visit this page it says nothing but an index,so I go to the following index but that too points to next index and says nothing.

I am confused!!  
I have been told to perform certain tasks which I think I won't be able to complete on time. Help me to complete the tasks on time.

## Task :
1) with the help of above URL find all the indices and store till it doesn't point further.
2) using these indices find the index which is prime number using the below-given API
http://mezurashi.co/products/prime-number-api
## Input format  
A single line showing the starting index.

## output format
for each index print the index and True if it is a prime number and False if it's not.  
index+" "+:+" "True/False  
.  
.  
.  


## input
400

## Output :  
400 : False  
9905 : False  
.  
.  


## my program
```python
import requests 
import json 
index=str(input())
while True: 
	payload={'nothing':index} 
	print(index+' : '+str(json.loads(requests.get('http://numbers.mezurashico.com/primes/'+index).text)['prime'])) 
	re=requests.get('http://www.pythonchallenge.com/pc/def/linkedlist.php',params=payload) 
	s=(re.text).split(' ') 
	if s[0]=='peak.html': 
		break 
	index=s[-1] 
	pass 

```

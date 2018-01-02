from io import StringIO
import socket
import pandas as pd
import re

class titaniumLite:
	
	def __init__(self, host = '127.0.0.1', port = 8080):
		self.s = socket.socket()         
		self.host = host
		self.port = port               
		# self.s.bind((self.host,self.port))	
		self.s.connect((self.host, self.port))
		

	def __del__(self):
		self.s.close()

	def execute(self, query):

		#-----------------------------------------
		dfNeeded=False
		if(bool(re.match('select',query,re.I))): #check if query is of type 'select', case insensitive.
			dfNeeded = True
		#-----------------------------------------
		
		self.s.send(query.encode())
		temp = self.__dataframe(self.s.recv(2024),dfNeeded)
		return temp
		
	def __dataframe(self, output, dfNeeded=False):
		table = output
		tableCopy = table.decode()
		
		if not dfNeeded: #Non 'select' type queries
			return tableCopy
		
		else: #'select' type query, return dataframe
			charsToReplace = ['+','-']
			for char in charsToReplace:
				tableCopy = tableCopy.replace(char,'')
				
			tableCopy = tableCopy.split('\n\n')

			for i in range(0,len(tableCopy)):
				tableCopy[i] = tableCopy[i].replace('|','')
				tableCopy[i] = ','.join(tableCopy[i].split())

			res = '\n'.join(tableCopy)
			test = StringIO(res)
			df = pd.read_csv(test,sep=',')

			return df



if __name__ == '__main__':
	t = titaniumLite()
	t.execute('use database db1;')
	print(t.execute('select * from stats;'))
	# t.execute('use database db1;')
	del t
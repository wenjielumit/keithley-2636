#!/usr/bin/env python3
#coding:utf-8

"""
  Author:  Ross
  Purpose: 'Simple' driver for Keithley 2636
  Created: 07/03/17
"""

import visa
import sys

########################################################################
class K2636():
	"""Class for Keithley control"""

	#----------------------------------------------------------------------
	def __init__(self, rm, address, read_term, baudrate):
		"""Constructor - makes connection to instrument on instance"""
		self.make_connection(rm, address, read_term, baudrate)
	
	#----------------------------------------------------------------------
	def make_connection (self, rm, address, read_term, baudrate):
		"""Make initial connection to instrument"""
		
		if 'ttyS' or 'ttyUSB' in str(address) :
			# Connection via SERIAL
			print ('Connecting to Keithley via %s' %address)
			self.inst = rm.open_resource(address)
			self.inst.read_termination = str(read_term)
			self.inst.baud_rate = baudrate
			#print (self.inst.query('*IDN?')) # Doesnt work for 2636
			
		if 'GPIB' in str(address):
			# Connection via GPIB
			print ('This is too hard in linux...')
			sys.exit()
			
	#----------------------------------------------------------------------		
	def write(self, m):
		'''Wrapper for the PyVisa write function'''
		assert type(m) == str
		self.inst.write(m)
		
	#----------------------------------------------------------------------		
	def loadTSP(self, tsp):
		'''Load an anonymous TSP script into the K2636 nonvolatile memory'''
		self.write('loadscript')
		print ('\n---------LOADING TSP-----------')
		for line in open(tsp, mode='r'):
			self.write(line)
			print('%s' %line)
		print ('----------SENT TO K2636-----------\n')
		self.write('endscript')
				
	#----------------------------------------------------------------------		
	def runTSP(self):
		'''Run the anonymous TSP script currently loaded in the K2636 memory'''	
		self.write('script.anonymous.run()')
		
########################################################################
def uploadTSP():
	'''Connects to keithley, uploads TSP instructions and tells keithley to execute'''
	print ('BEGIN')
	#------------------------------------------------------------
	
	rm = visa.ResourceManager('@py') #use py-visa backend
	keithley = K2636(rm, address='ASRL/dev/ttyUSB0', read_term='\r', baudrate=57600)
	keithley.write('*RST')
	
	print ('Uploading TSP script: ', sys.argv[1])
	keithley.loadTSP(sys.argv[1])
	keithley.runTSP()
	
	rm.close()
	
	#------------------------------------------------------------
	print ('END')

if __name__ == '__main__':
	uploadTSP()
	
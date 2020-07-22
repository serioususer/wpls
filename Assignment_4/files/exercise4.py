#!/usr/bin/env python2
# -*- coding: UTF-8 -*-

##############################################
##############################################
##   PhySec-Praktikum Framework 2019        ##
##   Authors: Jeremy Brauer                 ##
##                                          ##
##   Students:   <fill in your names>       ##
##               <fill in Matrikel-Nr>      ##
##               <fill in your names>       ##
##   Student-ID: <fill in Matrikel-Nr>      ##
##                                          ##
##   DO ONLY CHANGE MARKED FUNCTION BODIES  ##
##                                          ##
##############################################
##############################################


import utils
import numpy
from subprocess import check_output

"""
Excersise Bit Error Rate:
Implement the Bit Error Rate computation.
Do NOT use any given function for but implement them by yourself.

X, Y are given as lists.

Blockwise application is done outside so please use the whole vectors at once.
"""


def ber(X, Y):
	hw = 0.0
	for x,y in len(X):
		hw += x^y
	
	BER = hw/len(X)
	
	if 0 <= BER <= 0.5:
		return BER
	else:
		return 1 - BER


"""
Function call for entropy estimation.
Do not change this code
"""


def MI(A, B):
	if len(A) != len(B):
		raise ValueError("A and B must have the same length")
	with open("MI_temp.dat", "w+") as tmp:
		for (a, b) in zip(A, B):
			tmp.write("%f %f\n" % (a, b))
	return float(check_output(["./MIhigherdim", "MI_temp.dat", "2", "1", "1", "%d" % len(A), "8"]))


"""
Example mean-quantizer.
"""
def quant0(A, B, E, args):  # A, B, E are lists. Args is not used here but might be necessary when it comes to Q1 and Q2.
	Q = lambda x, t: 1 if x > t else 0  # Q maps to 1 if x>t. Otherwise Q maps to 0.
	bA = map(Q, A, [numpy.mean(A) for i in range(len(A))])  # bA[i]=Q(A[i], mean(A))
	bB = map(Q, B, [numpy.mean(B) for i in range(len(B))])
	bE = map(Q, E, [numpy.mean(E) for i in range(len(E))])
	return bA, bB, bE


"""
Implement the quantization scheme found in "Jana, Suman - 2009 - On the effectiveness of secret key extraction from wireless signal strength in real environments". 
You are provided with measurements for Node A, B and E.
Please return a binary list in bA, bB, bE as tuple.

Blockwise application is done outside so please use the whole datasets.
"""
def quant1(A, B, E, args):
	bA = []
	bB = []
	bE = []

	# Number of bits per symbol (parameter)
	number_of_bits = args.bits;
	# After you have finished, bA, bB and bE should be of same length and should be of the form [1, 0, 0, 1, 1, 1 ...]

	### YOUR CODE GOES HERE ###
	def JanaMultibit(X):
		#(i)determine the Range of RSS measurements from the minimum and the maximum measured RSS values
		x_min = min(X)
		x_max = max(X)

		#(ii) find N, the number of bits that can be extracted per measurement
		# N is already implemented
		N = number_of_bits

		#(iii) divide the Range into m = 2^n equal sized intervals
		M = 2**N	# M intervals, len(Range) = M+1
		interval = abs((max(X)-min(X))/float(M)) # interval size
		
		Range =[] 	# intervals
		
		if interval == 0:	#min=max
			interval = 1

		while x_min <= x_max:	# fill in
			Range.append(x_min) 
			x_min += interval

		#(iv) choose an N bit assignment for each of the M intervals (for example use the Gray code sequence) 
		bit_assignment = utils.gray_code(N)

		#(v) for each RSS measurement, extract N bits depending on the interval in which the RSS measurement lies. 
		quantized=[]
		for x in X:
			for j in xrange(len(Range) - 1):
				if Range[j] <= x <= Range[j+1]: # including max and min values
					quantized.extend(bit_assignment[j])
					break
			if len(Range) == 1:	# min=max → only one value
				quantized.extend(bit_assignment[0])
		return quantized
	
	bA = JanaMultibit(A)
	bB = JanaMultibit(B)
	bE = JanaMultibit(E)
	
	return (bA, bB, bE)
	# return (bA, bB, bE) #After implementation, return binary vectors as tuple


def quant2(A, B, E, args):
	bA = []
	bB = []
	bE = []

	## Better do not change the parameter validation
	alpha = args.alpha
	m = args.m
	if m % 2 == 0:  # check whether m is odd and change it if necessary
		m = m - 1
	"""
	Wenn Wert größer q_plus = 1
	Wenn Wert kleiner q_minus = 0					
	q_plus >= Wert >= q_minius --> -1
	"-1" für Alice und Bob unbrauchbar
	"""

	### YOUR CODE GOES HERE ###

	return not_yet_implemented("quant2")

	# return bA, bB, bE  # After implementation, return binary vectors as tuple


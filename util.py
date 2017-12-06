#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	@ author Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Very big prime for El Gamal use of 128-bit length, close to the digest's.
'''

import hashlib
import sys
import os
import shutil
import sys
import itertools

# CONSTANT, COPIED DIRECTLY FROM
# https://langui.sh/2009/03/07/generating-very-large-primes/
BIG_ASS_PRIME = 7337488745629403488410174275830423641502142554560856136484326749638755396267050319392266204256751706077766067020335998122952792559058552724477442839630133

def update_progress(name, progress):
	'''
	Update the progress bar, only for GUI purposes.
	Modified from StackOverflow: https://stackoverflow.com/a/15860757

	Takes in a string for process name and a float for progress.
	'''
	# get the terminal size (mostly width)
	termsize = shutil.get_terminal_size()
	# length of progress bar
	bar_length = termsize[0] - len(name) - 9
	# if done set progress to 1 (max value)
	if progress >= 1:
		progress = 1
	# length of the done block
	block = int(round(bar_length * progress))
	# the text to print out
	text = "\r{0:s}: [{1:s}] {2:3.0f}%".format \
		(name, "#" * block + "-" * (bar_length - block), progress * 100)
	# we have to use stdout because the caret will not return with print
	sys.stdout.write(text)
	sys.stdout.flush()

def get_digest(filenames):
	'''
	Get the hash of the files given as parameter.
	Returns a dictionary: {(fullpath, digest)}
	'''
	hashes = dict()
	for i in range(len(filenames)):
		update_progress('Hashing', (i+1) / len(filenames))
		# get the file in binary
		try:
			f = open(filenames[i], 'rb')
		except FileNotFoundError:
			print('Error! file not found: "' + filenames[i] + '". Quitting...')
			raise SystemExit
		# get the hash object
		m = hashlib.sha3_512()
		# actually hash the file content
		m.update(f.read())
		# and add the hash to a dictionary with the key being filename
		hashes[os.path.abspath(filenames[i])] = int(m.hexdigest(), 16) % BIG_ASS_PRIME
	if is_not_good(hashes):
		print('Fatal error! Hash/mod collision and/or hash returns 0. Quitting...')
	return hashes

def get_coeffs(roots):
	'''
	Get the coeeficients of the polynomial given the roots.
	'''
	counter = 0
	ret = [0]
	# a t-order polynomials has t+1 coefficients
	for i in range(len(roots)):
		ret.append(0)
	# get the i-th coeff
	for k in range(len(ret)):
		# get all subsets
		for roots_k in itertools.combinations(roots, k):
			prod_k = 1
			for elem in roots_k:
				prod_k *= elem
				prod_k %= BIG_ASS_PRIME
			prod_k *= (-1) ** len(roots_k)
			counter += 1
			update_progress('Getting coeffs', counter / 2 ** (len(ret)-1))
			ret[k] += prod_k
			ret[k] %= BIG_ASS_PRIME
	return ret

def poly_eval(coeffs, x):
	'''
	Apply Horner's rule for fast polynomial evaluation.
	'''
	ret = 0
	for i in coeffs:
		ret *= x
		ret %= BIG_ASS_PRIME
		ret += i
		ret %= BIG_ASS_PRIME
	return ret

def is_not_good(dictionary):
	'''
	Check if the values in the dictionary has duplicates.
	'''
	to_check = list(dictionary.values())
	ret = False
	while len(to_check) > 0:
		t = to_check.pop()
		if t in to_check:
			ret = True
		if t == 0:
			ret = True
	return ret


#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Encrypted using an imported PHE (Partially Homomorphic Encryption) module.
'''
import hashlib
import sys
import os
import shutil
import sys
import itertools
from phe import paillier

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
		hashes[os.path.abspath(filenames[i])] = int(m.hexdigest(), 16)
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
			prod_k *= (-1) ** len(roots_k)
			counter += 1
			update_progress('Getting coeffs', counter / 2 ** (len(ret)-1))
			ret[k] += prod_k
	return ret

def poly_eval_paillier(pubkey, coeffs, x):
	'''
	Apply Horner's rule for fast polynomial evaluation.
	'''
	ret = pubkey.encrypt(0)
	for i in coeffs:
		ret = ret * x
		ret = ret + i
	return ret

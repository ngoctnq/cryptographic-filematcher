#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Encrypted using an imported PHE (Partially Homomorphic Encryption) module.
'''
from util import *
from phe import paillier
import sys, secrets, pickle

if len(sys.argv) == 1:
	print('Usage:', sys.argv[0], '[filename_1] [filename_2] ... [filename_n]')
else:
	print('cryptographic filematcher (ngoc@underlandian.com)')
	print('This will ask you for the file from the other party, and a file to send back.')
	# get the coefficients
	fn = input('\nCoefficient file from the other party (default: ./COEFF): ')
	if fn == '':
		fn = 'COEFF'
	f = open(fn, 'rb')
	# verification
	pubkey, coeff = pickle.load(f)
	hashes = get_digest(sys.argv[1:])
	# get the edited digest to send back
	fn = input('\nEncrypted digest file to be sent back save location (default: ./DIGEST): ')
	if fn == '':
		fn = 'DIGEST'
	f = open(fn, 'wb+')
	digest = []
	for key in hashes:
		val = hashes[key]
		result = poly_eval_paillier(pubkey, coeff, val)
		result = result * (secrets.randbits(512) + 1)
		result = result + val
		digest.append(result)
	pickle.dump(digest, f)
	f.close()
	print('File written. Share this file with the other party.')

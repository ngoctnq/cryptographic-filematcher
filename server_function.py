#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Encrypted using an imported PHE (Partially Homomorphic Encryption) module.
'''
from util import *
from phe import paillier
import sys, pickle

if len(sys.argv) == 1:
	print('Usage:', sys.argv[0], '[filename_1] [filename_2] ... [filename_n]')
else:
	print('cryptographic filematcher (ngoc@underlandian.com)')
	print('This will save 2 files. One needs to be kept secret, one to be shared.')
	# print the key out
	pubkey, privkey = paillier.generate_paillier_keypair()
	# print the filenames out
	fn = input('\nKEEP SECRET: Private key save location (default: ./KEY): ')
	if fn == '':
		fn = 'KEY'
	f = open(fn, 'wb+')
	hashes = get_digest(sys.argv[1:])
	pickle.dump((privkey, hashes), f)
	f.close()
	print('\nFile written. DO NOT SHARE THIS!')

	# print the coeffs out
	fn = input('\nPublic file to be shared save location (default: ./COEFF): ')
	if fn == '':
		fn = 'COEFF'
	f = open(fn, 'wb+')
	coeff = [pubkey.encrypt(x) for x in get_coeffs(list(hashes.values()))]
	pickle.dump((pubkey, coeff), f)
	f.close()
	print('\nFile written. Share this file with the other party.')
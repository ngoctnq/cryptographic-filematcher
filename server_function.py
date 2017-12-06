#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	@ author Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Very big prime for El Gamal use of 128-bit length, close to the digest's.
'''

from util import *
import sys, pickle, secrets

if len(sys.argv) == 1:
	print('Usage:', sys.argv[0], '[filename_1] [filename_2] ... [filename_n]')
else:
	print('cryptographic filematcher (ngoc@underlandian.com)')
	print('This will save 2 files. One needs to be kept secret, one to be shared.')
	# print the filenames out
	fn = input('\nKEEP SECRET: Hash file save location (default: ./FILES): ')
	if fn == '':
		fn = 'FILES'
	f = open(fn, 'wb+')
	hashes = get_digest(sys.argv[1:])
	pickle.dump(hashes, f)
	f.close()
	print('\nFile written. DO NOT SHARE THIS!')
	# print the key out
	key = secrets.randbelow(BIG_ASS_PRIME - 1) + 1
	# key 2, for no reason
	key2 = secrets.randbelow(BIG_ASS_PRIME - 1) + 1
	'''
	fn = input('\nKEEP SECRET: Encrypt key save location (default: ./KEY): ')
	if fn == '':
		fn = 'KEY'
	f = open(fn, 'wb+')
	pickle.dump(key, f)
	f.close()
	print('File written. DO NOT SHARE THIS!')
	'''
	# print the coeffs out
	fn = input('\nCoefficient file to be shared save location (default: ./COEFF): ')
	if fn == '':
		fn = 'COEFF'
	f = open(fn, 'w+')
	# write out the public key
	f.write(hex(key2)[2:])
	f.write('\n')
	coeff = get_coeffs(list(hashes.values()))
	for val in coeff:
		val *= key
		val %= BIG_ASS_PRIME
		f.write(hex(val)[2:])
		f.write('\n')
	f.close()
	print('\nFile written. Share this file with the other party.')
#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	@ author Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Very big prime for El Gamal use of 128-bit length, close to the digest's.
'''
from util import *
import sys, secrets

if len(sys.argv) == 1:
	print('Usage:', sys.argv[0], '[filename_1] [filename_2] ... [filename_n]')
else:
	print('cryptographic filematcher (ngoc@underlandian.com)')
	print('This will ask you for the file from the other party, and a file to send back.')
	# get the coefficients
	fn = input('\nCoefficient file from the other party (default: ./COEFF): ')
	if fn == '':
		fn = 'COEFF'
	f = open(fn)
	coeff = []
	for line in f:
		coeff.append(int(line.strip(), 16))
	hashes = get_digest(sys.argv[1:])
	# get the edited digest to send back
	fn = input('\nEncrypted digest file to be sent back save location (default: ./DIGEST): ')
	if fn == '':
		fn = 'DIGEST'
	f = open(fn, 'w+')
	key2 = coeff.pop(0)
	for key in hashes:
		val = hashes[key]
		# re-encrypt
		val2 = val * key2
		val2 %= BIG_ASS_PRIME
		result = poly_eval(coeff, hashes[key])
		if result == 0:
			print('File', key, 'matched!')
		r = secrets.randbelow(BIG_ASS_PRIME - 1) + 1
		r *= result
		r %= BIG_ASS_PRIME
		r += val
		r %= BIG_ASS_PRIME
		f.write(hex(r)[2:])
		f.write('\n')
	f.close()

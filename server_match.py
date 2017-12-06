#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Encrypted using an imported PHE (Partially Homomorphic Encryption) module.
'''
from phe import paillier
import pickle, secrets

print('cryptographic filematcher (ngoc@underlandian.com)')
print('This will ask you for the hash file saved before,')
print('\tand the digest file from the other party.')
# get the coefficients
fn = input('\nPrivate key file saved before (default: ./KEY): ')
if fn == '':
	fn = 'KEY'
privkey, hashes = pickle.load(open(fn, 'rb'))
# get the coefficients
fn = input('Digest file from the other party (default: ./DIGEST): ')
if fn == '':
	fn = 'DIGEST'
digest = pickle.load(open(fn, 'rb'))
digest = [privkey.decrypt(x) for x in digest]

# compare the digests
matched = False
for hash1 in digest:
	for key in hashes:
		if secrets.compare_digest(hex(hash1), hex(hashes[key])):
			print('File', key, 'matched!')
			matched = True
if not matched:
	print('Nothing matched.')
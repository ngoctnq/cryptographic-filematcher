#!/usr/bin/env python3
'''
	Cryptographic Filematcher
	@ author Ngoc Tran (ngoc@underlandian.com)

	Hash the files with SHA3-512 for maximum security and fixed-size digest.
	Very big prime for El Gamal use of 128-bit length, close to the digest's.
'''

import pickle, secrets

print('cryptographic filematcher (ngoc@underlandian.com)')
print('This will ask you for the hash file saved before,')
print('\tand the digest file from the other party.')
# get the coefficients
fn = input('\nHash file saved before (default: ./FILES): ')
if fn == '':
	fn = 'FILES'
f = open(fn, 'rb')
hashes = pickle.load(f)
# get the coefficients
fn = input('Digest file from the other party (default: ./DIGEST): ')
if fn == '':
	fn = 'DIGEST'
f = open(fn)
digest = []
for line in f:
	digest.append(int(line.strip(), 16))
# compare the digests
for hash1 in digest:
	for key in hashes:
		if secrets.compare_digest(hex(hash1), hex(hashes[key])):
			print('File', key, 'matched!')
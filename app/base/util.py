# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
 
import hashlib, binascii, os
import random
import string

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/

def hash_pass( password ):
	"""Hash a password for storing."""
	salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
	pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
		                salt, 100000)
	pwdhash = binascii.hexlify(pwdhash)
	return (salt + pwdhash) # return bytes

def verify_pass(provided_password, stored_password):
	"""Verify a stored password against one provided by user"""
	stored_password = stored_password.decode('ascii')
	salt = stored_password[:64]
	stored_password = stored_password[64:]
	pwdhash = hashlib.pbkdf2_hmac('sha512', 
		                  provided_password.encode('utf-8'), 
		                  salt.encode('ascii'), 
		                  100000)
	pwdhash = binascii.hexlify(pwdhash).decode('ascii')
	return pwdhash == stored_password


def generate_rand_passwd(length=12):
	# Define the character sets for password generation
	uppercase_letters = string.ascii_uppercase
	lowercase_letters = string.ascii_lowercase
	digits = string.digits
	special_characters = string.punctuation

	# Combine all character sets
	all_characters = uppercase_letters + lowercase_letters + digits + special_characters

	# Generate random password
	password = ''.join(random.choice(all_characters) for _ in range(length))

	return password


	
	
	
	
	
	
	
	

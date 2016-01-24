from random import choice, random, randint
from string import ascii_lowercase

def randCSV(numPeople, hasID, hasGrade, hasEmail, hasDOB, hasAddress, hasPhone, deleteEntries, probDeletion):
	f = open('./static/random/firstNames.txt', 'r')
	firstNames = f.read().splitlines()
	f.close()
	f = open('./static/random/lastNames.txt', 'r')
	lastNames = f.read().splitlines()
	f.close()
	f = open('./static/random/streetSuffixes.txt', 'r')
	streetSuffixes = f.read().splitlines()
	f.close()
	f = open('./static/random/cities.txt', 'r')
	cities = f.read().splitlines()
	f.close()
	f = open('./static/random/states.txt', 'r')
	states = f.read().splitlines()
	f.close()
	domains = ['aol.com', 'gmail.com', 'hotmail.com', 'mail.com' , 'mail.kz', 'yahoo.com']
	s = ''
	if hasID:
		s += 'id, '
	s += 'name, '
	if hasGrade:
		s += 'grade, '
	if hasEmail:
		s += 'email, '
	if hasDOB:
		s += 'dob, '
	if hasAddress:
		s += 'address, '
	if hasPhone:
		s += 'phone, '
	s = s[:-2]
	s += '\n'
	for i in range(numPeople):
		if hasID:
			s += str(i) + ', '
		s += choice(firstNames) + ' ' + choice(lastNames) + ', '
		if hasGrade:
			if not deleteEntries or random() > probDeletion:
				s += str(randint(9, 12))
			s += ', '
		if hasEmail:
			if not deleteEntries or random() > probDeletion:
				# random string of 7 to 10 lowercase letters, followed by email domain
				s += \
					''.join(choice(ascii_lowercase) for i in range(randint(7, 14))) + \
					'@' + choice(domains)
			s += ', '
		if hasDOB:
			if not deleteEntries or random() > probDeletion:
				s += str(randint(1, 12)) + '/' + str(randint(1, 28)) + '/' + \
					str(randint(1998, 2001))
			s += ', '
		if hasAddress:
			if not deleteEntries or random() > probDeletion:
				# street address, city, state, zip
				s += str(randint(1, 9999)) + ' ' + choice(lastNames) + ' ' + choice(streetSuffixes) + ' ' + \
					choice(cities) + ' ' + choice(states) + ' ' + str(randint(3000, 99999))
			s += ', '
		if hasPhone:
			if not deleteEntries or random() > probDeletion:
				# random phone number such that area code doesn't start with a zero,
				# none of the middle three digits are a 9, middle three digits aren't 000,
				# and last 4 digits aren't all be the same
				n = '0000000000'
				while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
					n = str(randint(10**9, 10**10-1))
				s += n[:3] + '-' + n[3:6] + '-' + n[6:]
			s += ', '
		s = s[:-2]
		s += '\n'
	return s[:-1]

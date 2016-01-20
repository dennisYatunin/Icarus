from random import choice, random, randint

def csv(numPeople, hasID, hasEmail, hasDOB, hasAddress, hasPhone, missingData, probDeletion):
	f = open('/static/firstNames.txt', 'r')
	firstNames = f.readlines()
	f.close()
	f = open('/static/lastNames.txt', 'r')
	lastNames = f.readlines()
	f.close()
	f = open('/static/streetSuffixes.txt', 'r')
	streetSuffixes = f.readlines()
	f.close()
	f = open('/static/cities.txt', 'r')
	cities = f.readlines()
	f.close()
	f = open('/static/states.txt', 'r')
	states = f.readlines()
	f.close()
	domains = ['aol.com', 'gmail.com', 'hotmail.com', 'mail.com' , 'mail.kz', 'yahoo.com']
	data = [None] * numPeople

	for i in range(numPeople):
		if hasID:
			data[i] = str(i) + ', '
		data[i] += choice(firstNames) + ' ' + choice(lastNames) + ', '
		if hasEmail:
			if not missingData or random() < probDeletion:
				# random string of 7 to 10 lowercase letters, followed by email domain
				data[i] +=
				''.join(choice(string.ascii_lowercase) for i in range(randint(7, 14))) +
				'@' + choice(domains)
			data[i] += ', '
		if hasDOB:
			if not missingData or random() < probDeletion:
				data[i] += str(randint(1, 12)) + '/' + str(randint(1, 28)) + '/' +
				str(randint(1995, 2010))
			data[i] += ', '
		if hasAddress:
			if not missingData or random() < probDeletion:
				# street address, city, state, zip
				data[i] += str(randint(1, 9999)) + choice(lastNames) + choice(streetSuffixes) + ' ' +
				choice(cities) + ' ' + choice(states) + ' ' + str(randint(3000, 99999)) + ', '
			else:
				data[i] += ', '
		if hasPhone:
			if not missingData or random() < probDeletion:
				# random phone number such that area code doesn't start with a zero,
				# none of the middle three digits are a 9, middle three digits aren't 000,
				# and last 4 digits aren't all be the same
				n = '0000000000'
				while '9' in n[3:6] or n[3:6]=='000' or n[6]==n[7]==n[8]==n[9]:
					n = str(randint(10**9, 10**10-1))
				data[i] += n[:3] + '-' + n[3:6] + '-' + n[6:]
			data[i] += ', '
		data[i] = data[i][:-2]
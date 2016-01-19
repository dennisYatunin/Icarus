from random import choice, random, randint

def csv(numPeople, hasID, hasEmail, hasDOB, hasAddress, hasPhone, missingData):
	f = open('/static/firstNames.txt', 'r')
	firstNames = f.readlines()
	f.close()
	f = open('/static/lastNames.txt', 'r')
	lastNames = f.readlines()
	f.close()
	f = open('/static/streetSuffixes.txt', 'r')
	streetSuffixes = f.readlines()
	f.close()
	domains = ['aol.com', 'gmail.com', 'hotmail.com', 'mail.com' , 'mail.kz', 'yahoo.com']

	data = [None] * numPeople
	probability = 1.0 - missingData / 100.0

	for i in range(numPeople):
		if hasID:
			data[i] = str(i) + ', '
		data[i] += choice(firstNames) + ' ' + choice(lastNames) + ', '
		if hasEmail:
			if probability == 1 or random() < probability:
				data[i] +=
				''.join(choice(string.ascii_lowercase) for i in range(randint(7, 14))) +
				'@' + choice(domains)
			data[i] += ', '
		if hasDOB:
			if probability == 1 or random() < probability:
				data[i] += str(randint(1, 12)) + '/' + str(randint(1, 28)) + '/' +
				str(randint(1995, 2010))
			data[i] += ', '
		if hasAddress:
			if probability == 1 or random() < probability:
				data[i] += str(randint(1, 9999)) + choice(lastNames) + choice(streetSuffixes)
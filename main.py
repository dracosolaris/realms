import random

VOWELS = ["A","E","I","O","U","AA","EE","II","OO","UU"]
CONSTS = ["B","C","D","F","G","H","J","K","L","M","N","P","Q","R","S","T","V","W","X","Y","CH","SH","SCH","TS"]

random.seed(2)

def chance(prob=50):
	return random.randint(1,100) < prob

def low_chance(prob=50):
	return random.triangular(1, 100, 1) < prob

class Language():
	vowels = []
	consts = []
	syllables = []

	# TODO: use a zipf frequency of letter distribution

	def __init__(self):
		n_vowels = random.randrange(3, len(VOWELS)+1)
		n_consts = random.randrange(6, len(CONSTS)+1)

		self.vowels = random.sample(VOWELS, k=n_vowels)
		self.consts = random.sample(CONSTS, k=n_consts)

		for v in self.vowels:
			if chance(75):
				self.syllables.append(v)

		for c in self.consts:
			for v in self.vowels:
				if chance(75):
					self.syllables.append(c + v)
					for cc in self.consts:
						if chance(50):
							self.syllables.append(c + v + cc)
		random.shuffle(self.syllables)

	def word(self, syllable_length=None):
		if syllable_length is None:
			length = int(random.triangular(1,4,1))
		else:
			length = syllable_length
		w = []

		while len(w) < length:
			w.append(random.choice(self.syllables))

		return ''.join(w).lower()

lang = Language()


class Person():
	mother = None
	father = None

	def __init__(self, **kwargs):
		self.name = lang.word(2).title()
		self.age = kwargs.get('age', random.randint(1, 80))


community = []


for _ in range(10):
	person = Person()

	community.append(person)

	if person.age < 50:
		father_age = person.age + random.randint(16, 30)
		father = Person(age=father_age)
		mother_age = father_age + random.randint(-10, 3)
		mother = Person(age=mother_age)

		person.mother = mother
		person.father = father

		community.append(father)
		community.append(mother)

for p in community:
	print(p.name)
	print(p.age)
	print('')

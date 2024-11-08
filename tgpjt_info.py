possible_first_names = ["Eleanor", "Chidi", "Tahani", "Jason", "Michael", "Janet",
						"Mohammed", "Yusuf", "Pranav", "Ji-ho", "Hyun-woo", "Seo-yeon",
						"Ji-yoo", "Fatima", "Priya", "Jack", "John", "Grace", "Emily",
						"William", "Alice", "Wei", "Min", "Jia", "Xi", "Olivia", "Emma",
						"Liam", "Noah", "Hiroto", "Ren", "Yuma", "Hina", "Yui",
						"Mateo", "Valentina", "Aarav", "Saanvi", "Miguel", "Juan", "Ava",
						"Mary", "Maria", "Sofia", "Alexander", "Mikhail", "Omar",
						"Imene", "Sara", "Yasmine", "Ahmed", "Ali", "Peter", "Pierre",
						"Karim", "Lydia", "Fatma", "Miriam", "Marina", "Irene", "Amira", 
						"Nicolas", "Lucas", "Francisco", "Theo", "Ted", "Nathan", "Arthur",
						"Jack", "Thomas", "Malik", "Aiden", "Louis", "Edward", "Martha",
						"Elizabeth", "Sophia", "Laura", "Mia", "Islande", "Esther",
						"Jessica", "Mabel", "Ramona", "Amelia", "Linda", "Barbara",
						"Camila", "Mingze", "Muchen", "David", "Nagisa", "Krishna",
						"Seo-jun", "Mehmet", "Mustafa", "Maryam", "Lucy", "Aditi", 
						"Mila", "Rin", "Himari", "Hinata", "Adam", "Eve"
						]


possible_last_names = ["Shellstrop", "Anagonye", "Al-Jamil", "Mendoza",
					   "Grigoryan", "Akter", "Khat", "Kim", "Chan", "Cheng",
					   "Wang", "Li", "Zheng", "Devi", "Kumar", "Singh", 
					   "Cohen", "Levi", "Sato", "Suzuki", "Takahashi", "Tanaka", 
					   "Omarov", "Ivanov", "Lee", "Park", "de la Cruz", "Garcia",
					   "Ramos", "Gonzalez", "Smirnov", "Smirnova", "Ivanova",
					   "Pavlov", "Pavlova", "de Silva", "Yilmaz", "Kaya",
					   "Demir", "Nguyen", "Hoxha", "Luka", "Gruber", "Steiner",
					   "Berger", "Haas", "Novik", "Peters", "Peeters", "Janssens",
					   "Delic", "Subotic", "Dmitrov", "Dmitrova", "Horvat", 
					   "Novotny", "Nielsen", "Olsen", "Johansson", "Martin",
					   "Bernard", "Dubois", "Laurent", "Muller", "Miller",
					   "Schmidt", "Schneider", "Papoutsis", "Samaras", "Andersen",
					   "Murphy", "Kelly", "Rossi", "Esposito", "Rizzo",
					   "Omarov", "Weber", "Borg", "Ursu", "De Jong", 
					   "Smith", "Brown", "Hernandez", "Rodriguez", "Johnson",
					   "Williams", "Jones", "Taylor", "Young" 
					   ]


possible_personality_traits = ["kind", "unkind", "unstable", "stable"]
# kind: average +10
# unkind: average -10
# unstable: stdev +5
# stable: stdev -5

personality_traits_avg_dict = {"kind": 10, "unkind": -10, "stable": 0, "unstable": 0}
personality_traits_stdev_dict = {"kind": 0, "unkind": 0, "stable": -5, "unstable": 5}
#todo - use this in generate_world




"""
extra and further improvements


add more stuff to the people - gender, birthplace, death place, etc

easter eggs
if born in Florida, high chance for unstable or unkind
if born in Arizona, high chance for unkind






"""

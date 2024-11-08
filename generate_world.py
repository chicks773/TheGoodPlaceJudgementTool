import tgpjt_info

import pandas as pd

import datetime as dt

import random


average_points_per_action = 0
stdev_points_per_action = 15

average_number_of_actions = 70
stdev_number_of_actions = 20


#get timestamp of current time, return as format 2024-12-31_12-59-59
def get_timestamp():
    date_processed = dt.date.today()
    time_processed = dt.datetime.now()
    timestamp = str(date_processed) + "_" + str(time_processed.hour) + "-" + \
                str(time_processed.minute) + "-" + str(time_processed.second)
    return timestamp


def generate_name():
	#generate a random firstname and lastname (i.e. "Eleanor Shellstrop")
	#from the list of possible names in tgpjt_info
	#returns name (str)
	firstName = random.choice(tgpjt_info.possible_first_names)
	lastName = random.choice(tgpjt_info.possible_last_names)
	name = (firstName + " " + lastName)
	return name

def remove_conflicting_personality_traits(personality):
	#take list of personality traits as an argument, i.e., ["kind", "unstable", "stable"]
	#return list of personality traits with any conflicting traits removed
	#mutually exclusive pairs: (kind, unkind), (stable, unstable)

	#if conflicting personality traits, 50/50 random choice of which to keep

	#kind and unkind
	if ("kind" in personality) and ("unkind" in personality):
		r = random.randint(1, 10)
		if r <= 5:
			#keep unkind
			personality.remove("kind")
		else:
			#keep kind
			personality.remove("unkind")

	#stable and unstable
	if ("stable" in personality) and ("unstable" in personality):
		r = random.randint(1, 10)
		if r <= 5:
			#keep unstable
			personality.remove("stable")
		else:
			#keep stable
			personality.remove("unstable")

	return personality

def generate_personality():
	#choose 0, 1, or 2 random personality traits from the list
	#of possible personality traits in tgpjt_info
	#return list of personality traits (strings)

	n = random.randint(0, 2)

	#create sample (without replacement) of size n from possible personality traits
	personality = random.sample(tgpjt_info.possible_personality_traits, n)

	#run function to remove conflicting personality traits
	personality = remove_conflicting_personality_traits(personality)

	return personality



def generate_points_for_single_action(average_points, stdev_points):
	#given an average and standard deviation, generate a single value
	#from the normal distribution
	points = round(random.gauss(average_points, stdev_points), 1)
	return points




def apply_personality(average_points, stdev_points, personality):
	#given an average, standard deviation, and list of personality traits,
	#calculate and return a new average and standard deviation

	#kind: average + 10
	if "kind" in personality:
		average_points = average_points + 10

	#unkind: average - 10
	if "unkind" in personality:
		average_points = average_points - 10

	#stable: stdev - 5
	if "stable" in personality:
		stdev_points = stdev_points - 5

	#unstable: stdev + 5
	if "unstable" in personality:
		stdev_points = stdev_points + 5

	return (average_points, stdev_points)

def generate_points_list(personality_traits=[]):
	#given a list of personality traits (assume no personality as default if nothing given)
	#generate a list of point values representing their entire life

	average_points, stdev_points = apply_personality(average_points_per_action, stdev_points_per_action, personality_traits)

	#num actions is normally distributed with average=70, stdev=20
	#i.e., a person performs approximately 1 action per year of life
	#a list of length 70 lived 70 years before dying
	num_actions = int(round(random.gauss(average_number_of_actions, stdev_number_of_actions), 0))

	points_list = []
	for _ in range(num_actions):
		points = generate_points_for_single_action(average_points, stdev_points)
		points_list.append(points)

	return points_list

def apply_name_ee_to_personality(name, personality):
	#apply name-based Easter Eggs
	#if one of the special names comes up, ensure their personality
	#contains a certain trait, and no conflicting traits
	if name == "Eleanor Shellstrop":
		if "kind" in personality:
			personality.remove("kind")
		if "unkind" not in personality:
			personality.append("unkind")
	elif name == "Chidi Anagonye":
		if "unkind" in personality:
			personality.remove("unkind")
		if "kind" not in personality:
			personality.append("kind")
	elif name == "Jason Mendoza":
		if "stable" in personality:
			personality.remove("stable")
		if "unstable" not in personality:
			personality.append("unstable")
	elif name == "Tahani Al-Jamil":
		if "unstable" in personality:
			personality.remove("unstable")
		if "stable" not in personality:
			personality.append("stable")

	return personality

def generate_person():
	#generate a "person", represented as a single row pd.DataFrame
	#person has a name, personality, and points list

	name = generate_name()

	personality = generate_personality()
	personality = apply_name_ee_to_personality(name, personality)

	points_list = generate_points_list(personality_traits=personality)

	person = pd.DataFrame(columns=["name", "personality", "points list"], data=[[name, personality, points_list]])
	return person


def __main__():
	#ask user for n, and only accept if n is an integer > 0
	n = ''
	while (n == ''):
		print("Please enter the number of people to generate")
		n = input()
		try:
			n = int(n)
			assert(n > 0)
		except:
			print("please enter a valid n, must be an integer > 0")
			n = ''


	df = pd.DataFrame(columns=["name", "personality", "points list"])

	for _ in range(n):
		person = generate_person()
		df = pd.concat([df, person])

	output_filename = "TGPJT_" + str(n) + "_" + get_timestamp() + ".csv"
	df.to_csv(output_filename, index=False)

	print("file saved as {}".format(output_filename))

	return


if __name__ == "__main__":
	__main__()


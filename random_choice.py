# This script made by mathieu.pont@outlook.com allows you to made choice according a list of
# priority over differents users, it uses random to made choice when there is a conflict

import numpy as np
import sys
import random

# --- Parameters ---
#  The priority parameter below allows to give priority depending on the position of the choice
priority = True
number_per_choice = 2 # number of users per choice


# --- Import data ---
data = np.genfromtxt(sys.argv[1], delimiter=',', dtype=None, encoding="utf8")
print("data:")
print(data)


# --- Algo ---
num_users = data.shape[1]

best_ind = np.ones(num_users, dtype=int)
best_nsc = sys.maxsize
# We solve many times the problem due to randomness 
for epoch in range(0, 10000):
	ind = np.ones(num_users, dtype=int)
	conflict = True
	while conflict:
		conflict = False
		dist_choice_user = {}
		found = {}
		rand = random.sample(range(num_users*2), num_users)
		for i in range(0, num_users):
			# Get choice of user i
			if ind[i] < data.shape[0]:
				user_choice = data[ind[i],i]
			else:
				print("Can't satisfy the problem (restart or add choices for each users)")
				break
		
			# Choice already found		
			if user_choice in dist_choice_user:
		
				# Choice found less than the maximum
				if found[user_choice] < number_per_choice:
					# Manage priority
					if (priority and ind[i] > ind[dist_choice_user[user_choice]]) or rand[i] < rand[dist_choice_user[user_choice]]:
						dist_choice_user[user_choice] = i
					found[user_choice] += 1

				# Conflict (choice found too many times)
				else: 
					# If priority and different indice, solve the conflict
					if priority:
						if ind[i] > ind[dist_choice_user[user_choice]]:
							ind[i] += 1
							conflict = True
						elif ind[i] < ind[dist_choice_user[user_choice]]:	
							ind[dist_choice_user[user_choice]] += 1
							dist_choice_user[user_choice] = i
							conflict = True
						if conflict:
							break
					if rand[i] < rand[dist_choice_user[user_choice]]:
						ind[i] += 1
					else:
						ind[dist_choice_user[user_choice]] += 1
						dist_choice_user[user_choice] = i
					conflict = True
					break

			# Choice not found				
			else:
				dist_choice_user[user_choice] = i
				found[user_choice] = 1

	nsc = 0
	for i in range(0, num_users):
		nsc += ind[i]
	if best_nsc > nsc:
		best_nsc = nsc
		best_ind = np.copy(ind)
		print("Non-satisfaction coefficient   : {} (the lower is the better)".format(nsc))


# --- Display results ---
print("\n--- Results for non-satisfaction coefficient = {}".format(best_nsc))
for i in range(0, num_users):
	print(data[0,i],"gets the choice",data[best_ind[i],i]," (ind {})".format(best_ind[i]))


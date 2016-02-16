


#when you add an item, you need three pieces of information
#Name, Ammount, Monthly (optional y/n value)
#store it in my data dictionary
def add_an_item(data):
	#check the header state and call the right add method 
	if data["Custom headers"] == True:
		add_an_item_custom(data["data"])
	else:
		name = raw_input("Name: ")
		dupe = True
		while dupe:
			dupe = check_for_dupes(data["data"], name)
			if dupe:
				name = raw_input("Name taken, enter another: ")
		#print "Adding %s" %name
		data["data"].append([name, raw_input("Amount: "), raw_input("Monthly: ")])

def add_an_item_custom(data):
	#i'll need to get the input for each item in the header and then append that array to my data
	tmp_array =[]
	for item in data[0]:
		string = raw_input(item + ": ")
		'''
		dupe = True
		while dupe:
			dupe = check_for_dupes(data, string)
			if dupe:
				name = raw_input("Name taken, enter another: ")
		'''
		tmp_array.append(string)
	data.append(tmp_array)
	
#Look for the amount column and add the stuff in that column only
#print it out in dollars
#TO DO add a try/catch on amount
def calculate_total(data):
	total = 0 
	#find the amount column and then sum only that column
	for item in data[1:]:
		total += float(item[data[0].index("amount")])
	return total

#iterate through my array of arrays
#Print out the contents and sum the cost
def show_items(data):
	print "Here is your budget: "
	for index, item in enumerate(data["data"]):
		print index, ', '.join(item)
	print "Total: $" + '{0:,.2f}'.format(calculate_total(data["data"]))

#remove the selected item for the given data structure
def remove_items(data_xlist):
	item_to_rmv = raw_input("which item would you like to remove? ")
	for index, item in enumerate(data_xlist["data"]):
		if item[0] == item_to_rmv:
			print "removing " + ', '.join(data_xlist["data"][index])
			data_xlist["data"].remove(data_xlist["data"][index])
	print data_xlist["data"]

#iterate through the array and the name index
#if it matches then prompt the user to enter something else
#currently not applied to cases where you are using custom headers
def check_for_dupes(data, item):
	if len(data) == 0:
		return False
	else:
		for items in data:
			if item == items[0]:
				dupe = True
			else:
				dupe = False
	return dupe

#open the file for writing
#write the items in the data structure and append new lines
def write_csv(data):

	if data["filename"] == "default":
		data["filename"]= raw_input("What do you want to call your budget file? ") + ".csv"
	print "Writing your csv file to %s" %data["filename"]
	#data[0]=['Name', 'Amount', 'Monthly']
	with open(data["filename"], "w") as f:
		for items in data["data"]:
			f.write(','.join(items) + '\n')

#open the file for reading 
#use readlines to get back an array with each line 
#strip the new line and spit back out via a for loop
def read_csv(data):
	del data["data"][:]
	data["filename"] = raw_input("What's the name of the file you want to read? ")
	print "Reading %s" %data["filename"]
	with open (data["filename"], 'r') as f:
		tmp_array = f.readlines() #array of strings with new lines
	for item in tmp_array:
		data["data"].append((item.strip()).split(','))
	print data["data"]
	if len(data["data"]) > 3:
		data["Custom headers"] = True


def header(data):
	done = False
	tmp_array = []
	customize = raw_input("Would you like to define your own headers? Enter Y or N ").lower()
	if(customize == 'y'):
		while not done:
			header = raw_input("Enter the name of your header, or enter d if you are done: ").lower()
			if header == 'd':
				done = True
			else:
				tmp_array.append(header)
		data["data"]=[tmp_array]
		data["Custom headers"]= True
	else:
		data["data"]= [['name', 'amount', 'monthly']]
		data["Custom headers"]= False
	#return data, customize

def print_commands(data):
	print "Commands"
	print '*' * 50
	for k,v in data.iteritems():
		print k + ": " + v[0]
	print '*' * 50 + '\n'

#main budget engine 
#Get the initial user input and process their command
#exit when the user inputs 'q'
def ui_loop():
	commands = {"a": ("Add an Item",add_an_item), "s":("Show Items",show_items), "r":("Remove an item",remove_items), "q":"Quit the program", "w":("Save your budget to a file", write_csv), "o":("Open a budget file", read_csv)}
	state = {"data": "array of arrays", "Custom headers": "", "filename":"default"}
	header(state)
	quit= False
	while not quit:
		print_commands(commands)
		user_input=(raw_input("what do you want to do? ")).lower()
		if user_input == 'q':
			print "Thanks for budgeting!"
			quit = True
		elif user_input in commands.keys():
			commands[user_input][1](state)
		else:
			print "Use one of the available commands!"


ui_loop()

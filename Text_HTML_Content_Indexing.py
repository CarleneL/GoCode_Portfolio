import string
import os
import pprint
from re import sub
"""
Google Like Content Indexer. Given a directory, this script will index the content of the filess, and allow for basic searching. Entering a list of words at the prompt will return a list of files containing those words
"""

stop_words = ['a','an','and','i']
'''
Recursviely walks through a directory to return a list of files in a directory
'''
def recursive_find(dirname,file_list):
	array_all = os.listdir(dirname)
	for item in array_all:
		if item == ".DS_Store":
			continue
		else:
			path = os.path.join(dirname, item)
			if os.path.isdir(path):
				recursive_find(path,file_list)
			else:
				file_list.append(path)
	return file_list
'''
Given a list of files, open each file, and get a list of words from each file
Helper methods will verify the file extension and call the appropriate read_file method 
'''
def index_all_files(file_list, dictionary):
    for the_file in file_list:
    	dictionary_builder(check_file_extension(the_file)(read_file(the_file)), the_file, dictionary)
'''
Given a list of words in a file, build a list of unique words.
Each word will be a dictionary key and its value pair will be an array of files containing that word
'''
def dictionary_builder(wordlist, filename, dictionary):
	for word in wordlist:
		if word in dictionary.keys():
			if filename in dictionary[word]:
				continue
			else:
				dictionary[word].append(filename)
		else:
			if word not in stop_words:
				dictionary[word] = [filename]
			else:
				continue

'''
Given a file name, open it and spit it out into an array 
'''
def read_file (filename):
	tmp_array = []
	with open(filename, "r") as f:
		tmp_array = f.readlines()
	return tmp_array

'''
Given a filename, check the file extension and return the appropriate function name
'''
def check_file_extension(filename):
	index = filename.index('.')
	extension = filename[index:]
	if extension == ".txt":
		return file_to_wordlist
	elif extension == ".html" or extension == ".htm":
		return html_file_to_wordlist
	else:
		return unknown
def unknown(filename):
	print "unknown file type: " + str(filename)

'''
File_to_wordlist will take a list of lines form a txt file and split them up into an array of words that I can iterate over later
Punctuation and spaces will be ignored
Returns a list of words
'''
def file_to_wordlist (array_of_file_lines):
	word = ""
	wordlist = []
	for item in array_of_file_lines:
		item.replace('\n',"")
		for letter in item:
			if not is_space(letter) and not is_punctuation(letter):
				word += letter.lower()
				if letter == item[-1] and item == array_of_file_lines[-1]:
					wordlist.append(word)
			elif is_space(letter) or is_punctuation(letter):
				if len(word):
					wordlist.append(word)
					word = ""
				else:
					continue
	return wordlist

'''
html_tile_to_wordlist will take a list of lines form a .html file and split them up into an array of words that I can iterate over later
Punctuation, spaces, and tags will be ignored
Returns a list of words
'''
def html_file_to_wordlist (array_of_html_lines):
	word = ""
	wordlist = []
	for index in range(0, len(array_of_html_lines)):
		array_of_html_lines[index] = sub('[ \t\r\n]+', ' ', array_of_html_lines[index])
		for letter in array_of_html_lines[index]:
			if letter == '<':
				break
			else:
				if not is_space(letter) and not is_punctuation(letter):
					word += letter.lower()
				elif is_space(letter) or is_punctuation(letter):
					if len(word):
						wordlist.append(word)
						word = ""
					else:
						continue
	return wordlist

'''
helper methods for parsing file text
'''
def is_space(character):
	return character == ' '

def is_punctuation(character):
	punctuation = '!"#$%&\n()*+,-./:;<=>?@[\\]^_`{|}~'
	return character in punctuation

'''
This will just be a dictionary look up on the keywords
Given a dictionary and a list of keywords to search for, this function will return a list of search results for the keywords
'''
def find_files_with(index,keywords):
	search_results = {}
	for word in keywords:
		if word in index.keys():
			search_results[word] = index[word]
		else:
			search_results[word] = "Not Found"
	return search_results

'''
Takes a comma delimited string and strips spaces and splits on commas
Returns an array with user input
'''
def user_input_to_array(string):
	string_list = string.lower().split(',')
	for index in range(0, len(string_list)):
		string_list[index] = string_list[index].strip()
	return string_list

'''
set up any required data structures and kick off the user input call
leverages the PPrint module to pretty print the search results which are a series of dictionary key/value pairs
'''
def index_engine():
	#hard_coding_directory
	directory = '/Users/Carly/Documents/GoCode/ContentIndex'

	master_dictionary = {}
	index_all_files(recursive_find(directory, []), master_dictionary)
	
	#search across the hardcorded directory and return the search results
	search_results = find_files_with(master_dictionary, user_input_to_array(raw_input("Enter a comma separated list of words to search for: ")))
	pprint.pprint(search_results)

index_engine()



        


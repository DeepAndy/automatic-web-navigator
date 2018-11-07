'''
Author: Austin Moore
Date Created: 10-29-18
Description: Script for cleaning up HTML files during migration from CommonSpot
			 to Drupal
'''

import re
import urllib2
import StringIO
import getpass
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def translate_html(textarea):
	if (re.findall(r'data-editor-value-original=\"((.|\n)*?)\"', textarea)):
	    textarea = re.findall(r'data-editor-value-original=\"((.|\n)*?)\"', textarea)[0]
	elif (re.findall(r'data-editor-value-original=\"((.|\n)*?)</textarea>', textarea)):
	    textarea = re.findall(r'data-editor-value-original=\"((.|\n)*?)</textarea>', textarea)[0]
	else:
		print("Could not find the textarea HTML for this site.")
		print
		print("Possible solutions:")
		print
		print("Make sure your username and password were entered correctly.")
		print
		quit()

	# create a subclass and override the handler methods
	class MyHTMLParser(HTMLParser):
	    def handle_starttag(self, tag, attrs):
	        print "Start tag:", tag
	        for attr in attrs:
	            print "     attr:", attr

	    def handle_endtag(self, tag):
	        print "End tag  :", tag

	    def handle_data(self, data):
	        print "Data     :", data

	    def handle_comment(self, data):
	        print "Comment  :", data

	    def handle_entityref(self, name):
	        c = unichr(name2codepoint[name])
	        print "Named ent:", c

	    def handle_charref(self, name):
	        if name.startswith('x'):
	            c = unichr(int(name[1:], 16))
	        else:
	            c = unichr(int(name))
	        print "Num ent  :", c

	    def handle_decl(self, data):
	        print "Decl     :", data

	# instantiate the parser and feed it some HTML
	parser = MyHTMLParser()
	textarea = parser.unescape(textarea[0])

	return textarea


def find_errors(lines):
	errors = []
	warnings = []
	print_friendly_errors = []
	error_line_string = [] # For saving the line string an error is on
	first_header_found = False

	last_header_old = 2
	first_header_start = 2
	current_header_num = 3 # Whatever the current header is when we iterate
	found_first_head = False

	# Iterate through each line and find errors
	for i in range(len(lines)):
		if (re.findall(r'<h\d.*?>', lines[i])):
			header = re.findall(r'<h(\d).*?>', lines[i])[0]
		else:
			header = ""

		if (header != "2" and header != "" and first_header_found == False):
			first_header_found = True
			errors.append("<h>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": First header is not an <h2>")
			error_line_string.append(lines[i])
		elif (header == "2" and first_header_found == False):
			first_header_found = True
		if (re.findall(r'<hr />', lines[i])):
			errors.append("<hr />")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <hr /> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<hr.*?>', lines[i])):
			errors.append("<hr>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <hr> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<b>', lines[i])):
			errors.append("<b>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <b> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<i>', lines[i])):
			errors.append("<i>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <i> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<u>', lines[i])):
			errors.append("<u>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <u> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<span.*?>', lines[i])):
			errors.append("<span>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <span> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'&nbsp;', lines[i])):
			errors.append("&nbsp;")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": &nbsp; found")
			error_line_string.append(lines[i])
		if (re.findall(r'<img.*?>.*</img>', lines[i])):
			errors.append("<img>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <img> tag found. Will delete and needs to be Drupal embedded")
			error_line_string.append(lines[i])
		if (re.findall(r'<img.*/>', lines[i])):
			errors.append("<img>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <img> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<div.*?>.*</div>', lines[i])):
			errors.append("<div>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": <div> tag found")
			error_line_string.append(lines[i])
                if (re.findall(r'<p>\s*</p>', lines[i])):
                        errors.append("empty <p>")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": empty <p> tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'<[^/>]+>[ \n\r\t]*</[^>]+>', lines[i])):
			warnings.append("empty")
			print_friendly_errors.append("WARNING, Line " + str(i + 1) + ": empty tag found")
			error_line_string.append(lines[i])
		if (re.findall(r'\?', lines[i])):
			warnings.append("?")
			print_friendly_errors.append("WARNING, Line " + str(i + 1) + ": ? found")
			error_line_string.append(lines[i])
		if (re.findall(r'\.cfm', lines[i])):
			warnings.append("cfm")
			print_friendly_errors.append("WARNING, Line " + str(i + 1) + ": .cfm found")
			error_line_string.append(lines[i])
		if (re.findall(r' style\s*?=\s*?\".*?\"', lines[i])):
			errors.append("style=")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": inline style found")
			error_line_string.append(lines[i])
		if (re.findall(r' class\s*?=\s*?\".*?\"', lines[i])):
			errors.append("class=")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": CSS class found")
			error_line_string.append(lines[i])
		if (re.findall(r' dir\s*?=\s*?\".*?\"', lines[i])):
			errors.append("dir=")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": dir attribute found")
			error_line_string.append(lines[i])
		if (re.findall(r'author.oit.ohio.edu', lines[i])):
			warnings.append("author")
			print_friendly_errors.append("WARNING, Line " + str(i + 1) + ": author link found")
			error_line_string.append(lines[i])
		if (re.findall(r'\.pdf', lines[i])):
			errors.append("pdf")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": PDF link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		if (re.findall(r'\.docx', lines[i])):
			errors.append("docx")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": DOCX link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		elif (re.findall(r'\.doc', lines[i])):
			errors.append("doc")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": DOC link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		if (re.findall(r'\.pptx', lines[i])):
			errors.append("pptx")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": PPTX link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		elif (re.findall(r'\.ppt', lines[i])):
			errors.append("ppt")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": PPT link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		if (re.findall(r'\.xlsx', lines[i])):
			errors.append("xlsx")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": XLSX link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		elif (re.findall(r'\.xls', lines[i])):
			errors.append("xls")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": XLS link found. Will add brackets but this still needs Drupal embedded")
			error_line_string.append(lines[i])
		elif (re.findall(r'id="CP___PAGEID=.*?"', lines[i])):
			errors.append("cp_pageid")
			print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": CP___PAGEID found.")
			error_line_string.append(lines[i])

		# Find out of order headers if there are any
		if (re.findall(r'<h\d.*?>', lines[i])): # The first time we find a header
			# If we have not found a first header before
			if (found_first_head == False):
				first_header_start = re.findall(r'<h(\d).*?>', lines[i])[0]
				found_first_head = True
				last_header_old = first_header_start
			# If we have found a non-first header
			else:
				current_header_num = re.findall(r'<h(\d).*?>', lines[i])[0]
				if (int(current_header_num) > int(last_header_old) + 1): # Give error if out of order
					errors.append("order")
					print_friendly_errors.append("ERROR, Line " + str(i + 1) + ": header out of order")
					error_line_string.append(lines[i])
					last_header_old = int(current_header_num)
				else:
					last_header_old = int(current_header_num) # Update the last header

	return lines, errors, warnings, print_friendly_errors, error_line_string


# Prints all error messages
def print_errors(print_friendly_errors, error_line_string, errors, warnings):
	if (len(errors) == 0 and len(warnings) == 0):
		print("There are no errors :)")
	else:
		for i in range(len(print_friendly_errors)):
			print(print_friendly_errors[i])
			print(error_line_string[i].strip("\t"))
	print (str(len(errors)) + " Errors | " + str(len(warnings)) + " Warnings")
	print
	if (len(warnings) != 0):
		print("Note: Warnings can not be fixed.")
		print

def print_errors_gui(print_friendly_errors, error_line_string, errors, warnings):
        gui_printout = ""
	if (len(errors) == 0 and len(warnings) == 0):
                gui_printout += "There are no errors :)\n\n"
	else:
		for i in range(len(print_friendly_errors)):
                        gui_printout += print_friendly_errors[i] + '\n\n'
                        gui_printout += error_line_string[i].strip('\t') + '\n\n'
        gui_printout += (str(len(errors)) + " Errors | " + str(len(warnings)) + " Warnings") + "\n\n"
	if (len(warnings) != 0):
                gui_printout += "Note: Warnings can not be fixed.\n\n"
        return gui_printout


# Fix all errors
def fix_all(lines, errors):
	# Assign default values
	last_header_old = 2
	first_header_start = 2
	last_header_num = 2
	correct_first_header_num = 2 # The header that we should ALWAYS start with
	current_header_num = 3 # Whatever the current header is when we iterate
	new_header_num = 2 # What the current header should be when we iterate
	max_header_num = 6 # The max a header can be. Is 6 in HTML 5
	found_first_head = False
	order = False

        new_text = ""

	# Check if we have an issue with the first header in the errors list
	for i in range(len(errors)):
		if (errors[i] == "order"):
			order = True

	# Go ahead and replace same of these easy to find errors
	for i in range(len(lines)):
		if (i > len(lines) - 1):
			break

		lines[i] = re.sub(r'<hr.*?>', "", lines[i])
		lines[i] = re.sub(r'<hr />', "", lines[i])
		lines[i] = re.sub(r'<b>', "<strong>", lines[i])
		lines[i] = re.sub(r'</b>', "</strong>", lines[i])
		lines[i] = re.sub(r'<i>', "<em>", lines[i])
		lines[i] = re.sub(r'</i>', "</em>", lines[i])
		lines[i] = re.sub(r'<u>', "", lines[i])
		lines[i] = re.sub(r'</u>', "", lines[i])
		lines[i] = re.sub(r'<img.*?>.*</img>', "", lines[i])
		lines[i] = re.sub(r'<img.*?/>', "", lines[i])
		lines[i] = re.sub(r'<div.*?>', "", lines[i])
		lines[i] = re.sub(r'</div>', "", lines[i])
		lines[i] = re.sub(r'<h\d>&nbsp;</h\d>', "", lines[i])
		lines[i] = re.sub(r'<p>&nbsp;</p>', "", lines[i])
		lines[i] = re.sub(r'<p>\s*</p>', "", lines[i])
		lines[i] = re.sub(r'&nbsp;', "", lines[i])
		lines[i] = re.sub(r'<span.*?>', "", lines[i])
		lines[i] = re.sub(r'</span>', "", lines[i])
		lines[i] = re.sub(r' class\s*?=\s*?\".*?\"', "", lines[i])
		lines[i] = re.sub(r' style\s*?=\s*?\".*?\"', "", lines[i])
		lines[i] = re.sub(r' dir\s*?=\s*?\".*?\"', "", lines[i])
		lines[i] = re.sub(r' id\s*?=\s*?\"\s*?CP___PAGEID.*?"', "", lines[i])
                lines[i] = re.sub(r'<p>\s*</p>', "", lines[i])

		# Fixing headers
		if (order == True): # Use the out of order headers method
			if (re.findall(r'<h\d.*?>', lines[i])): # The first time we find a header
				# If we have not found a first header before - assign values and make sure it is correct
				if (found_first_head == False):
					first_header_start = re.findall(r'<h(\d).*?>', lines[i])[0]
					last_header_num = correct_first_header_num
					found_first_head = True
					lines[i] = re.sub(r'<h\d.*?>', "<h" + str(correct_first_header_num) + ">", lines[i])
					lines[i] = re.sub(r'</h\d>', "</h" + str(correct_first_header_num) + ">", lines[i])
					last_header_old = first_header_start
				# If we have found a non-first header - assign values and make sure they are correct
				else:
					current_header_num = re.findall(r'<h(\d).*?>', lines[i])[0]
					if (int(current_header_num) > int(last_header_old)): # Only modify headers that were larger or equal to the first header found in the file
						new_header_num = int(last_header_num) + 1
						if (new_header_num > 6):
							new_header_num = 6
						lines[i] = re.sub(r'<h\d.*?>', "<h" + str(new_header_num) + ">", lines[i])
						lines[i] = re.sub(r'</h\d>', "</h" + str(new_header_num) + ">", lines[i])
						last_header_old = int(current_header_num)
						last_header_num = new_header_num
					elif (int(current_header_num) == int(last_header_old)):
						new_header_num = last_header_num
						if (new_header_num > 6):
							new_header_num = 6
						lines[i] = re.sub(r'<h\d.*?>', "<h" + str(new_header_num) + ">", lines[i])
						lines[i] = re.sub(r'</h\d>', "</h" + str(new_header_num) + ">", lines[i])
						last_header_old = int(current_header_num)
						last_header_num = new_header_num
		else: # Use the scale relative to first header method if headers are not out of sync
			if (re.findall(r'<h\d.*?>', lines[i])): # The first time we find a header
				# If we have not found a first header before - assign values and make sure it is correct
				if (found_first_head == False):
					first_header_start = re.findall(r'<h(\d).*?>', lines[i])[0]
					found_first_head = True
					lines[i] = re.sub(r'<h\d.*?>', "<h" + str(correct_first_header_num) + ">", lines[i])
					lines[i] = re.sub(r'</h\d>', "</h" + str(correct_first_header_num) + ">", lines[i])
				# If we have found a non-first header - assign values and make sure they are correct
				else:
					current_header_num = re.findall(r'<h(\d).*?>', lines[i])[0]
					new_header_num = int(current_header_num) - (int(first_header_start) - correct_first_header_num)
					if (new_header_num > 6):
						new_header_num = 6
					lines[i] = re.sub(r'<h\d.*?>', "<h" + str(new_header_num) + ">", lines[i])
					lines[i] = re.sub(r'</h\d>', "</h" + str(new_header_num) + ">", lines[i])

		# Fix any missing brackets for file extensions
		link_name = "dummy"
		if (re.findall(r'<a href\s*?=\s*?\".*?\.pdf\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.pdf\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[PDF\]', link_name)):
				new_link_name = link_name + " [PDF]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.docx\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.docx\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Word\]', link_name)):
				new_link_name = link_name + " [Word]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.doc\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.doc\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Word\]', link_name)):
				new_link_name = link_name + " [Word]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.pptx\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.pptx\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Powerpoint\]', link_name)):
				new_link_name = link_name + " [Powerpoint]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.ppt\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.ppt\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Powerpoint\]', link_name)):
				new_link_name = link_name + " [Powerpoint]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.xlsx\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.xlsx\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Excel\]', link_name)):
				new_link_name = link_name + " [Excel]"
				lines[i] = lines[i].replace(link_name, new_link_name)
		if (re.findall(r'<a href\s*?=\s*?\".*?\.xls\.*?\".*?</a>', lines[i])):
			link_name = re.findall(r'<a href\s*?=\s*?\".*?\.xls\.*?\"(.*?)</a>', lines[i])[0]
			if (not re.findall(r'\[Excel\]', link_name)):
				new_link_name = link_name + " [Excel]"
				lines[i] = lines[i].replace(link_name, new_link_name)
        for line in lines:
                new_text += line + '\n'

        return new_text


# Write everything to our output file
def write_out(lines, output):
	output_file = open(output, "w")
	for i in range(len(lines)):
		output_file.write(lines[i])

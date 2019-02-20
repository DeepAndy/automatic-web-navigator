'''
Author: Austin Moore
Date Created: 10-29-18
Description: Script for cleaning up HTML files during migration from CommonSpot
             to Drupal
'''

import re
import urllib
import getpass
import bs4
from html.parser import HTMLParser
from bs4 import BeautifulSoup

def translate_html(textarea):
    if (re.findall(r'data-editor-value-original=\"((.|\n)*?)\"', textarea)):
        textarea = re.findall(r'data-editor-value-original=\"((.|\n)*?)\"', textarea)[0]
    elif (re.findall(r'data-editor-value-original=\"((.|\n)*?)</textarea>', textarea)):
        textarea = re.findall(r'data-editor-value-original=\"((.|\n)*?)</textarea>', textarea)[0]
    else:
        print("Could not find the textarea HTML for this site.")
        print()
        print("Possible solutions:")
        print()
        print("Make sure your username and password were entered correctly.")
        print()
        quit()

    # instantiate the parser and feed it some HTML
    parser = HTMLParser()
    textarea = parser.unescape(textarea[0])

    return textarea

def find_errors(soup):
    errors = []
    warnings = []
    print_friendly_errors = []
    error_line_string = [] # For saving the line string an error is on
    first_header = True
    out_of_order = False

    # Iterate through each line and find errors
    for tag in soup.find_all():
        if (tag.name == "p"):
            if (re.findall(r"^\s*$", tag.text)):
                errors.append("empty <p>")
                print_friendly_errors.append("ERROR: empty <p> tag found")
                #error_line_string.append(lines[i])
            elif (re.findall(r"^\s*$", tag.text)):
                warnings.append("empty")
                print_friendly_errors.append("WARNING: empty tag found")
                #error_line_string.append(lines[i])
        if (re.findall(r"h\d", str(tag.name))):
            if (re.findall(r"^\s*$", tag.text)):
                errors.append("empty header")
                print_friendly_errors.append("ERROR: empty header tag found")
        if (tag.name == "hr"):
            errors.append("<hr />")
            print_friendly_errors.append("ERROR: <hr /> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "b"):
            errors.append("<b>")
            print_friendly_errors.append("ERROR: <b> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "i"):
            errors.append("<i>")
            print_friendly_errors.append("ERROR: <i> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "u"):
            errors.append("<u>")
            print_friendly_errors.append("ERROR: <u> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "span"):
            errors.append("<span>")
            print_friendly_errors.append("ERROR: <span> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "img"):
            errors.append("<img>")
            print_friendly_errors.append("ERROR: <img> tag found. Will delete and needs to be Drupal embedded")
            #error_line_string.append(lines[i])
        if (tag.name == "div"):
            errors.append("<div>")
            print_friendly_errors.append("ERROR: <div> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "script"):
            errors.append("<script>")
            print_friendly_errors.append("ERROR: <script> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "style"):
            errors.append("<style>")
            print_friendly_errors.append("ERROR: <style> tag found")
            #error_line_string.append(lines[i])
        if (tag.name == "link"):
            errors.append("<link>")
            print_friendly_errors.append("ERROR: <link> tag found")
            #error_line_string.append(lines[i])
        # First header is not an h2
        if (first_header == True):
            if (re.findall(r"^h(\d)$", tag.name)):
                if (int(re.findall(r"^h(\d)$", tag.name)[0]) != 2):
                    errors.append("<h>")
                    print_friendly_errors.append("ERROR: First header is not an <h2>")
                    #error_line_string.append(lines[i])
        if (re.findall(r'\?', tag.text)):
            warnings.append("?")
            print_friendly_errors.append("WARNING: ? found")
            #error_line_string.append(lines[i])
        if (tag.has_attr("href")):
            if (re.findall(r'\.cfm', tag["href"])):
                warnings.append("cfm")
                print_friendly_errors.append("WARNING: .cfm link found")
                #error_line_string.append(lines[i])
            if (re.findall(r'author.oit.ohio.edu', tag["href"])):
                warnings.append("author")
                print_friendly_errors.append("WARNING: author link found")
                #error_line_string.append(lines[i])
            if (re.findall(r'\.pdf', tag["href"])):
                errors.append("pdf")
                print_friendly_errors.append("ERROR: PDF link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            if (re.findall(r'\.docx?', tag["href"])):
                errors.append("docx")
                print_friendly_errors.append("ERROR: DOCX link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            elif (re.findall(r'\.doc', tag["href"])):
                errors.append("doc")
                print_friendly_errors.append("ERROR: DOC link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            if (re.findall(r'\.pptx', tag["href"])):
                errors.append("pptx")
                print_friendly_errors.append("ERROR: PPTX link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            elif (re.findall(r'\.ppt', tag["href"])):
                errors.append("ppt")
                print_friendly_errors.append("ERROR: PPT link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            if (re.findall(r'\.xlsx', tag["href"])):
                errors.append("xlsx")
                print_friendly_errors.append("ERROR: XLSX link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            elif (re.findall(r'\.xls', tag["href"])):
                errors.append("xls")
                print_friendly_errors.append("ERROR: XLS link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i])
            elif (re.findall(r'\.zip', tag["href"])):
                errors.append("zip")
                print_friendly_errors.append("ERROR: ZIP link found. Will add brackets but this still needs Drupal embedded")
                #error_line_string.append(lines[i]))

        if (tag.has_attr("style")):
            errors.append("style=")
            print_friendly_errors.append("ERROR: inline style found")
            #error_line_string.append(lines[i])
        if (tag.has_attr("class")):
            errors.append("class=")
            print_friendly_errors.append("ERROR: CSS class found")
            #error_line_string.append(lines[i])
        if (tag.has_attr("dir")):
            errors.append("dir=")
            print_friendly_errors.append("ERROR: dir attribute found")
            #error_line_string.append(lines[i])
        if (tag.has_attr("id")):
            if (re.findall("CP___PAGEID", tag["id"])):
                errors.append("id=")
                print_friendly_errors.append("ERROR: CP___PAGEID found")
                #error_line_string.append(lines[i])

        # Header order check
        if (out_of_order == False):
            if (re.findall(r"^h\d$", tag.name)):
                header_num = int(re.findall(r"^h(\d)$", tag.name)[0])

                if (first_header == False):
                    if ((header_num > last_header_num) and (header_num != last_header_num + 1)):
                        out_of_order = True
                        errors.append("order")
                        print_friendly_errors.append("ERROR: Headers are out of order")
                        #error_line_string.append(lines[i])

                first_header = False
                last_header_num = header_num

    return errors, warnings, print_friendly_errors, error_line_string

# Prints all error messages
def print_errors(print_friendly_errors, error_line_string, errors, warnings):
    if (len(errors) == 0 and len(warnings) == 0):
        print("There are no errors :)")
    else:
        for i in range(len(print_friendly_errors)):
            print(print_friendly_errors[i])
            #print(error_line_string[i].strip("\t"))

    print (str(len(errors)) + " Errors | " + str(len(warnings)) + " Warnings")
    print()

    if (len(warnings) != 0):
        print("Note: Warnings can not be fixed.")
        print()

def print_errors_gui(print_friendly_errors, error_line_string, errors, warnings):
    gui_printout = ""
    if (len(errors) == 0 and len(warnings) == 0):
        gui_printout += "There are no errors :)\n\n"
    else:
        for i in range(len(print_friendly_errors)):
            gui_printout += print_friendly_errors[i] + '\n\n'
            #gui_printout += error_line_string[i].strip('\t') + '\n\n'
        gui_printout += (str(len(errors)) + " Errors | " + str(len(warnings)) + " Warnings") + "\n\n"
    if (len(warnings) != 0):
        gui_printout += "Note: Warnings can not be fixed.\n\n"
    return gui_printout


# Fix all errors
def fix_all(soup, errors):
    # Assign default values
    first_header_correct = True
    order_correct = True
    min_header_num = 2
    max_header_num = 6

    # Check if first header is correct
    for error in errors:
        if (error == "<h>"):
            first_header_correct = False
            order_correct = False # Correcting the first header will put everything out of order

    # Check if headers are out of order
    for error in errors:
        if (error == "order"):
            order_correct = False

    # Correct out of order headers
    if (order_correct == False):
        first_header = True
        header_lookup = dict()

        for header in soup.find_all(re.compile(r"^h?\d+$")):
            header_num = int(re.findall(r"^h?(\d+)$", header.name)[0])

            if (first_header == True):
                header.name = "h" + str(min_header_num)
                first_header = False
                last_header_num = header_num
                correct_last_header = min_header_num
                header_lookup[str(header_num)] = correct_last_header
                continue
            elif ((header_num > last_header_num) and (header_num != correct_last_header + 1)):
                header.name = "h" + str(correct_last_header + 1)
                last_header_num = header_num
                correct_last_header += 1

                try:
                    header_lookup[str(header_num)]
                except:
                    header_lookup[str(header_num)] = correct_last_header

                continue
            elif (header_num < last_header_num):
                last_header_num = header_num

                try:
                    header.name = "h" + str(header_lookup[str(header_num)])
                    correct_last_header = header_lookup[str(header_num)]
                except:
                    correct_last_header = header_num

                continue
            elif (header_num == last_header_num):
                last_header_num = header_num
                header.name = "h" + str(correct_last_header)

                continue
            elif (header_num == correct_last_header + 1):
                last_header_num = header_num
                correct_last_header = header_num

                continue

    # Go ahead and replace same of these easy to find errors
    for tag in soup.find_all():
        if (re.findall(r"^\s*$", tag.get_text()) and tag.name != "td" and tag.name != "tr" and tag.name != "div" and tag.name != "br"):
            tag.decompose()
        if (tag.name == "hr"):
            tag.decompose()
        elif (tag.name == "script"):
            tag.decompose()
        elif (tag.name == "style"):
            tag.decompose()
        elif (tag.name == "link"):
            tag.decompose()
        elif (tag.name == "b"):
            tag.name = "strong"
        elif (tag.name == "i"):
            tag.name = "em"
        elif (tag.name == "u"):
            tag.unwrap()
        elif (tag.name == "img"):
            tag.decompose()
        elif (tag.name == "span"):
            tag.unwrap()
        elif (tag.name == "p"):
            if (re.findall(r"^\s*$", tag.text)):
                tag.decompose()
        elif (re.findall(r"h\d", str(tag.name))):
            if (re.findall(r"^\s*$", tag.text)):
                tag.decompose()
        elif (tag.name == "div"):
            unwrap_tags = False
            for tag2 in tag:
                if ((isinstance(tag2, bs4.element.NavigableString) and not re.findall(r"^\s*$", tag2)) or (tag2.name == "strong" or tag2.name == "em")):
                    unwrap_tags = True
                    tag.name = "p"
                elif (unwrap_tags == True and not isinstance(tag2, bs4.element.NavigableString)):
                    tag2.unwrap()
            if (re.findall(r"^\s*$", tag.get_text())):
                tag.decompose()
            elif (unwrap_tags == False):
                tag.unwrap()
        try:
            if (tag.has_attr("class")):
                del tag["class"]
            if (tag.has_attr("style")):
                del tag["style"]
            if (tag.has_attr("dir")):
                del tag["dir"]
            if (tag.has_attr("id")):
                if (re.findall("CP___PAGEID", tag["id"])):
                    del tag["id"]
            if (tag.has_attr("href")):
                if (re.findall("\.pdf", tag["href"])):
                    if (not re.findall("\[PDF\]", tag.text)):
                        tag.string += " [PDF]"
                if (re.findall("\.docx?", tag["href"])):
                    if (not re.findall("\[Word\]", tag.text)):
                        tag.string += " [Word]"
                if (re.findall("\.pptx?", tag["href"])):
                    if (not re.findall("\[Powerpoint\]", tag.text)):
                        tag.string += " [Powerpoint]"
                if (re.findall("\.xlsx?", tag["href"])):
                    if (not re.findall("\[Excel\]", tag.text)):
                        tag.string += " [Excel]"
                if (re.findall(r'\.zip', tag["href"])):
                    if (not re.findall(r'\[ZIP]', tag.text)):
                        tag.string += " [ZIP]"
        except:
            continue

    return soup

# Write everything to our output file
def write_out(soup, output):
    output_file = open(output, "w")
    output_file.write(str(soup))

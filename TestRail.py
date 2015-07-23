#!/usr/bin/python
from lxml import etree
import csv, re, os, sys

def read_csv(path):
	'''Takes in the path to the .csv file and returns a list of dictionaries where each dictionary is a test case.'''

	output = []
	for row in csv.DictReader(open(path, 'rU')):
		output.append(row)
	return output

def common(case, row, update_flag):
	'''Takes in the parent tag and a dictionary to create a sub-function that has all the common elements/tags each test will have when adding it to the xml tree.
	To add a new field, create the tag as a SubElement of custom.'''

	#if user decides to update existing test cases, it will grab the Case ID
	if update_flag == 'update':
		case_id = etree.SubElement(case, 'id').text = row['Case ID']

	title = etree.SubElement(case, 'title').text = row['Title'].decode('latin-1', 'ignore')
	custom = etree.SubElement(case, 'custom')
	#automated = etree.SubElement(custom, 'automated').text = row['Automated']
	#bvt = etree.SubElement(custom, 'bvt').text = row['BVT']
	scenario = etree.SubElement(custom, 'scenario').text = row['Scenario'].decode(encoding='latin-1')
	preconditions = etree.SubElement(custom, 'precondition').text = row['Preconditions'].decode(encoding='latin-1')
	expected_results = etree.SubElement(custom, 'expectedresults').text = row['Expected Results'].decode(encoding='latin-1')
	notes = etree.SubElement(custom, 'notes').text = row['Notes']
	ticket = etree.SubElement(custom, 'ticket').text = row['Jira Ticket']

	steps = etree.SubElement(custom, 'testingsteps')

	#creates the correct xml structure for each individual step
	step_list = row['Testing Steps'].rstrip('\n').split('\n')
	count = 1
	for s in step_list:
		#strips out everything before the actual step
		if update_flag == 'update':
			s = re.sub(r'\w+\. ', '', s)
		else:
			s = re.sub(r'\w+\) ', '', s)
		step = etree.SubElement(steps, 'step')
		index = etree.SubElement(step, 'index').text = str(count)
		content = etree.SubElement(step, 'content').text = s.decode(encoding='latin-1')
		count += 1

def build_xml(output, update_flag): 
	'''Takes in a list of dictionaries of test cases and first builds the main roots of the xml tree and then adds each test case in the appropriate sections of the tree.'''

	#create the root elements
	root_sections = etree.Element('sections')
	root_section = etree.SubElement(root_sections, 'section')
	if update_flag == 'new':
		master = raw_input("Enter your name: ") #name this to your name so you know what folder it goes into
	else:
		master = 'place_holder'
	root_name = etree.SubElement(root_section, 'name').text = master
	sub_sections = etree.SubElement(root_section, 'sections')

	track = set() #keep track of existing folders/section
	for row in output:
		#look to see if this folder/section already exists; if so, add a new case and custom underneath
		if row['Functional Area'] in track:
			for element in sub_sections:
				if element.get("folder") == row['Functional Area']:
					case = etree.SubElement(element[1], 'case')
					common(case, row, update_flag)
		#folder/section doesn't exist yet so create structure and add new case and custom underneath
		else:
			track.add(row['Functional Area'])
			section = etree.SubElement(sub_sections, 'section', folder=row['Functional Area'])
			name = etree.SubElement(section, 'name').text = row['Functional Area']
			cases = etree.SubElement(section, 'cases')
			case = etree.SubElement(cases, 'case')
			common(case, row, update_flag)

	result = etree.ElementTree(root_sections)
	return result

def main():

	#exception handling for any errors while running the script
	try:
		output = read_csv(os.path.join(os.getcwd(), sys.argv[1]))
		update_flag = sys.argv[3]

		if update_flag.lower() not in ['update', 'new']:
			print "The third argument only acccepts the values 'update' or 'new'."
			sys.exit(2)
		if ("." + re.sub(r'\w+\.', '', sys.argv[2])) != '.xml':
			print "The second argumment has to be a .xml file."
			sys.exit(2)

		result = build_xml(output, update_flag)
		result.write(os.path.join(os.getcwd(), sys.argv[2]), xml_declaration=True, encoding='utf-8', method="xml", pretty_print=True)
	except IndexError:
		print "You are missing an argument. Remember it's 'python TestRail.py name-of-csv-file.csv name-of-output-file.xml update | new'"

if __name__ == '__main__':
    main()
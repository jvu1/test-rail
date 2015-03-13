# TestRail Import Script

This is a script to convert test cases from excel/csv into XML so that they can be put into the QA test case management solution, TestRail.

This script depends on the lxml library to create the XML structure.

The Confluence page for how to run this script is here: https://fulcrumtech.atlassian.net/wiki/display/QAS/Importing+Test+Cases+into+TestRail

## Prerequisites:
1. Download and install the lxml library 
	1. Run the command `sudo easy_install pip` via command line
	2. Run `pip install lxml` (run it with sudo if you get a permissions error) via command line.

## Important Fields:

- Folder: The name of the folder the test case belongs to. For example, if you have multiple test cases that fit into Inventory Picking, make sure you label them in this field (required field).
- Title: The title of the test case (required field).
- Automated: This field will only accept TRUE or FALSE. If you know the test case has been automated, the value should be TRUE (required field).
- BVT: This field will only accept TRUE or FALSE. If the test is part of a BVT, the value should be TRUE (required field).
- Scenario: The scenario the user will be testing for (required field).
- Preconditions: Any conditions that need to be met to run the test case (not a required field).
- Testing Steps: The steps have to be entered in one cell and entered in a very specific format or else they will not import correctly. Place each step in the same cell, but on a new line (ctrl+alt+enter for mac, alt+enter for windows) numbered like 1) , 2) , etc (required field).
- Expected Results: The results the user should be expecting after running the test case (required field).
- Notes: Any additional notes about the test cases (required field).
- JIRA Ticket: JIRA ticket number (required field).

## Updating TestRail Test Cases:
1. Export the test cases into .csv. Keep in mind you cannot specifically target which test cases you want to export as TestRail will export all test cases in the suite.
2. Open the .csv file and in first cell (A1), there will be some weird characters. Rename this cell to 'Case ID'.
3. Update the test cases you want in the .csv file, while making sure they adhere to the format stated in the Important Fields section, especially Testing Steps.
4. When you are done updating, make sure the .csv file is in the same directory or folder as the TestRail.py script in the Files section.
5. Open up command prompt and navigate to the location of the .csv and TestRail.py files.
6. Run the following command: `python TestRail.py name-of-csv-file.csv name-of-output-file.xml update`
	1. The name of the .csv file should be the name of the file from step 2.
	2. The name of the output file is what you want to name it. Make sure the extension is .xml.
	3. Example: "python TestRail.py john.csv john.xml update"
7. It will also ask you enter a name. Enter any name you want as this doesn't matter when updating test cases.
8. If successful, the .xml file will be created in the same location as the script and the .csv file.
9. Import the .xml file into TestRail in your chosen location/suite.

## Importing New Test Cases:
1. Make sure all of your test cases are in the format stated in the Important Fields section and in this document: template_new.xlsx
2. Save your spreadsheet as a .csv by using Save As and choosing the Comma Separated Values (.csv) option in Excel.
3. Save TestRail.py and the .csv file from step 2 into the same folder.
4. Using command line, navigate to the location of the folder from step 3.
5. Run the command `python TestRail.py name-of-csv-file.csv name-of-output-file.xml new` 
	a. The name of the .csv file should be the name of the file from step 2.
	b. The name of the output file is what you want to name it. Make sure the extension is .xml.
	c. Example: `python TestRail.py john.csv john.xml new`
6. After you run the command, it will ask you to enter your name. This will be the master folder where all of your test cases will be in once they are imported.
7. If successful, the .xml file will be created in the same location as the script and the .csv file.
8. Import the .xml file into TestRail in your chosen location/suite.
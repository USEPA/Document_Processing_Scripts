# ERMD Document Processing Scripts

# Categorized Training Data
###### This is a guide for how to download and then process categorized documents from ECMS. To prepare the documents for a machine learning model the files need to have text extracted and saved into a txt file within a folder with a record schedule as the folder name.

1. Records from Documentum are downloaded as a zip file using the Documentum API. The filename contains the Object ID. To download records from Documentum use the following script: **Dctmdl.py**.
2. To unzip all of the records and create folders with the correct record schedule names use **Unzip_Rename.py**. This script is capable of crosswalking old record schedules with the new consolidated record schedule.
3. Now that the files have been unzipped they need to be converted to txt files so that they can be ingested by the machine learning model. Use the **extract.py** script to convert all PDFs, DOCs, PPTs, etc. to txt files. This script leverages the Tika component of the Content Ingestion Services to extract text and write it to a txt file.

# Uncategorized Training Data
###### The following set of scripts are used to process exported records from ECMS that are uncategorized and prepare them for categorization. These records will ultimatly be saved to our training dataset once categorized.
**trainingdata_part1.py** - this script moves the files into the appropriate folder named by record schedule id. This sets up the files for manual categorization.<br />
**trainingdata_part2.py** - this script moves the files into the appropriate folder named by record schedule based on the results of manual categorization. This script also extract the text using tika services and converts the files to txt format for ingestion into the ML model.<br />
**getidfilename.py** - this script generates the excel spreadsheet used to categorize the records by NRMP contractors. It grabs all filenames and record IDs from the newfile folder.

# Record Schedules
###### We are currently using word documents that are then converted to txt files to extract the current record schedules, but this process may change in the future to being managed in a database.
**excel-description.py, excel-guidance.py, excel-itemdescription.py** - pulls from an excel spreadsheet and creates txt files with record schedule descriptions, item descriptions and their guidance. These scripts ensure that each record schedule folder in our training dataset contains at a minimum description and guidnace information.<br />
**extractitem.py** - 
1) Run **extract.py** onto word documents providing the full record schedule details to generate the text files (Provided by NRMP contractor).
2) Run **extractitem.py** which extracts item description from text files containing the full record schedule details into a spreadsheet. 
3) Run **excel-itemdescription.py** to create the appropriate text files from the extracted item descriptions<br />

# Testing
###### Once the ML model is updated, these scripts are used for load testing and to determine document processing time.
**CIS Testing.py** - this script takes a record as an input and displays the prediction, summary and extracted keywords as an output. This script also displays the time it takes to process a record through each component of the Content Ingestion Services.<br />

# Dependencies
###### Some of the document processing scripts rely on other scripts to be imported to function or spreadsheets that they can read, they will be listed here.
**Buildfolder.py** - User can select a source and target folder for their files.<br />
**Extractultil.py** - Cleans up text including removing unicode and special characters.<br />

**trainingdata_part2.py** - *trainingdata_part2.xlsx* is required. This spreadsheet must contain Record ID, Record Schedule, and Title/filename without extension.<br />
**cxwalk.py** - *xwalk.csv* is required. This spreadsheet must contain Previous EPA Number,	Previous Item Number, New EPA Number, New Item Number, and	Function Code. <br />
**excel-description.py** - *Schedules Description.xlsx* is required. **Need to add headers back in**. <br />
**excel-guidance.py** - *Schedules Guidance.xlsx* is required. **Need to add headers back in**. <br />
**excel-itemdescription.py** - *item_descriptions.xlsx* is required. **Need to add headers back in**. <br /><br/>

**Unzip_Rename.py** - **buildfolder.py** is required. <br />
**Extract.py** - **buildfolder.py**, **extractultil.py** and **cxwalk.py** are required.
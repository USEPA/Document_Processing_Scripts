# ERMD Document Processing Scripts

###### This is a guide for how to download and then process documents from Documentum. To prepare the documents for a machine learning model the files need to have text extracted and save that text into a txt file within a folder with a record schedule as the folder name.

1. Records from Documentum are downloaded as zip files with Object IDs as the name. To download records from Documentum use **Dctmdl.py**.
2. To unzip all of the records and create folders with the correct record schedule name use **Unzip_Rename.py**.
3. Now that the files have been unzipped they need to be converted to txt files so that they can be ingested by the machine learning model. Use the **extract.py** script to convert all PDFs, DOCs, PPTs, etc. to txt files.

# Dependencies
###### Some of the document processing scripts rely on other scripts to be imported to function, they will be listed here.
**Buildfolder.py** - User can select a source and target folder for their files.<br />
**Extractultil.py** - Cleans up filenames

# Record Schedules
###### We are currently using word documents that are then converted to txt files to extract the current record schedules, but this process may change in the future to being managed in a database.
**excel-description.py, excel-guidance.py, excel-itemdescription.py** - pulls from an excel spreadsheet and creates txt files with record schedule descriptions and their guidance.<br />
**extractitem.py** - Refresh the item description, adds item description to the training data.<br />
**trainingdata_part2a.py**

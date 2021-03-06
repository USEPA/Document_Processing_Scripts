import xlrd
import os

#def replace_with_underscores(cell):
#    return cell.value.replace(" ", "_")

basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\Main\\"
# Change filename if applicable
wb = xlrd.open_workbook("item_descriptions.xlsx")
sh = wb.sheet_by_index(0)


rows = sh.get_rows()
# Skip header row
next(rows)


for row in rows:
    # Extract value from spreadsheet and save to variable
    schedule = row[0].value
    content = row[1].value

    # Construct filename of text file
    filename = schedule + "-item-description.txt"
    # Change Location to reflect where output folders are located
    if not os.path.exists(basepath+schedule):
        os.makedirs(basepath+schedule)
        print(folder + " created")
    with open(os.path.join(basepath+schedule,filename), "w", encoding='utf-8') as f:
        # Write content and print filename when successful
        f.write(content)
        print(filename + " written")

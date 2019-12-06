import xlrd
import os

#def replace_with_underscores(cell):
#    return cell.value.replace(" ", "_")

basepath = "C:\\Users\\AYuen\\Environmental Protection Agency (EPA)\\ECMS - Documents\\Extract Documentum\\Main\\"
# Change filename if applicable
wb = xlrd.open_workbook("Schedules Guidance.xlsx")
sh = wb.sheet_by_index(0)

for row in sh.get_rows():
    # Extract value from spreadsheet and save to variable
    schedule = row[0].value
    folder = row[3].value
    content = row[4].value

    # Construct filename of text file
    filename = schedule + "-guidance.txt"
    # Change Location to reflect where output folders are located
    if not os.path.exists(basepath+folder):
        os.makedirs(basepath+folder)
        print(folder + " created")
    with open(os.path.join(basepath+folder,filename), "w", encoding='utf-8') as f:
        # Write content and print filename when successful
        f.write(content)
        print(filename + " written")

Use QLIK, filter by AA, exclude tempt, then export data
row 1 should contain "Lan_ID"
row 6 should contain "Record ID"

rename export to "Records IDs.xlsx"
run generate_dql.py
submit the resulting 2 text files for export from documentum
keep Records_Export for reference 
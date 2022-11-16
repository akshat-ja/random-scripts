import klayout.db as db

ly = db.Layout()
top_cell = ly.create_cell("ARA_TOP_FILL")


for file in [ "ARA_TOP.gds.gz", "ARA_TOP_DM.gds", "ARA_TOP_DODPO.gds" ]:

	ly_import = db.Layout()
	ly_import.read(file)
	imported_top_cell = ly_import.top_cell()
	
	target_cell = ly.create_cell(imported_top_cell.name)
	target_cell.copy_tree(imported_top_cell)

	ly_import._destroy()
	
	inst = db.DCellInstArray(target_cell.cell_index(), db.DTrans(db.DVector(0, 0)))
	top_cell.insert(inst)

ly.write("ARA_TOP_FILL.gds")



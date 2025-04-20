# =============================================================================
# input_dtype
# =============================================================================
input_dtype = {
'YEAR':str,
'Year':str,
'TYPE_PROC':str,
'PORT':str,
'PORT_NAME':str,
'WTWY':str,
'WTWY_NAME':str,
'STATE':str,
'FORPORT':str,
'FORPORT_NAME':str,
'CTRY_F':str,
'CTRY_F_NAME':str,
'CTRY_C':str,
'CTRY_C_NAME':str,
'PMS_COMM':str,
'PMS_NAME':str,
'TONNAGE':float,
'COASTDST':str,
 }

# =============================================================================
# inputfile_loc_by_year
# =============================================================================
inputfile_loc_by_year = {
    2017:r"S:\NAOA\Projects\Other\USA-ROK_Green_Shipping_Corridor\02.Tasks\01.Cargo_Flow\01.Input_Data\01.USACE\02.Foreign_Cargo_Import_Export\Raw_Data\2017\7022fdb0-12ab-462a-fff7-c7aabe7979c1___Exports_Imports_2017.xlsx",
    2018:r"S:\NAOA\Projects\Other\USA-ROK_Green_Shipping_Corridor\02.Tasks\01.Cargo_Flow\01.Input_Data\01.USACE\02.Foreign_Cargo_Import_Export\Raw_Data\2018\32b68971-ff0d-431c-b335-48981c7c3df8___Exports_Import_2018.xlsx",
    2019:r"S:\NAOA\Projects\Other\USA-ROK_Green_Shipping_Corridor\02.Tasks\01.Cargo_Flow\01.Input_Data\01.USACE\02.Foreign_Cargo_Import_Export\Raw_Data\2019\45f8f094-fc47-4d37-a3b6-bafef5e83f4c___Exports_Imports_2019.xlsx",
    2020:r"S:\NAOA\Projects\Other\USA-ROK_Green_Shipping_Corridor\02.Tasks\01.Cargo_Flow\01.Input_Data\01.USACE\02.Foreign_Cargo_Import_Export\Raw_Data\2020\c0b8c657-70d0-45ba-8925-7fcbf726b4bd___Imports_Exports_2020.xlsx",
    2021:r"S:\NAOA\Projects\Other\USA-ROK_Green_Shipping_Corridor\02.Tasks\01.Cargo_Flow\01.Input_Data\01.USACE\02.Foreign_Cargo_Import_Export\Raw_Data\2021\f6c7bae8-55f2-4ecb-b610-40f8e90d9631___Imports_Exports-2021.xlsx",
    }

# =============================================================================
# sheetname_import_by_year
# =============================================================================
sheetname_import_by_year = {
    2017:"Imports2017",
    2018:"Import-2018",
    2019:"Imports2019",
    2020:"Import",
    2021:"Imports-2021",
    }

# =============================================================================
# sheetname_export_by_year
# =============================================================================
sheetname_export_by_year = {
    2017:"Exports2017",
    2018:"Export-2018",
    2019:"Exports2019",
    2020:"Export",
    2021:"Exports_2021",
    }

# =============================================================================
# column_rename
# =============================================================================
column_rename = {"Year":"YEAR"}
# column_rename = {}


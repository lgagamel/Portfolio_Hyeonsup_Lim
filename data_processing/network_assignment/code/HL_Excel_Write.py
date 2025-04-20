import xlsxwriter

# =============================================================================
# Main function to write Excel file
# =============================================================================
def write_Excel(df,grp_list,measure_columns,excel_location):
    workbook = xlsxwriter.Workbook(excel_location)
    for i,grp in enumerate(grp_list):
        sht_name = str(i).zfill(2) + "." + '_'.join(grp)
        df_out = df.groupby(grp,as_index=False)[measure_columns].sum()
        df_out = df_out.fillna(0)
        write_Excel_lines(df_out, workbook, grp, sht_name)        
    workbook.close()

# =============================================================================
# Sub-function to wrtie Excel file
# =============================================================================
def write_Excel_lines(df_out, workbook, grp, grp_name):
    grp_name = grp_name[:31]
    # formats used in excel
    title_text = workbook.add_format({'bold': True, 'font_color':'white', 'bg_color':'#006d2c', 'border':3})        
    title_num = workbook.add_format({'bold': True, 'font_color':'white', 'bg_color':'#252525', 'border':3})
    title_pct = workbook.add_format({'bold': True, 'font_color':'white', 'bg_color':'#252525', 'border':3})
    body_text = workbook.add_format({'font_color':'black','bg_color':'#edf8e9', 'border':1})
    body_num = workbook.add_format({'font_color':'black', 'num_format':'#,##0','bg_color':'#f7f7f7', 'border':1})
    body_pct = workbook.add_format({'font_color':'black', 'num_format':'0.0%','bg_color':'#cccccc', 'border':1})
    
    worksheet = workbook.add_worksheet(grp_name)
    worksheet.set_column(0, len(grp)-1, 13)
    worksheet.set_column(len(grp), len(df_out.columns), 12)
    row_ = 0
    for j in range(len(df_out.columns)):
        if j <len(grp):
                temp_format = title_text
        else:
            if '%' in df_out.columns[j]:
                worksheet.set_column(j, j, 10)
                temp_format = title_pct
            else:
                temp_format = title_num            
        worksheet.write(row_, j, df_out.columns[j], temp_format)
    for i in range(len(df_out)):
        row_ = row_ + 1
        for j in range(len(df_out.columns)):
            if j <len(grp):
                temp_format = body_text
            else:
                if '%' in df_out.columns[j]:
                    temp_format = body_pct
                else:
                    temp_format = body_num
            worksheet.write(row_, j, df_out.iloc[i,j], temp_format)

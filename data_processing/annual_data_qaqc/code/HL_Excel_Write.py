import xlsxwriter
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import rgb2hex

# =============================================================================
# test for colormap
# =============================================================================
# cmap = plt.get_cmap('RdBu')
# norm = plt.Normalize(-100, 100)
# color1 = cmap(norm(-100))
# color2 = cmap(norm(0))
# color3 = cmap(norm(100))

# print(rgb2hex(color1))
# print(rgb2hex(color2))
# print(rgb2hex(color3))


# =============================================================================
# Main function to write Excel file
# =============================================================================
def write_excel(df_list,grp_list,outputfile_loc,sheet_name_list=[]):
    workbook = xlsxwriter.Workbook(outputfile_loc)
    for i,df in enumerate(df_list):
        if len(df)>0:
            grp = grp_list[i]
            if len(sheet_name_list)>0:
                sheet_name = sheet_name_list[i]
            else:
                sheet_name = str(i+1).zfill(3) + "." + '-'.join(grp)
            sheet_name = sheet_name[:31]
            write_sheet(df, workbook, grp, sheet_name)        
    workbook.close()

# =============================================================================
# Sub-function to wrtie Excel file
# =============================================================================
def write_sheet(df, workbook, grp, sheet_name):
    # colormap for pct
    cmap = plt.get_cmap('RdBu')
    pct_norm = plt.Normalize(-1, 1)
    
    # formats used in excel
    title_format = {"base":{'font_color':'white','border':3,'bold': True},
                   "text":{"bg_color":"#006d2c","num_format":""},
                   "num":{"bg_color":"#252525","num_format":"#,##0"},
                   "v2w":{"bg_color":"#252525","num_format":"#,##0.000"},
                   "pct":{"bg_color":"#525252","num_format":"0.0%"},
                   "dif":{"bg_color":"#737373","num_format":"#,##0"},
                   }
    
    body_format = {"base":{'font_color':'black','border':1},
                   "text":{"bg_color":"#edf8e9","num_format":""},
                   "num":{"bg_color":"#ffffff","num_format":"#,##0"},
                   "v2w":{"bg_color":"#ffffff","num_format":"#,##0.000"},
                   "pct":{"bg_color":"#bdbdbd","num_format":"0.0%"},
                   "dif":{"bg_color":"#f0f0f0","num_format":"#,##0"},
                   }
    
    bg_color_flagged = "#fee0d2"
    worksheet = workbook.add_worksheet(sheet_name)
    worksheet.set_column(0, len(grp)-1, 13)
    worksheet.set_column(len(grp), len(df.columns), 12)
    
    row_ = 0
    
    # first row - field names
    for j in range(len(df.columns)):
        temp_format = workbook.add_format(title_format["base"])
        if j <len(grp):
            value_type = "text"
        else:
            if '%' in df.columns[j]:
                value_type = "pct"
            elif 'v2w' in df.columns[j]:
                value_type = "v2w"
            elif "dif" in df.columns[j]:
                value_type = "dif"
            else:
                value_type = "num"
        temp_format.set_bg_color(title_format[value_type]["bg_color"])
        temp_format.set_num_format(title_format[value_type]["num_format"])
        worksheet.write(row_, j, df.columns[j], temp_format)
    
    # from second row - data
    for i in range(len(df)):
        row_ = row_ + 1
        # flagged = df.iloc[i]["flag_any"]
        for j in range(len(df.columns)):
            temp_format = workbook.add_format(body_format["base"])
            if j <len(grp):
                value_type = "text"
            else:
                if '%' in df.columns[j]:
                    value_type = "pct"
                elif 'v2w' in df.columns[j]:
                    value_type = "v2w"
                elif "dif" in df.columns[j]:
                    value_type = "dif"
                else:
                    value_type = "num"
            temp_format.set_bg_color(body_format[value_type]["bg_color"])
            temp_format.set_num_format(body_format[value_type]["num_format"])
            # if flagged:
            #     temp_format.set_bg_color(bg_color_flagged)

            value = df.iloc[i,j]            
            if type(value)!=str:                
                if np.isinf(value):
                    value = "Inf"
                elif np.isnan(value):
                    value = "N/A"
            
            # change color by pct
            if ('%' in df.columns[j]):
                try:
                    tmp_color = rgb2hex(cmap(pct_norm(value*1)))
                except:
                    tmp_color = "orange"
                temp_format.set_bg_color(tmp_color)
            
            # change color by flag
            if ('flag' in df.columns[j]):
                if value:
                    tmp_color = bg_color_flagged
                    temp_format.set_bg_color(tmp_color)
                
            worksheet.write(row_, j, value, temp_format)

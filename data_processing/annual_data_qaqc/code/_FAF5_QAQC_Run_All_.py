import os

python_list = [
    "00_create_folders",
    "01_data_format_check",
    "02_trend_over_years",
    "03_changes_from_previous_version",
    "04_v2w_over_years",
    "05_change_of_shares",
    "99_summary",
    ]

for pfile in python_list:
    print(pfile)
    os.system("python " + pfile + ".py")
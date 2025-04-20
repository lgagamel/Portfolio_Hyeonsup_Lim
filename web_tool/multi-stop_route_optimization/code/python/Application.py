import win32com.client as win32
import os
import pandas as pd


def send_email(curr_Email):
    print("curr_Email",curr_Email)
    outlook = win32.Dispatch('outlook.application')
    mail = outlook.CreateItem(0)
    mail.Subject = '[Route.BongBong.Store] Your Optimal Route'
    mail.To = curr_Email
    # mail.Recipients.Add("hslim8211@gmail.com").Type = 3
    f = open("output/04/final.txt","r")
    body_txt = "Please use the below links to use the optimal route."
    for i,txt in enumerate(f):        
        tmp_txt = "<li><a href='"+txt+"'>Route "+str(i+1)+"</a></li>"
        body_txt = body_txt + tmp_txt
    f.close()
    
    df_null_xy = pd.read_csv("output/01/xy_null.csv",dtype=str)
    null_address_list =list(df_null_xy["address"])
    if len(null_address_list)>0:
        body_txt = body_txt + "<br>We could not find geo coordinates (lat/lon) of the following addresses. We highly recommend you try it again by using exact lat/lon for those locations."
        for null_address in null_address_list:
            if len(null_address)>0:
                tmp_txt = "<li>"+null_address+"</li>"
                body_txt = body_txt + tmp_txt
    
    body_txt = body_txt + "<br>Note that this is an automatically generated message. Please do not reply."
    body_txt = body_txt + "<br>Thank you."
    body_txt = body_txt + "<br><a href='Route.BongBong.store'>Route.BongBong.store</a>"
    
    mail.HTMLBody = body_txt
    mail.Attachments.Add(os.getcwd() + "\\output\\05\\suggested_route.pdf")
    mail.Send()
    return "success"
    

def send_email_failed(curr_Email):
    try:
        print("curr_Email",curr_Email)
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = '[Route.BongBong.Store] Your Optimal Route'
        mail.To = curr_Email
        
        body_txt = "We are so sorry. Something went wrong during the process."
        body_txt = body_txt + "<br>We highly recommend you try it again by using exact lat/lon for those locations."
        
        body_txt = body_txt + "<br><br>Note that this is an automatically generated message. Please do not reply."
        body_txt = body_txt + "<br>Thank you."
        body_txt = body_txt + "<br><a href='Route.BongBong.store'>Route.BongBong.store</a>"
        
        mail.HTMLBody = body_txt    
        mail.Send()        
    except:
        pass
    return "fail"

def send_email_too_many(curr_Email, n_limit):
    try:
        print("curr_Email",curr_Email)
        outlook = win32.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.Subject = '[Route.BongBong.Store] Your Optimal Route'
        mail.To = curr_Email
        
        body_txt = "We are so sorry. We are currently accepting up to " + str(n_limit) +" locations."
        body_txt = body_txt + "<br>You can try with less number of locations."
        body_txt = body_txt + "<br>Also, we highly recommend you try it again by using exact lat/lon for those locations."
        
        body_txt = body_txt + "<br><br>Note that this is an automatically generated message. Please do not reply."
        body_txt = body_txt + "<br>Thank you."
        body_txt = body_txt + "<br><a href='Route.BongBong.store'>Route.BongBong.store</a>"
        
        mail.HTMLBody = body_txt    
        mail.Send()        
    except:
        pass
    return "fail"

def run_application(inputfileloc, curr_Email):
    python_list = [   
        # "00_Initiate_Output_Folders",
        "01_Get_Coordinate",
        "02_Update_Graph",
        "03_Calculate_Distance",
        "04_Run_TSP",
        "05_Output",
        # "99_summary",
        ]

    for pfile in python_list:
        print(pfile)
        os.system("python " + pfile + ".py " + inputfileloc)
    
    
        
    try:
        completed = send_email(curr_Email)
    except:
        completed = send_email_failed(curr_Email)
    
    with open("output/05/completed.txt","w") as f:
        f.write(completed)
    return completed

# run_application("input/address.txt")
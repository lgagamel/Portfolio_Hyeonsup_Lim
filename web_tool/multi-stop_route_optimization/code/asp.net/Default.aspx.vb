Imports System.IO

Public Class _Default
    Inherits Page

    Protected Sub Page_Load(ByVal sender As Object, ByVal e As EventArgs) Handles Me.Load
        'Session("API") = Request.QueryString
        'Session("SN") = Session("API")("SN")
        'Session("Request_ID") = Session("API")("Request_ID")
        'Session("Email") = Session("API")("Email")
        'Session("Request_Folder") = Server.MapPath("Data/User_Request/" + Session("Request_ID")).ToString()
        'Session("Initiated") = Session("API")("Initiated")
        'Session("Completed") = Session("API")("Completed")
        'Session("Clear_Queue") = Session("API")("Clear_Queue")
        'Session("Input") = Session("API")("Input")

        'If Session("Clear_Queue") = "True" Then
        '    Clear_Queue()
        'End If

        'If Len(Session("Input")) > 0 Then
        '    Dim inputfileloc As String = Server.MapPath("Data/Pre_Input/" + Session("Input") + ".txt").ToString()
        '    Dim input_text As String = File.ReadAllText(inputfileloc)
        '    TextBox_User_Input.Text = input_text
        'Else
        '    ScriptManager.RegisterStartupScript(Me, Page.GetType, "Script", "load_TextBox_Default();", True)
        'End If

        'If Len(Session("Initiated")) > 0 And Len(Session("Request_ID")) > 0 Then
        '    Write_Initiated()
        'End If

        'If Len(Session("Completed")) > 0 And Len(Session("Request_ID")) > 0 Then
        '    Write_Completed()
        '    Update_Queue()
        'End If
    End Sub

    'Protected Sub Clear_Queue()
    '    Dim queuefileloc As String = Server.MapPath("Data/User_Request/__queue__" + Session("SN") + ".txt").ToString()
    '    Dim sw As IO.StreamWriter = New IO.StreamWriter(queuefileloc, False)
    '    sw.Write("")
    '    sw.Close()
    'End Sub

    'Protected Sub Write_Initiated()
    '    Dim inputfileloc As String = Session("Request_Folder") + "\__initiated__.txt"
    '    Dim sw As IO.StreamWriter = New IO.StreamWriter(inputfileloc, False)
    '    sw.Write(Session("Initiated") & vbCrLf)
    '    sw.Close()
    'End Sub

    'Protected Sub Write_Completed()
    '    Dim inputfileloc As String = Session("Request_Folder") + "\__completed__.txt"
    '    Dim sw As IO.StreamWriter = New IO.StreamWriter(inputfileloc, False)
    '    sw.Write(Session("Completed") & vbCrLf)
    '    sw.Close()
    'End Sub

    'Protected Sub User_Request_Click()
    'End Sub

    'Protected Sub Run_All()
    '    Dim items() As String = TextBox_User_Input.Text.Split(New String() {Environment.NewLine}, StringSplitOptions.None)
    '    Dim n As Integer = 0
    '    For Each x In items
    '        If x.Length > 3 Then
    '            n = n + 1
    '        End If
    '    Next

    '    If n >= 2 Then
    '        Random_Key_Generation()
    '        Create_Request_Folder()
    '        Select_SN()
    '        Log_Queue()
    '        Message_Update()
    '        ScriptManager.RegisterStartupScript(Me, Page.GetType, "Script", "hide_busy();", True)
    '    Else
    '        Message_Update_too_small_input()

    '    End If
    'End Sub




    'Protected Sub Random_Key_Generation()
    '    Dim s As String = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    '    Dim r As New Random
    '    Dim sb As New StringBuilder
    '    For i As Integer = 1 To 20
    '        Dim idx As Integer = r.Next(0, 35)
    '        sb.Append(s.Substring(idx, 1))
    '    Next
    '    Session("Request_ID") = sb.ToString
    'End Sub

    'Protected Sub Create_Request_Folder()
    '    Session("Request_Folder") = Server.MapPath("Data/User_Request/" + Session("Request_ID")).ToString()
    '    If Not Directory.Exists(Session("Request_Folder")) Then
    '        Directory.CreateDirectory(Session("Request_Folder"))
    '    End If

    '    Dim inputfileloc As String = Session("Request_Folder") + "\Input.txt"
    '    Dim sw As IO.StreamWriter = New IO.StreamWriter(inputfileloc, False)
    '    sw.Write(TextBox_User_Input.Text & vbCrLf)
    '    sw.Close()

    '    inputfileloc = Session("Request_Folder") + "\CheckBox_Open_TSP.txt"
    '    sw = New IO.StreamWriter(inputfileloc, False)
    '    sw.Write(CheckBox_Open_TSP.Checked)
    '    sw.Close()
    'End Sub

    'Protected Sub Select_SN()
    '    Dim best_SN As String = 1
    '    Dim min_count As Integer = 100000

    '    Dim queuefileloc As String
    '    Dim lines() As String

    '    For i As Integer = 1 To 3
    '        queuefileloc = Server.MapPath("Data/User_Request/__queue__" + CStr(i) + ".txt").ToString()
    '        lines = IO.File.ReadAllLines(queuefileloc)
    '        If min_count > lines.Count Then
    '            min_count = lines.Count
    '            best_SN = i
    '        End If
    '    Next
    '    Session("SN") = CStr(best_SN)
    'End Sub

    'Protected Sub Log_Queue()
    '    Dim queuefileloc As String = Server.MapPath("Data/User_Request/__queue__" + Session("SN") + ".txt").ToString()
    '    Dim sw As IO.StreamWriter = New IO.StreamWriter(queuefileloc, True)
    '    Dim line As String = Session("Request_ID") + "," + TextBox_Email.Text
    '    sw.Write(line & vbCrLf)
    '    sw.Close()
    'End Sub

    'Protected Sub Check_Initiated()
    '    Session("Initiated") = False
    '    Dim i As Integer = 1
    '    Do While ((Session("Initiated") = False) And (i < 60))
    '        If File.Exists(Session("Request_Folder") + "\__initiated__.txt") Then
    '            Session("Initiated") = True
    '        End If
    '        Threading.Thread.Sleep(1000)
    '        i = i + 1
    '    Loop
    'End Sub

    'Protected Sub Update_Queue()
    '    Dim queuefileloc As String = Server.MapPath("Data/User_Request/__queue__" + Session("SN") + ".txt").ToString()
    '    Dim lines As New List(Of String)(IO.File.ReadLines(queuefileloc))
    '    lines.Remove(Session("Request_ID") + "," + Session("Email"))
    '    IO.File.WriteAllLines(queuefileloc, lines.ToArray())
    'End Sub

    'Protected Sub Check_Completed()
    '    Session("Completed") = False
    '    Dim i As Integer = 1
    '    Do While ((Session("Completed") = False) And (i < 60))
    '        If File.Exists(Session("Request_Folder") + "\__completed__.txt") Then
    '            Session("Completed") = True
    '        End If
    '        Threading.Thread.Sleep(1000)
    '        i = i + 1
    '    Loop
    'End Sub

    'Protected Sub Message_Update()
    '    Label_Message_Update.Text = "<b>Our optimal route tool is processing your request. You should get an email shortly once the process is done.</b>"
    'End Sub

    'Protected Sub Message_Update_too_small_input()
    '    Label_Message_Update.Text = "<b>There should be at least two valid coordinates and/or addresses separated by lines.</b>"
    'End Sub

    'Protected Sub Disable_Click()
    '    Button_Run_All.Enabled = False
    'End Sub
End Class
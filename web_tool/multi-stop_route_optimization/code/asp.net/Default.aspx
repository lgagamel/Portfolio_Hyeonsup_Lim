<%@ Page Title="Home Page" Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="Default.aspx.vb" Inherits="Route.BongBong.Store._Default" %>


<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">   
    
    <h1>We are currently working to improve our solution. Will come back shortly. Thank you!</h1>
    <%--<div class="w3-container w3-center w3-margin-top">
        <h1>Lat/Lon Coordinates (Recommended) or Addresses (US Only)</h1>
        <div class="w3-cell-row">
            This is an example. Please replace it with your input coordinates (recommended) or addresses here. The first location must be where you want to start and end.
        </div>
        <asp:TextBox ID="TextBox_User_Input" runat="server" CssClass="content" MaxLength="3000" Rows="20" TextMode="MultiLine" Width="100%" onfocus="TextBox_User_Input_onfocus()" onblur="TextBox_User_Input_onblur();" ToolTip="This is an example. Please replace it with your input coordinates (recommended) or addresses here. The first location must be where you want to start and end."></asp:TextBox>
        <asp:CheckBox ID="CheckBox_Open_TSP" runat="server" CssClass="w3-check" Text="&nbsp;&nbsp;must come back to the first location?" Checked="true" />

    </div>
    <div class="w3-container w3-center w3-margin-top">
        <h1>Your Email</h1>
        <asp:TextBox ID="TextBox_Email" runat="server" Width="50%" TextMode="Email" onfocus="TextBox_Email_onfocus();" onblur="TextBox_Email_onblur();">Please type your email here.</asp:TextBox>
    </div>

    <div class="w3-container w3-center">
        <br />
        <asp:Button ID="Button_Run_All" runat="server" CssClass="w3-button w3-teal w3-round-large" Text="Get Optimal Routes" OnClick="Run_All" Style="font-size: large" Width="50%" />
    </div>

    <div class="w3-container w3-center">
        <asp:Label ID="Label_Message_Update" Text="" runat="server"></asp:Label>
        <div id="busy" class="w3-center" style="margin-top: 150px; margin-bottom: 20px; display: none;">
            <i class="w3-xxxlarge glyphicon glyphicon-refresh w3-spin"></i>
        </div>
    </div>

    <script>
        var TextBox_User_Input_Default = "34.02312, -118.24276\n34.00642, -118.15158\n33.93707, -118.11762\n33.94678, -118.25119\n3040 Slauson Ave, Huntington Park, CA 90255";
        var TextBox_Email_Default = "Please type your email here.";
        function show_busy() {
            document.getElementById("busy").style.display = "block";
        };

        function hide_busy() {
            document.getElementById("busy").style.display = "none";
        }

        function TextBox_User_Input_onfocus() {
            document.getElementById('<%= Label_Message_Update.ClientID %>').innerText = "";
            if (document.getElementById('<%= TextBox_User_Input.ClientID %>').value == TextBox_User_Input_Default) {
                document.getElementById('<%= TextBox_User_Input.ClientID %>').value = "";
            }
        }

        function TextBox_User_Input_onblur() {
            if (document.getElementById('<%= TextBox_User_Input.ClientID %>').value.length == 0) {
                document.getElementById('<%= TextBox_User_Input.ClientID %>').value = TextBox_User_Input_Default;
            }
        }

        function TextBox_Email_onfocus() {
            document.getElementById('<%= Label_Message_Update.ClientID %>').innerText = "";
            if (document.getElementById('<%= TextBox_Email.ClientID %>').value == TextBox_Email_Default) {
                document.getElementById('<%= TextBox_Email.ClientID %>').value = "";
            }
        }

        function TextBox_Email_onblur() {
            if (document.getElementById('<%= TextBox_Email.ClientID %>').value.length == 0) {
        document.getElementById('<%= TextBox_Email.ClientID %>').value = TextBox_Email_Default;
            }
        }

        function load_TextBox_Default() {
            document.getElementById('<%= TextBox_User_Input.ClientID %>').value = TextBox_User_Input_Default;
            document.getElementById('<%= TextBox_Email.ClientID %>').value = TextBox_Email_Default;
            if (localStorage.getItem("hasCodeRunBefore") === null) {
                
                localStorage.setItem("hasCodeRunBefore", true);
            }
        }
    </script>--%>

</asp:Content>



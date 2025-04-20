<%@ Page Title="About" Language="VB" MasterPageFile="~/Site.Master" AutoEventWireup="true" CodeBehind="About.aspx.vb" Inherits="Route.BongBong.Store.About" %>

<asp:Content ID="BodyContent" ContentPlaceHolderID="MainContent" runat="server">
    <h2><%: Title %>.</h2>
    <p>Your app description page.</p>
    <p>Use this area to provide additional information.</p>    
    <a runat="server" href="~/?Input=Input1" class="w3-bar-item w3-button">Input1</a>
    <a runat="server" href="~/?Input=Input2" class="w3-bar-item w3-button">Input2</a>
</asp:Content>

#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: TvLuserland.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxWindows' modules
from wxPython.wx import *

# Custom source
from ClickableText import *


# Window functions

ID_TEXT = 10000
ID_POSTTITLE = 10001
ID_POSTLINK = 10002
ID_BROWSE = 10003
ID_POSTTEXT = 10004
ID_TEX = 10005
ID_POSTINGTEXT = 10006
ID_POSTINGGAUGE = 10007
wxID_POST = 10008

def EditPostFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxBoxSizer( wxHORIZONTAL )
    parent.previewsizer = item1
    
    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item2 = wxFlexGridSizer( 0, 2, 0, 0 )
    item2.AddGrowableCol( 1 )
    item2.AddGrowableRow( 2 )
    
    item3 = wxStaticText( parent, ID_TEXT, "Title", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item4 = wxTextCtrl( parent, ID_POSTTITLE, "", wxDefaultPosition, wxSize(300,-1), 0 )
    item2.AddWindow( item4, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item5 = wxStaticText( parent, ID_TEXT, "Link", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxBoxSizer( wxHORIZONTAL )
    
    item7 = wxTextCtrl( parent, ID_POSTLINK, "", wxDefaultPosition, wxSize(300,-1), 0 )
    item6.AddWindow( item7, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item8 = wxButton( parent, ID_BROWSE, "GO", wxDefaultPosition, wxSize(40,-1), 0 )
    item6.AddWindow( item8, 0, wxALIGN_CENTRE|wxALL, 5 )

    item2.AddSizer( item6, 0, wxGROW|wxALIGN_CENTER_VERTICAL, 5 )

    item9 = wxStaticText( parent, ID_TEXT, "Text", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item9, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item10 = wxTextCtrl( parent, ID_POSTTEXT, "", wxDefaultPosition, wxSize(300,-1), wxTE_MULTILINE|wxTE_RICH )
    item2.AddWindow( item10, 0, wxGROW|wxALL, 5 )

    item11 = wxStaticText( parent, ID_TEX, "Categories", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item11, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item12 = wxFlexGridSizer( 0, 4, 0, 0 )
    item12.AddGrowableCol( 0 )
    item12.AddGrowableCol( 1 )
    item12.AddGrowableCol( 2 )
    item12.AddGrowableCol( 3 )
    parent.catsizer = item12
    
    item2.AddSizer( item12, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item2, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item13 = wxBoxSizer( wxHORIZONTAL )
    
    item14 = wxStaticText( parent, ID_POSTINGTEXT, "", wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT )
    item13.AddWindow( item14, 0, wxALIGN_CENTRE|wxALL, 5 )

    item15 = wxGauge( parent, ID_POSTINGGAUGE, 100, wxDefaultPosition, wxSize(100,-1), 0 )
    item15.Enable(false)
    item13.AddWindow( item15, 0, wxALIGN_CENTRE|wxALL, 5 )

    item13.AddSpacer( 20, 20, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item16 = wxButton( parent, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item16, 0, wxALIGN_CENTRE|wxALL, 5 )

    item17 = wxButton( parent, wxID_POST, "Post", wxDefaultPosition, wxDefaultSize, 0 )
    item17.SetDefault()
    item13.AddWindow( item17, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item13, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item0.AddSpacer( 10, 10, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_SERVICELIST = 10009
ID_NEWSERVICE = 10010
ID_NEWPOST = 10011
ID_REFRESH = 10012
ID_NEWSPANE = 10013

def ReadNewsFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxHORIZONTAL )
    
    item1 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxBoxSizer( wxHORIZONTAL )
    
    item3 = wxButton( parent, ID_SERVICELIST, "Service List", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item4 = wxButton( parent, ID_NEWSERVICE, "New Service", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

    item5 = wxButton( parent, ID_NEWPOST, "New Post", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxButton( parent, ID_REFRESH, "Refresh", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

    item1.AddSizer( item2, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item7 = parent.newspane
    item1.AddWindow( item7, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_SOURCE = 10014
ID_HTML = 10015
ID_KILL = 10016
ID_POST = 10017
ID_EDIT = 10018

def NewsItemFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxHORIZONTAL )
    
    item1 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxClickableText( parent, ID_SOURCE, "source", wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT )
    item2.SetFont( wxFont( 10, wxSWISS, wxNORMAL, wxNORMAL ) )
    item1.AddWindow( item2, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL, 5 )

    item3 = wxBoxSizer( wxHORIZONTAL )
    parent.itemsizer = item3
    
    item4 = parent.html
    item3.AddWindow( item4, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL, 15 )

    item5 = wxBoxSizer( wxVERTICAL )
    
    item6 = wxButton( parent, ID_KILL, "Kill", wxDefaultPosition, wxDefaultSize, 0 )
    item5.AddWindow( item6, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item7 = wxButton( parent, ID_POST, "Post", wxDefaultPosition, wxDefaultSize, 0 )
    item5.AddWindow( item7, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item8 = wxButton( parent, ID_EDIT, "Edit", wxDefaultPosition, wxDefaultSize, 0 )
    item5.AddWindow( item8, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item3.AddSizer( item5, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 0 )

    item1.AddSizer( item3, 0, wxALIGN_CENTRE|wxALL, 0 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CONFIGWEBLOG = 10019
wxID_Cancel = 5101
wxID_Ok = 5100

def ConfigFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxNotebook( parent, ID_CONFIGWEBLOG, wxDefaultPosition, wxSize(400,300), 0 )
    item1 = wxNotebookSizer( item2 )

    item3 = wxPanel( item2, -1 )
    ConfigWeblogFunc( item3, false )
    item2.AddPage( item3, "Weblog/XML-RPC" )

    item4 = wxPanel( item2, -1 )
    ConfigUiFunc( item4, false )
    item2.AddPage( item4, "User Interface" )

    item5 = wxPanel( item2, -1 )
    ConfigNetworkFunc( item5, false )
    item2.AddPage( item5, "Network" )

    item6 = wxPanel( item2, -1 )
    ConfigFsFunc( item6, false )
    item2.AddPage( item6, "Files" )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    item7 = wxBoxSizer( wxHORIZONTAL )
    
    item8 = wxButton( parent, wxID_Cancel, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
    item7.AddWindow( item8, 0, wxALIGN_CENTRE|wxALL, 5 )

    item9 = wxButton( parent, wxID_Ok, "OK", wxDefaultPosition, wxDefaultSize, 0 )
    item7.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item7, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CWLOGSERVER = 10020
ID_CWLOGUSER = 10021
ID_CWLOGPASSWORD = 10022
ID_CWLOGMETAAPI = 10023
ID_CWLOGSETDATE = 10024
ID_CWLOGAGGREGATOR = 10025
ID_CWLOGDEBUG = 10026
ID_CWLOGAUTODETECT = 10027

def ConfigWeblogFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item2 = wxStaticText( parent, ID_TEXT, "Server", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item2, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item3 = wxTextCtrl( parent, ID_CWLOGSERVER, "", wxDefaultPosition, wxSize(200,-1), 0 )
    item1.AddWindow( item3, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item4 = wxStaticText( parent, ID_TEXT, "Username", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item4, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item5 = wxTextCtrl( parent, ID_CWLOGUSER, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item1.AddWindow( item5, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item6 = wxStaticText( parent, ID_TEXT, "Password", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item6, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item7 = wxTextCtrl( parent, ID_CWLOGPASSWORD, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item1.AddWindow( item7, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item8 = wxStaticText( parent, ID_TEXT, "Supported API Features", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item8, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item9 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item10 = wxCheckBox( parent, ID_CWLOGMETAAPI, "metaWeblog API", wxDefaultPosition, wxDefaultSize, 0 )
    item10.SetValue(true)
    item9.AddWindow( item10, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item11 = wxCheckBox( parent, ID_CWLOGSETDATE, "SetDate", wxDefaultPosition, wxDefaultSize, 0 )
    item9.AddWindow( item11, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item12 = wxCheckBox( parent, ID_CWLOGAGGREGATOR, "aggregator API", wxDefaultPosition, wxDefaultSize, 0 )
    item9.AddWindow( item12, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item13 = wxCheckBox( parent, ID_CWLOGDEBUG, "XML-RPC debugging", wxDefaultPosition, wxDefaultSize, 0 )
    item9.AddWindow( item13, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item9.AddSpacer( 20, 20, 0, wxALIGN_CENTRE|wxALL, 5 )

    item14 = wxButton( parent, ID_CWLOGAUTODETECT, "Autodetect", wxDefaultPosition, wxDefaultSize, 0 )
    item14.SetToolTip( wxToolTip("Autodetect The Servers Capabilities") )
    item9.AddWindow( item14, 0, wxALIGN_CENTRE|wxALL, 5 )

    item1.AddSizer( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CUIITEMS = 10028
ID_CUIDELAFTERPOST = 10029
ID_CUIAUTOPREVIEW = 10030

def ConfigUiFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item2 = wxStaticText( parent, ID_TEXT, "items on newspage", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item2, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item3 = wxSpinCtrl( parent, ID_CUIITEMS, "23", wxDefaultPosition, wxSize(100,-1), wxSP_ARROW_KEYS|wxSP_WRAP, 1, 1000, 23 )
    item1.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item4 = wxStaticText( parent, ID_TEXT, "misc. options", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item4, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item5 = wxCheckBox( parent, ID_CUIDELAFTERPOST, "delete item after posting", wxDefaultPosition, wxDefaultSize, 0 )
    item5.SetValue(true)
    item1.AddWindow( item5, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item1.AddSpacer( 20, 20, 0, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxCheckBox( parent, ID_CUIAUTOPREVIEW, "automatic preview", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item6, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CNETTIMEOUT = 10031

def ConfigNetworkFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item2 = wxStaticText( parent, ID_TEXT, "Timeout", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxSpinCtrl( parent, ID_CNETTIMEOUT, "0", wxDefaultPosition, wxSize(100,-1), wxSP_WRAP, 0, 3600, 0 )
    item1.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CFSDBDIR = 10032

def ConfigFsFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item2 = wxStaticText( parent, ID_TEXT, "database directory", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxTextCtrl( parent, ID_CFSDBDIR, "", wxDefaultPosition, wxSize(160,-1), 0 )
    item1.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_LASTREQUEST = 10033
ID_LASTNEWITEM = 10034
ID_ITEMSFETCHED = 10035
ID_UNREADITEMS = 10036
ID_LINE = 10037
ID_ERRORS = 10038
ID_LASTERROR = 10039
ID_LASTERRORTEXT = 10040
ID_TITLE = 10041
ID_LINK = 10042
ID_CHANNELINFO = 10043
ID_PUBLICNAME = 10044
ID_PRIVATENAME = 10045
ID_PUBLICLINK = 10046
ID_HOWOFTEN = 10047
ID_CHECKFORREDIRECTED = 10048
ID_FIXUMLAUTS = 10049
ID_EXTRACTLTD = 10050
ID_REMOVEMARKUP = 10051
ID_KILLITEMS = 10052
ID_REMOVESERVICE = 10053

def ServiceDialogFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxStaticBox( parent, -1, "Information about Aggregation" )
    item1 = wxStaticBoxSizer( item2, wxVERTICAL )
    
    item3 = wxBoxSizer( wxHORIZONTAL )
    
    item4 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item5 = wxStaticText( parent, ID_TEXT, "Last Request", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item5, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item6 = wxStaticText( parent, ID_LASTREQUEST, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item6, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item7 = wxStaticText( parent, ID_TEXT, "Last new Item", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item7, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item8 = wxStaticText( parent, ID_LASTNEWITEM, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item8, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item9 = wxStaticText( parent, ID_TEXT, "Items fetched", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item9, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item10 = wxStaticText( parent, ID_ITEMSFETCHED, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item10, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item11 = wxStaticText( parent, ID_TEXT, "Unread Items", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item11, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item12 = wxStaticText( parent, ID_UNREADITEMS, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item12, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item3.AddSizer( item4, 0, wxALL, 5 )

    item13 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(-1,20), wxLI_VERTICAL )
    item3.AddWindow( item13, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item14 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item15 = wxStaticText( parent, ID_TEXT, "Errors", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item15, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item16 = wxStaticText( parent, ID_ERRORS, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item16, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item17 = wxStaticText( parent, ID_TEXT, "Last Error", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item17, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item18 = wxStaticText( parent, ID_LASTERROR, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item18, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item19 = wxStaticText( parent, ID_TEXT, "Last Error Text", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item19, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item20 = wxStaticText( parent, ID_LASTERRORTEXT, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item14.AddWindow( item20, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item3.AddSizer( item14, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item1.AddSizer( item3, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item22 = wxStaticBox( parent, -1, "Information provided by the Service" )
    item21 = wxStaticBoxSizer( item22, wxVERTICAL )
    parent.rsssizer = item21
    
    item23 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item24 = wxStaticText( parent, ID_TEXT, "Title", wxDefaultPosition, wxDefaultSize, 0 )
    item23.AddWindow( item24, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item25 = wxStaticText( parent, ID_TITLE, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item23.AddWindow( item25, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item26 = wxStaticText( parent, ID_TEXT, "Link", wxDefaultPosition, wxDefaultSize, 0 )
    item23.AddWindow( item26, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item27 = wxLinkText( parent, ID_LINK, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item23.AddWindow( item27, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item21.AddSizer( item23, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item28 = wxTextCtrl( parent, ID_CHANNELINFO, "", wxDefaultPosition, wxSize(180,100), wxTE_MULTILINE )
    item21.AddWindow( item28, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item21, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item29 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item29, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item30 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item31 = wxStaticText( parent, ID_TEXT, "Public Name", wxDefaultPosition, wxDefaultSize, 0 )
    item30.AddWindow( item31, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item32 = wxTextCtrl( parent, ID_PUBLICNAME, "", wxDefaultPosition, wxSize(180,-1), 0 )
    item30.AddWindow( item32, 0, wxGROW|wxLEFT|wxRIGHT|wxTOP, 5 )

    item33 = wxStaticText( parent, ID_TEXT, "Private Name", wxDefaultPosition, wxDefaultSize, 0 )
    item30.AddWindow( item33, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item34 = wxTextCtrl( parent, ID_PRIVATENAME, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item30.AddWindow( item34, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item35 = wxStaticText( parent, ID_TEXT, "Public Link", wxDefaultPosition, wxDefaultSize, 0 )
    item30.AddWindow( item35, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item36 = wxTextCtrl( parent, ID_PUBLICLINK, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item30.AddWindow( item36, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item37 = wxStaticText( parent, ID_TEXT, "Fetch how often", wxDefaultPosition, wxDefaultSize, 0 )
    item30.AddWindow( item37, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item38 = wxChoice( parent, ID_HOWOFTEN, wxDefaultPosition, wxSize(100,-1), 
        ["30m","1h","2h","3h ","4h","5h","6h","8h","12h","18h","24h","48h","72h"] , 0 )
    item30.AddWindow( item38, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item39 = wxStaticText( parent, ID_TEXT, "Options", wxDefaultPosition, wxDefaultSize, 0 )
    item30.AddWindow( item39, 0, wxALL, 5 )

    item40 = wxFlexGridSizer( 0, 2, 0, 0 )
    item40.AddGrowableCol( 0 )
    item40.AddGrowableCol( 1 )
    
    item41 = wxCheckBox( parent, ID_CHECKFORREDIRECTED, "Check for redirected URLs", wxDefaultPosition, wxDefaultSize, 0 )
    item40.AddWindow( item41, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item42 = wxCheckBox( parent, ID_FIXUMLAUTS, "Fix �ml�uts", wxDefaultPosition, wxDefaultSize, 0 )
    item40.AddWindow( item42, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item43 = wxCheckBox( parent, ID_EXTRACTLTD, "Extract Link and Title from Description", wxDefaultPosition, wxDefaultSize, 0 )
    item40.AddWindow( item43, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxBOTTOM, 5 )

    item44 = wxCheckBox( parent, ID_REMOVEMARKUP, "Remove Markup", wxDefaultPosition, wxDefaultSize, 0 )
    item40.AddWindow( item44, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxBOTTOM, 5 )

    item30.AddSizer( item40, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item30, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item45 = wxBoxSizer( wxHORIZONTAL )
    
    item46 = wxButton( parent, ID_REFRESH, "Refresh", wxDefaultPosition, wxDefaultSize, 0 )
    item45.AddWindow( item46, 0, wxALIGN_CENTRE|wxALL, 5 )

    item47 = wxButton( parent, ID_KILLITEMS, "Kill Items", wxDefaultPosition, wxDefaultSize, 0 )
    item45.AddWindow( item47, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item45, 0, wxALIGN_CENTRE|wxALL, 5 )

    item48 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item48, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item49 = wxBoxSizer( wxHORIZONTAL )
    
    item50 = wxButton( parent, ID_REMOVESERVICE, "Remove Service", wxDefaultPosition, wxDefaultSize, 0 )
    item49.AddWindow( item50, 0, wxALIGN_CENTRE|wxALL, 5 )

    item49.AddSpacer( 20, 20, 0, wxALIGN_CENTRE|wxALL, 5 )

    item51 = wxButton( parent, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
    item49.AddWindow( item51, 0, wxALIGN_CENTRE|wxALL, 5 )

    item52 = wxButton( parent, wxID_OK, "OK", wxDefaultPosition, wxDefaultSize, 0 )
    item49.AddWindow( item52, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item49, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0


def ServiceListFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxListCtrl( parent, ID_SERVICELIST, wxDefaultPosition, wxSize(160,120), wxLC_REPORT|wxSUNKEN_BORDER )
    item1.AddWindow( item2, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

# Menubar functions

ID_PREFERENCES = 10054
ID_File = 10055
ID_HELP = 10056

def MenuBarFunc():
    item0 = wxMenuBar()
    
    item1 = wxMenu()
    item1.Append( ID_PREFERENCES, "Preferences", "" )
    item0.Append( item1, "File" )
    
    item2 = wxMenu()
    item0.Append( item2, "Help" )
    
    return item0

# Toolbar functions

ID_TOOL = 10057

def MainToolBarFunc( parent ):
    parent.SetMargins( [2,2] )
    
    parent.AddSimpleTool( ID_TOOL, wxBitmap( 16, 15, -1 ), "" )
    
    parent.Realize()

# Bitmap functions


# End of generated file

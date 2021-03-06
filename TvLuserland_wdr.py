#-----------------------------------------------------------------------------
# Python source generated by wxDesigner from file: TvLuserland.wdr
# Do not modify this file, all changes will be lost!
#-----------------------------------------------------------------------------

# Include wxWindows' modules
from wxPython.wx import *

# Custom source
from ClickableText import *


# Window functions

ID_SOURCE = 10000
ID_TEXT = 10001
ID_POSTTITLE = 10002
ID_POSTLINK = 10003
ID_BROWSE = 10004
ID_POSTTEXT = 10005
ID_DATE = 10006
ID_CHANGEDATE = 10007
ID_TEX = 10008
ID_POSTINGGAUGE = 10009
ID_POSTINGTEXT = 10010
ID_KILL = 10011
wxID_POST = 10012

def EditPostFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxBoxSizer( wxHORIZONTAL )
    parent.previewsizer = item1
    
    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item2 = wxFlexGridSizer( 0, 2, 0, 0 )
    item2.AddGrowableCol( 1 )
    item2.AddGrowableRow( 3 )
    
    item2.AddSpacer( 10, 10, 0, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxClickableText( parent, ID_SOURCE, "source", wxDefaultPosition, wxDefaultSize, 0 )
    item3.SetFont( wxFont( 10, wxSWISS, wxNORMAL, wxNORMAL ) )
    item2.AddWindow( item3, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxRIGHT, 10 )

    item4 = wxStaticText( parent, ID_TEXT, "Title", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item4, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item5 = wxTextCtrl( parent, ID_POSTTITLE, "", wxDefaultPosition, wxSize(300,-1), 0 )
    item2.AddWindow( item5, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item6 = wxStaticText( parent, ID_TEXT, "Link", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item6, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item7 = wxBoxSizer( wxHORIZONTAL )
    
    item8 = wxTextCtrl( parent, ID_POSTLINK, "", wxDefaultPosition, wxSize(300,-1), 0 )
    item7.AddWindow( item8, 1, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item9 = wxButton( parent, ID_BROWSE, "Go", wxDefaultPosition, wxSize(40,-1), 0 )
    item7.AddWindow( item9, 0, wxALIGN_CENTRE|wxALL, 5 )

    item2.AddSizer( item7, 0, wxGROW|wxALIGN_CENTER_VERTICAL, 5 )

    item10 = wxStaticText( parent, ID_TEXT, "Text", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item10, 0, wxALL, 5 )

    item11 = wxTextCtrl( parent, ID_POSTTEXT, "", wxDefaultPosition, wxSize(300,-1), wxTE_MULTILINE|wxTE_RICH )
    item2.AddWindow( item11, 0, wxGROW|wxALL, 5 )

    item12 = wxStaticText( parent, ID_TEXT, "Date", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item12, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item13 = wxBoxSizer( wxHORIZONTAL )
    
    item14 = wxStaticText( parent, ID_DATE, "unchanged", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item14, 1, wxALIGN_CENTRE|wxLEFT, 10 )

    item15 = wxButton( parent, ID_CHANGEDATE, "Change", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item15, 0, wxALIGN_CENTRE|wxALL, 5 )

    item2.AddSizer( item13, 0, wxGROW|wxALIGN_CENTER_VERTICAL, 5 )

    item16 = wxStaticText( parent, ID_TEX, "Categories", wxDefaultPosition, wxDefaultSize, 0 )
    item2.AddWindow( item16, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item17 = wxFlexGridSizer( 0, 4, 0, 0 )
    item17.AddGrowableCol( 0 )
    item17.AddGrowableCol( 1 )
    item17.AddGrowableCol( 2 )
    item17.AddGrowableCol( 3 )
    parent.catsizer = item17
    
    item2.AddSizer( item17, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item2, 1, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item18 = wxBoxSizer( wxHORIZONTAL )
    
    item19 = wxGauge( parent, ID_POSTINGGAUGE, 100, wxDefaultPosition, wxSize(100,-1), 0 )
    item19.Enable(false)
    item18.AddWindow( item19, 0, wxALIGN_CENTRE|wxALL, 5 )

    item20 = wxStaticText( parent, ID_POSTINGTEXT, "", wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT )
    item18.AddWindow( item20, 0, wxALIGN_CENTRE|wxALL, 5 )

    item18.AddSpacer( 10, 10, 1, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item21 = wxButton( parent, ID_KILL, "Kill", wxDefaultPosition, wxDefaultSize, 0 )
    item18.AddWindow( item21, 0, wxALIGN_CENTRE|wxALL, 5 )

    item18.AddSpacer( 10, 10, 0, wxALIGN_CENTRE|wxALL, 5 )

    item22 = wxButton( parent, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
    item18.AddWindow( item22, 0, wxALIGN_CENTRE|wxALL, 5 )

    item23 = wxButton( parent, wxID_POST, "Post", wxDefaultPosition, wxDefaultSize, 0 )
    item23.SetDefault()
    item18.AddWindow( item23, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item18, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 10 )

    item0.AddSpacer( 10, 10, 0, wxALIGN_CENTRE|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_SERVICELIST = 10013
ID_NEWSERVICE = 10014
ID_NEWPOST = 10015
ID_REFRESH = 10016
ID_KILLALL = 10017
ID_NEWSPANE = 10018

def ReadNewsFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxBoxSizer( wxHORIZONTAL )
    
    item2 = wxButton( parent, ID_SERVICELIST, "Service List", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item2, 0, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxButton( parent, ID_NEWSERVICE, "New Service", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item3, 0, wxALIGN_CENTRE|wxALL, 5 )

    item4 = wxButton( parent, ID_NEWPOST, "New Post", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item4, 0, wxALIGN_CENTRE|wxALL, 5 )

    item5 = wxButton( parent, ID_REFRESH, "Refresh", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item5, 0, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxButton( parent, ID_KILLALL, "Kill All", wxDefaultPosition, wxDefaultSize, 0 )
    item1.AddWindow( item6, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item1, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item7 = parent.newspane
    item0.AddWindow( item7, 1, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_TITLE = 10019
ID_LINK = 10020
ID_HTML = 10021
ID_EDIT = 10022

def NewsItemFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item1 = wxBoxSizer( wxHORIZONTAL )
    
    item2 = wxStaticText( parent, ID_TITLE, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item2.SetFont( wxFont( 16, wxSWISS, wxNORMAL, wxBOLD ) )
    item1.AddWindow( item2, 0, wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    item1.AddSpacer( 10, 10, 1, wxALIGN_CENTRE|wxALL, 5 )

    item3 = wxClickableText( parent, ID_SOURCE, "source", wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT )
    item3.SetFont( wxFont( 10, wxSWISS, wxNORMAL, wxNORMAL ) )
    item1.AddWindow( item3, 0, wxALIGN_RIGHT|wxALIGN_BOTTOM|wxRIGHT, 10 )

    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxLEFT, 10 )

    item4 = wxBoxSizer( wxHORIZONTAL )
    
    item5 = wxLinkText( parent, ID_LINK, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item4.AddWindow( item5, 0, wxALIGN_CENTER_VERTICAL, 0 )

    item4.AddSpacer( 10, 10, 1, wxALIGN_CENTRE|wxALL, 5 )

    item6 = wxStaticText( parent, ID_DATE, "-unset-", wxDefaultPosition, wxDefaultSize, wxALIGN_RIGHT )
    item6.SetFont( wxFont( 9, wxSWISS, wxNORMAL, wxNORMAL ) )
    item4.AddWindow( item6, 0, wxALIGN_CENTRE|wxRIGHT, 10 )

    item0.AddSizer( item4, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT, 10 )

    item7 = wxBoxSizer( wxHORIZONTAL )
    parent.itemsizer = item7
    
    item8 = parent.html
    item7.AddWindow( item8, 1, wxGROW|wxALIGN_CENTER_HORIZONTAL, 15 )

    item9 = wxBoxSizer( wxVERTICAL )
    
    item10 = wxButton( parent, ID_KILL, "Kill", wxDefaultPosition, wxDefaultSize, 0 )
    item9.AddWindow( item10, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item11 = wxButton( parent, ID_EDIT, "Edit", wxDefaultPosition, wxDefaultSize, 0 )
    item9.AddWindow( item11, 0, wxALIGN_RIGHT|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item7.AddSizer( item9, 0, wxALIGN_CENTER_HORIZONTAL|wxALL, 0 )

    item0.AddSizer( item7, 1, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 0 )

    if set_sizer == true:
        parent.SetAutoLayout( true )
        parent.SetSizer( item0 )
        if call_fit == true:
            item0.Fit( parent )
            item0.SetSizeHints( parent )
    
    return item0

ID_CONFIGWEBLOG = 10023
wxID_Cancel = 5101
wxID_Ok = 5100

def ConfigFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxNotebook( parent, ID_CONFIGWEBLOG, wxDefaultPosition, wxSize(400,300), 0 )
    item1 = wxNotebookSizer( item2 )

    item3 = wxPanel( item2, -1 )
    ConfigUiFunc( item3, false )
    item2.AddPage( item3, "User Interface" )

    item4 = wxPanel( item2, -1 )
    ConfigWeblogFunc( item4, false )
    item2.AddPage( item4, "Weblog/XML-RPC" )

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

ID_CWLOGSERVER = 10024
ID_CWLOGUSER = 10025
ID_CWLOGPASSWORD = 10026
ID_CWLOGMETAAPI = 10027
ID_CWLOGSETDATE = 10028
ID_CWLOGAGGREGATOR = 10029
ID_CWLOGDEBUG = 10030
ID_CWLOGAUTODETECT = 10031

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

ID_CUIITEMS = 10032
ID_CUIDELAFTERPOST = 10033
ID_CUIAUTOPREVIEW = 10034

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

ID_CNETTIMEOUT = 10035

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

ID_CFSDBDIR = 10036

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

ID_LASTREQUEST = 10037
ID_LASTNEWITEM = 10038
ID_ITEMSFETCHED = 10039
ID_UNREADITEMS = 10040
ID_LINE = 10041
ID_ERRORS = 10042
ID_LASTERROR = 10043
ID_LASTERRORTEXT = 10044
ID_CHANNELINFO = 10045
ID_PUBLICNAME = 10046
ID_PRIVATENAME = 10047
ID_PUBLICLINK = 10048
ID_HOWOFTEN = 10049
ID_CHECKFORREDIRECTED = 10050
ID_FIXUMLAUTS = 10051
ID_EXTRACTLTD = 10052
ID_REMOVEMARKUP = 10053
ID_KILLITEMS = 10054
ID_REMOVESERVICE = 10055

def ServiceDialogFunc( parent, call_fit = true, set_sizer = true ):
    item0 = wxBoxSizer( wxVERTICAL )
    
    item2 = wxStaticBox( parent, -1, "Information about Aggregation" )
    item1 = wxStaticBoxSizer( item2, wxHORIZONTAL )
    
    item3 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item4 = wxStaticText( parent, ID_TEXT, "Last Request", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item4, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item5 = wxStaticText( parent, ID_LASTREQUEST, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item5, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item6 = wxStaticText( parent, ID_TEXT, "Last new Item", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item6, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item7 = wxStaticText( parent, ID_LASTNEWITEM, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item7, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item8 = wxStaticText( parent, ID_TEXT, "Items fetched", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item8, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item9 = wxStaticText( parent, ID_ITEMSFETCHED, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item9, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item10 = wxStaticText( parent, ID_TEXT, "Unread Items", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item10, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item11 = wxStaticText( parent, ID_UNREADITEMS, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item3.AddWindow( item11, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item1.AddSizer( item3, 1, wxALL, 5 )

    item12 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(-1,20), wxLI_VERTICAL )
    item1.AddWindow( item12, 0, wxGROW|wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item13 = wxFlexGridSizer( 0, 2, 0, 0 )
    
    item14 = wxStaticText( parent, ID_TEXT, "Errors", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item14, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item15 = wxStaticText( parent, ID_ERRORS, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item15, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item16 = wxStaticText( parent, ID_TEXT, "Last Error", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item16, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item17 = wxStaticText( parent, ID_LASTERROR, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item17, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item18 = wxStaticText( parent, ID_TEXT, "Last Error Text", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item18, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item19 = wxStaticText( parent, ID_LASTERRORTEXT, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item13.AddWindow( item19, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item1.AddSizer( item13, 1, wxALIGN_CENTER_HORIZONTAL|wxALL, 5 )

    item0.AddSizer( item1, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item21 = wxStaticBox( parent, -1, "Information provided by the Service" )
    item20 = wxStaticBoxSizer( item21, wxVERTICAL )
    parent.rsssizer = item20
    
    item22 = wxFlexGridSizer( 0, 2, 0, 0 )
    item22.AddGrowableCol( 1 )
    
    item23 = wxStaticText( parent, ID_TEXT, "Title", wxDefaultPosition, wxDefaultSize, 0 )
    item22.AddWindow( item23, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item24 = wxStaticText( parent, ID_TITLE, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item22.AddWindow( item24, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item25 = wxStaticText( parent, ID_TEXT, "Link", wxDefaultPosition, wxDefaultSize, 0 )
    item22.AddWindow( item25, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item26 = wxLinkText( parent, ID_LINK, "-unset-", wxDefaultPosition, wxDefaultSize, 0 )
    item22.AddWindow( item26, 0, wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item20.AddSizer( item22, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT, 5 )

    item27 = wxTextCtrl( parent, ID_CHANNELINFO, "", wxDefaultPosition, wxSize(180,100), wxTE_MULTILINE )
    item20.AddWindow( item27, 3, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item20, 2, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item28 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item28, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item29 = wxFlexGridSizer( 0, 2, 0, 0 )
    item29.AddGrowableCol( 1 )
    
    item30 = wxStaticText( parent, ID_TEXT, "Public Name", wxDefaultPosition, wxDefaultSize, 0 )
    item29.AddWindow( item30, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item31 = wxTextCtrl( parent, ID_PUBLICNAME, "", wxDefaultPosition, wxSize(180,-1), 0 )
    item29.AddWindow( item31, 0, wxGROW|wxLEFT|wxRIGHT|wxTOP, 5 )

    item32 = wxStaticText( parent, ID_TEXT, "Private Name", wxDefaultPosition, wxDefaultSize, 0 )
    item29.AddWindow( item32, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item33 = wxTextCtrl( parent, ID_PRIVATENAME, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item29.AddWindow( item33, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item34 = wxStaticText( parent, ID_TEXT, "Public Link", wxDefaultPosition, wxDefaultSize, 0 )
    item29.AddWindow( item34, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item35 = wxTextCtrl( parent, ID_PUBLICLINK, "", wxDefaultPosition, wxSize(80,-1), 0 )
    item29.AddWindow( item35, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item36 = wxStaticText( parent, ID_TEXT, "Fetch how often", wxDefaultPosition, wxDefaultSize, 0 )
    item29.AddWindow( item36, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item37 = wxChoice( parent, ID_HOWOFTEN, wxDefaultPosition, wxSize(100,-1), 
        ["30m","1h","2h","3h ","4h","5h","6h","8h","12h","18h","24h","48h","72h"] , 0 )
    item29.AddWindow( item37, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item38 = wxStaticText( parent, ID_TEXT, "Options", wxDefaultPosition, wxDefaultSize, 0 )
    item29.AddWindow( item38, 0, wxALL, 5 )

    item39 = wxFlexGridSizer( 0, 2, 0, 0 )
    item39.AddGrowableCol( 0 )
    item39.AddGrowableCol( 1 )
    
    item40 = wxCheckBox( parent, ID_CHECKFORREDIRECTED, "Check for redirected URLs", wxDefaultPosition, wxDefaultSize, 0 )
    item39.AddWindow( item40, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item41 = wxCheckBox( parent, ID_FIXUMLAUTS, "Fix �ml�uts", wxDefaultPosition, wxDefaultSize, 0 )
    item39.AddWindow( item41, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxTOP, 5 )

    item42 = wxCheckBox( parent, ID_EXTRACTLTD, "Extract Link and Title from Description", wxDefaultPosition, wxDefaultSize, 0 )
    item39.AddWindow( item42, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxBOTTOM, 5 )

    item43 = wxCheckBox( parent, ID_REMOVEMARKUP, "Remove Markup", wxDefaultPosition, wxDefaultSize, 0 )
    item39.AddWindow( item43, 0, wxALIGN_CENTER_VERTICAL|wxLEFT|wxRIGHT|wxBOTTOM, 5 )

    item29.AddSizer( item39, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item0.AddSizer( item29, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item44 = wxBoxSizer( wxVERTICAL )
    
    item45 = wxButton( parent, ID_KILLITEMS, "Kill all Items of this Feed ", wxDefaultPosition, wxDefaultSize, 0 )
    item44.AddWindow( item45, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item44, 1, wxALIGN_CENTRE|wxALL, 5 )

    item46 = wxStaticLine( parent, ID_LINE, wxDefaultPosition, wxSize(20,-1), wxLI_HORIZONTAL )
    item0.AddWindow( item46, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

    item47 = wxBoxSizer( wxHORIZONTAL )
    
    item48 = wxButton( parent, ID_REMOVESERVICE, "Remove Service", wxDefaultPosition, wxDefaultSize, 0 )
    item47.AddWindow( item48, 0, wxALIGN_CENTRE|wxALL, 5 )

    item47.AddSpacer( 20, 20, 1, wxALIGN_CENTRE|wxALL, 5 )

    item49 = wxButton( parent, wxID_CANCEL, "Cancel", wxDefaultPosition, wxDefaultSize, 0 )
    item47.AddWindow( item49, 0, wxALIGN_CENTRE|wxALL, 5 )

    item50 = wxButton( parent, wxID_OK, "OK", wxDefaultPosition, wxDefaultSize, 0 )
    item47.AddWindow( item50, 0, wxALIGN_CENTRE|wxALL, 5 )

    item0.AddSizer( item47, 0, wxGROW|wxALIGN_CENTER_VERTICAL|wxALL, 5 )

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

wxID_ABOUT = 10056
ID_PREFERENCES = 10057
ID_QUIT = 10058
ID_File = 10059
ID_SHELL = 10060
ID_INSPECTOR = 10061
ID_DEBUG = 10062
ID_HELP = 10063

def MenuBarFunc():
    item0 = wxMenuBar()
    
    item1 = wxMenu()
    item1.Append( wxID_ABOUT, "About", "" )
    item1.Append( ID_PREFERENCES, "Preferences", "" )
    item1.Append( ID_QUIT, "Quit", "" )
    item0.Append( item1, "File" )
    
    item2 = wxMenu()
    item2.Append( ID_SHELL, "Python Shell", "" )
    item2.Append( ID_INSPECTOR, "Inspector", "" )
    item0.Append( item2, "Debug" )
    
    item3 = wxMenu()
    item0.Append( item3, "Help" )
    
    return item0

# Toolbar functions

ID_TOOL = 10064

def MainToolBarFunc( parent ):
    parent.SetMargins( [2,2] )
    
    parent.AddSimpleTool( ID_TOOL, wxBitmap( 16, 15, -1 ), "" )
    
    parent.Realize()

# Bitmap functions


# End of generated file

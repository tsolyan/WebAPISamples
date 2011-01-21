import sys, os, glob, urllib2
from xml.dom import minidom

"""
The Login class and resulting objects will hold the user supplied account
credentials. apiUname provides the converted account key / username string
that's used for the username when authenticating at
https://services.reachmail.net
"""
class Login:
    def __init__(self,key,uname,password):
        self.key = key.upper()
        self.uname = uname
        self.password = password
        self.apiUname = key+'\\'+uname

"""
The Service class defines all the URIs for the API
"""
class Service:
    def __init__(self):
        self.base = 'https://services.reachmail.net/'
        self.user = 'https://services.reachmail.net/Rest/Administration/v1/users/current'
        self.createList = 'https://services.reachmail.net/Rest/Contacts/v1/lists/'
        self.getList = 'https://services.reachmail.net/Rest/Contacts/v1/lists/'
        self.modifyList = 'https://services.reachmail.net/Rest/Contacts/v1/lists/'
        self.deleteList = 'https://services.reachmail.net/Rest/Contacts/v1/lists/'
        self.exportRecipients = 'https://services.reachmail.net/Rest/Contacts/v1/lists/'
        self.getExportStatus = 'https://services.reachmail.net/Rest/Contacts/v1/lists/export/status/'
        self.enumerateFields = 'https://services.reachmail.net/Rest/Contacts/v1/lists/fields/'
        self.enumerateGroups = 'https://services.reachmail.net/Rest/Contacts/v1/lists/groups/'
        self.uploadFile = 'https://services.reachmail.net/Rest/Data/'
        self.listImport = 'https://services.reachmail.net/Rest/Contacts/v1/lists/import/'
        self.getReadDetailReport = 'https://services.reachmail.net/Rest/Reports/v1/details/mailings/reads/'
        self.enumerateMailingReports = 'https://services.reachmail.net/Rest/Reports/v1/mailings/query/'
"""
The service_request function is the backbone of this library, it makes and
receives requests of the various API services.
It takes a service URL, method, request body (for POST reqeuests), api username
and api password
Use it thusly:
service_request(serviceUrl, method, requestBody, apiUser, apiPass)
-- or --
service_request(service.user,'GET','',login.apiUname,login.apiPass)
"""
def service_request(serviceUrl,method,requestBody,apiUser,apiPass):
    pwManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    pwManager.add_password(None,serviceUrl,apiUser,apiPass)
    authHandler = urllib2.HTTPBasicAuthHandler(pwManager)
    opener = urllib2.build_opener(authHandler)
    urllib2.install_opener(opener)
    global response
    try:
        if method == 'GET':
            response = urllib2.urlopen(serviceUrl)
        elif method == 'POST':
            request = urllib2.Request(serviceUrl, requestBody)
            request.add_header('Content-Type', 'text/xml')
            response = urllib2.urlopen(request)
    except urllib2.HTTPError, e:
        print "There was an HTTP error"
        print serviceUrl
        print e
        sys.exit(1)
    except urllib2.URLError, e:
        print "There is a problem with the URL"
        print e
        print "Attempted: %s" % serviceUrl
        print "Please check the service URL and try again"
        sys.exit(1)
    except urllib2.IOError, e:
        print "I/O Error"
        print e
        sys.exit(1)

"""
get_current_user:
This function gets your API account id. It needs to be run before you do
anything else with the API
"""
def get_current_user(key,uname,password):
    global accountLogin
    accountLogin = Login(key,uname,password)
    service_request(service.user,'GET','',accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    accountId = xmldoc.getElementsByTagName('AccountId')[0].firstChild.nodeValue
    #print "Authenticated successfully, account ID is %s" % accountId
    return accountId

def enumerate_fields(accountId):
    service_request(service.enumerateFields+accountId,'GET','',accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    fields = xmldoc.documentElement.getElementsByTagName('Field')
    for field in fields:
        print field.getElementsByTagName('Name')[0].childNodes[0].nodeValue+' ('+field.getElementsByTagName('Description')[0].childNodes[0].nodeValue+')'

def enumerate_groups(accountId):
    service_request(service.enumerateGroups+accountId,'GET','',accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(resposne)
    groups = xmldoc.documentElements.getElementsByTagName('Group')
    for group in groups:
        print group.getElementsByTagName('Name')[0].firstChild.nodeValue

def create_list(accountId,listName,fields):
    global listId
    fields = fields.split(" ")
    createListBody = '<ListProperties><Fields>'
    for field in fields:
        createListBody += '<Field>'+field+'</Field>'
    createListBody += '</Fields><Name>'+listName+'</Name></ListProperties>'
    service_request(service.createList+accountId,'POST',createListBody,accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    listId = xmldoc.getElementsByTagName('Id')[0].firstChild.nodeValue
    #print listId
    return listId

def upload_file(fileName):
    global dataId
    handle = open(fileName,'r')
    service_request(service.uploadFile,'POST',handle.read(),accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    dataId = xmldoc.getElementsByTagName('Id')[0].firstChild.nodeValue
    #print dataId
    return dataId

def import_list(accountId,listId,fields,dataId,delimiter,sheetName='0'):
    n = 1
    global importRequestBody
    importRequestBody = '<Parameters><DataId>'+dataId+'</DataId><FieldMappings>'
    for field in fields:
        importRequestBody += '<FieldMapping><DestinationFieldName>'+field
        importRequestBody += '</DestinationFieldName><SourceFieldPosition>'
        importRequestBody += str(n)+'</SourceFieldPosition></FieldMapping>'
        n = n + 1
    if delimiter == 'Excel':
        importRequestBody += '</FieldMappings><ImportOptions><ExcelOptions><WorksheetName>'+sheetName+'</WorksheetName></ExcelOptions><Format>Excel</Format></ImportOptions></Parameters>'
    else:
        importRequestBody += '</FieldMappings><ImportOptions><CharacterSeperatedOptions><Delimiter>'+delimiter+'</Delimiter></CharacterSeperatedOptions><Format>CharacterSeperated</Format></ImportOptions></Parameters>'
    service_request(service.listImport+accountId+'/'+listId,'POST',importRequestBody,accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    importId = xmldoc.getElementsByTagName('Id')[0].firstChild.nodeValue
    return importId

def list_from_file(accountId,fileName,fileFormat):
    global fields
    global listId
    global listName
    global delimiter
    listName = fileName.split("/")
    listName = listName[1].rstrip('.csvxtl')
    if fileFormat == 'csv':
        file = open(fileName,'r')
        head = file.readline().rstrip()
        fields = head.split(',')
        fieldsStr = " ".join(fields)
        delimiter = 'Comma'
    elif fileFormat == 'tab':
        print "Sorry, support for tab-delimited files is not available at this time"
        sys.exit(1)
        #file = open(fileName,'r')
        #head = file.readline().rstrip()
        #fields = head.split('\t')
        #fieldsStr = " ".join(fields)
        #delimiter = 'Tab'
    elif fileFormat == 'xls':
        import xlrd
        cfileName = fileName.replace('\\','/')
        book = xlrd.open_workbook(cfileName)
        sheetName = book.sheet_names(0)
        sheet = book.sheet_by_index(0)
        fields = sheet.row_values(0)
        fieldsStr = " ".join(fields)
        delimiter = 'Excel'
    print "Creating list %s" % listName
    print "with fields %s" % fields
    create_list(accountId,listName,fieldsStr)
    upload_file(fileName)
    import_list(accountId,listId,fields,dataId,delimiter,sheetName)

def get_read_detail_report(accountId,mailingId):
    requestBody = '<DetailReportFilter></DetailReportFilter>'
    service_request(service.getReadDetailReport+accountId+'/'+mailingId,'POST',requestBody,accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    print xmldoc.read()

def enumerate_mailing_reports(accountId):
    requestBody = '<MailingReportFilter></MailingReportFilter>'
    service_request(service.enumerateMailingReports+accountId,'POST',requestBody,accountLogin.apiUname,accountLogin.password)
    xmldoc = minidom.parse(response)
    mailingIds = xmldoc.documentElement.getElementsByTagName('MailingReport')
    for mailingId in mailingIds:
        print mailingId.getElementsByTagName('MailingId')[0].childNodes[0].nodeValue
    
service = Service()

version = '0.1'

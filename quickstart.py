
from __future__ import print_function
import httplib2, os, io
from apiclient.http import MediaIoBaseDownload

from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents = [tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly'
SCOPES = 'https://www.googleapis.com/auth/drive.metadata.readonly https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
#APPLICATION_NAME = 'Drive API Python Quickstart'
APPLICATION_NAME = 'GDrive Quick Access App'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def prntRes(res):
    print(res)
    items = res.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print(item)
            #print('{0} ({1})'.format(item['name'], item['id']))

def test(service):
    results = service.files().list(
        pageSize = 10, fields = 'nextPageToken, files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

    prntRes(service.files().list(q = "'root' in parents", orderBy = 'name').execute())
    prntRes(service.files().list(q = "'0Bw0qVz4FT_IQYnFnYkhiRG9uVDA' in parents", orderBy = 'name').execute())
    #0Bw0qVz4FT_IQd1p5VnJjZGxXZVU
    file_id = '0Bw0qVz4FT_IQd1p5VnJjZGxXZVU'
    request = service.files().get_media(fileId = file_id)
    fh = io.FileIO('filename~', 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    
    while done is False:
        status, done = downloader.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def dl_rqt(rqt, f_io):
    dler = MediaIoBaseDownload(f_io, rqt)
    done = False
    
    while not(done):
        status, done = dler.next_chunk()
        print("Download %d%%." % int(status.progress() * 100))

def prep_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)
    
def dl_f(service, f):
    tmp_dir_name = '.gdrive_quick_access_tmp'
    tmp_dir = os.path.join(os.path.expanduser('~'), tmp_dir_name)
    prep_dir(tmp_dir)
    
    rqt = service.files().get_media(fileId = f['id'])
    f_io = io.FileIO(os.path.join(tmp_dir, f['name']), 'wb')
    dl_rqt(rqt, f_io)
    return f_io

def open_f(f_io):
    os.startfile(f_io.name) # I think, this only works for windows only for now
    
    '''try:
        retcode = subprocess.call("open " + f_io.name, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e'''
    
def access_f(service, f):
    f_io = dl_f(service, f)
    open_f(f_io)
        
def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http = http)
    #test(service)

    f = {
        'id': '0Bw0qVz4FT_IQd1p5VnJjZGxXZVU',
        'name': '.dropbox',
    }
    access_f(service, f)

if __name__ == '__main__':
    main()

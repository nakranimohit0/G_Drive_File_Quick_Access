
import os, time
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

app = {
    'code': 'qgd',
    'name': 'G Drive Quick Access',
    'desc': 'Want to access something from google drive quickly ??',
    'dbg': True,
}

def prnt(it):
    if (app['dbg']):
        print(it)

def prep_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def usr_dir_init():
    usr_dir = os.path.join(os.path.expanduser('~'), '.' + app['code'])
    prep_dir(usr_dir)
    return usr_dir

def auth(usr_dir):
    gauth = GoogleAuth()
    credentials_path = os.path.join(usr_dir, '.credentials')
    gauth.LoadCredentialsFile(credentials_path)

    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile(credentials_path)

    return gauth

def open_f(f_loc):
    os.startfile(f_loc) # I think, this only works for windows only for now
    
    '''try:
        retcode = subprocess.call("open " + f_io.name, shell=True)
        if retcode < 0:
            print >>sys.stderr, "Child was terminated by signal", -retcode
        else:
            print >>sys.stderr, "Child returned", retcode
    except OSError, e:
        print >>sys.stderr, "Execution failed:", e'''

def watch_f(f_loc, handler):
    prnt('watch_f()')
    freq = 0.5
    prnt(f_loc)
    last_time = os.stat(f_loc).st_mtime
    while 1:
        try:
            time.sleep(freq)
            new_time = os.stat(f_loc).st_mtime
            if (new_time != last_time):
                last_time = new_time
                handler()
        except KeyboardInterrupt:
            prnt('bye')
            break

def access_f(f):
    f.GetContentFile(f['local']['path'])
    open_f(f['local']['path'])
    
    def handler():
        f.SetContentFile(f['local']['path'])
        prnt('updt')
        f.Upload()
    watch_f(f['local']['path'], handler)
    
def main():
    usr_dir = usr_dir_init()
    gauth = auth(usr_dir)
    drive = GoogleDrive(gauth)

    f = drive.CreateFile({'id': '0Bw0qVz4FT_IQd1p5VnJjZGxXZVU'})
    f['local'] = {'path': os.path.join(usr_dir, f['title'])}
    access_f(f)

if __name__ == '__main__':
    main()

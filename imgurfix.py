#! python3
# DB Examp
# future:
# if no arg and no copy, show menu
# if no arg and copy, show copy
# if arg, copy url

import pyperclip, sqlite3, time, datetime, os, sys

index = -1

drive = 'C:\\' #os.path.split(os.path.abspath(os.curdir))[0]
workspace, workbox, item = 'pydap', 'imgider', 'imgid.db'
p = os.path.join(drive, workspace, workbox, item)
# conn = 'c:\\pydap\\imgider\\imgid.db'

conn = sqlite3.connect(p)
cur = conn.cursor()

def rowcopy():
    global index
    if len(sys.argv) > 1:
            try:
                index = int(sys.argv[1])
                for i in cur.execute("Select addr from accounts where rowid = " + sys.argv[1]):
                    pyperclip.copy(i[0])
            except:
                print('### ARGERROR ###', end='\n\n')
                return

def create_table():
    cur.execute("CREATE TABLE IF NOT EXISTS accounts(name TEXT, addr TEXT, datestamp TEXT, isActive TEXT)")

def acct_entry(username, url):
    cur.execute("INSERT INTO accounts (name, addr, datestamp, isActive) VALUES(?, ?, ?, ?)"
		    , (username, url, datetime.datetime.now().strftime("%A, %d %B %Y %I:%M%p"), 'Y'))
    conn.commit()

def get_colnames():
    for i in cur.execute("PRAGMA table_info(accounts)"):
        print(i)
        

def get_urls():
    print("Menu")
    for i in cur.execute("select rowid, name from accounts"):
        print(str(i[0]) + "\t" + i[1])
    print()

def deact_url(username):
    cur.execute("UPDATE accounts SET isActive = 'N' WHERE name = " + username)


text = pyperclip.paste()
splist = text.split("/")

if "imgur.com" in splist:
    name = splist[len(splist) - 1]
    addr = ''.join(['https://', name, '.imgur.com'])
    pyperclip.copy(addr)
    print()
    print(addr, end="\n\n")
    #create_table()
    acct_entry(name, addr)
else:
    print()
    print("No account entry", end='\n\n')

rowcopy()
get_urls()
cur.close()
conn.close()

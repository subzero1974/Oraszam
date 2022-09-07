from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import subprocess

conn = None
curs = None

def db_create():
	global conn, curs
	conn = sqlite3.connect("users/data.db")
	curs = conn.cursor()
	
	curs.execute("CREATE TABLE IF NOT EXISTS users (userid INTEGER PRIMARY KEY NOT NULL, vezeteknev TEXT, nev TEXT, torzs INTEGER, telepules TEXT, irszam INTEGER, kozterulet TEXT, hazszam INTEGER, telszam1 INTEGER, telszam2 INTEGER, email TEXT)")
	curs.execute("CREATE TABLE IF NOT EXISTS dates (dateid INTEGER NOT NULL, ev INTEGER NOT NULL, honap INTEGER NOT NULL, nap INTEGER NOT NULL, oraszam INTEGER NOT NULL)")

def db_insert(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, table):
	if not vezeteknev.get() or not nev.get():
		return
	curs.execute("INSERT INTO users (vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email) VALUES (?,?,?,?,?,?,?,?,?,?)", (vezeteknev.get(), nev.get(), torzs.get(), telepules.get(), irszam.get(), kozterulet.get(), hazszam.get(), telszam1.get(), telszam2.get(), email.get()))
	conn.commit()
	vezeteknev.delete(0, 'end')
	nev.delete(0, 'end')
	torzs.delete(0, 'end')
	telepules.delete(0, 'end')
	irszam.delete(0, 'end')
	kozterulet.delete(0, 'end')
	hazszam.delete(0, 'end')
	telszam1.delete(0, 'end')
	telszam2.delete(0, 'end')
	email.delete(0, 'end')
	vezeteknev.focus_set()
	db_query(table)

def oraszam_insert(userId, ev, honap, nap, oraszam, table2, textBox):
	if not ev.get() or not honap.get() or not nap.get() or not oraszam.get():
		return
	curs.execute("INSERT INTO dates (dateid, ev, honap, nap, oraszam) VALUES (?,?,?,?,?) ", (userId.get(), ev.get(), honap.get(), nap.get(), oraszam.get()))
	conn.commit()
	nap.delete(0, 'end')
	oraszam.delete(0, 'end')
	nap.focus_set()
	kattOra(userId, table2, textBox)

def db_mezok_torlese(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, kereses):
	vezeteknev.delete(0, 'end')
	nev.delete(0, 'end')
	torzs.delete(0, 'end')
	telepules.delete(0, 'end')
	irszam.delete(0, 'end')
	kozterulet.delete(0, 'end')
	hazszam.delete(0, 'end')
	telszam1.delete(0, 'end')
	telszam2.delete(0, 'end')
	email.delete(0, 'end')
	kereses.delete(0, 'end')	
	vezeteknev.focus_set()
	
def oraszam_mezok_torlese(ev, honap, nap, oraszam):
	ev.delete(0, 'end')
	honap.delete(0, 'end')
	nap.delete(0, 'end')
	oraszam.delete(0, 'end')
	ev.focus_set()

def db_kereses(table, kereses):
	if not kereses.get():
		return
	curs.execute("SELECT * FROM users WHERE vezeteknev LIKE ? OR nev LIKE ? OR torzs LIKE ? OR telepules LIKE ? OR irszam LIKE ? OR kozterulet LIKE ? OR hazszam LIKE ? OR telszam1 LIKE ? OR telszam2 LIKE ? OR email LIKE ?", (f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%', f'%{kereses.get()}%'))
	datas = curs.fetchall()
	table.delete(*table.get_children())
	for data in datas:
		table.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))
	kereses.delete(0, 'end')
	
def oraKereses(userId, table2, ev, honap, oraszam, textBox):
	if not userId.get() or not ev.get() or not honap.get():
		return
	curs.execute("SELECT * FROM dates WHERE dateid = ? AND ev = ? AND honap = ? ORDER BY dateid ASC, ev ASC, honap ASC, nap ASC", (f'{userId.get()}', f'{ev.get()}', f'{honap.get()}'))
	datas2 = curs.fetchall()
	table2.delete(*table2.get_children())
	oraCikl = 0
	osszOra = 0
	for data2 in datas2:
		table2.insert("", "end", values=(data2[0], data2[1], data2[2], data2[3], data2[4]))
		osszOra = osszOra + data2[4]
		oraCikl += 1		
	textBox.delete(1.0, 'end')
	textBox.insert('end', "Havi óraszám különbség: ")
	textBox.insert('end', (osszOra-oraCikl*8))
	textBox.insert('end', '\n')
	hoGet = int(f'{honap.get()}')
	if hoGet>0 and hoGet<4:
		curs.execute("SELECT * FROM dates WHERE dateid = ? AND ev = ? AND honap BETWEEN 1 AND 3", (f'{userId.get()}', f'{ev.get()}'))
	if hoGet>3 and hoGet<7:
		curs.execute("SELECT * FROM dates WHERE dateid = ? AND ev = ? AND honap BETWEEN 4 AND 6", (f'{userId.get()}', f'{ev.get()}'))
	if hoGet>6 and hoGet<10:
		curs.execute("SELECT * FROM dates WHERE dateid = ? AND ev = ? AND honap BETWEEN 7 AND 9", (f'{userId.get()}', f'{ev.get()}'))
	if hoGet>9 and hoGet<13:
		curs.execute("SELECT * FROM dates WHERE dateid = ? AND ev = ? AND honap BETWEEN 10 AND 12", (f'{userId.get()}', f'{ev.get()}'))
	datas2 = curs.fetchall()
	oraCikl2 = 0
	osszOra2 = 0
	for data2 in datas2:
		osszOra2 = osszOra2 + data2[4]
		oraCikl2 += 1
	textBox.insert('end', "Negyedéves óraszám különbség: ")
	textBox.insert('end', (osszOra2-oraCikl2*8))
		
def kattOra(userId, table2, textBox):
	curs.execute("SELECT * FROM dates WHERE dateid = ? ORDER BY dateid ASC, ev ASC, honap ASC, nap ASC", (f'{userId.get()}',))
	datas2 = curs.fetchall()
	table2.delete(*table2.get_children())
	for data2 in datas2:
		table2.insert("", "end", values=(data2[0], data2[1], data2[2], data2[3], data2[4]))
	textBox.delete(1.0, 'end')

def db_query(table):
	curs.execute("SELECT * FROM users")
	datas = curs.fetchall()
	table.delete(*table.get_children())
	for data in datas:
		table.insert("", "end", values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8], data[9], data[10]))

def ora_query(table2):
	curs.execute("SELECT * FROM dates ORDER BY dateid ASC, ev ASC, honap ASC, nap ASC")
	datas2 = curs.fetchall()
	table2.delete(*table2.get_children())
	for data2 in datas2:
		table2.insert("", "end", values=(data2[0], data2[1], data2[2], data2[3], data2[4]))
	
def db_id_torles(table, idTorles, idUpdate, table2, userId, vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, kereses):
	res = messagebox.askyesno('Törlés', 'Biztosan törli a felhasználót?')
	if res == True:
		if not idTorles.get():
			return
		curs.execute("DELETE FROM users WHERE rowid = ?", (f'{idTorles.get()}',))
		curs.execute("DELETE FROM dates WHERE dateid = ?", (f'{idTorles.get()}',))
		idTorles.delete(0, 'end')
		idUpdate.delete(0, 'end')
		userId.delete(0, 'end')
		conn.commit()
		db_query(table)
		ora_query(table2)
		db_mezok_torlese(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, kereses)
	elif res == False:
		return

def oraTorles(table2):
	try:
		selectedItem2 = table2.selection()[0]
	except:
		return
	curs.execute("DELETE FROM dates WHERE dateid = ? AND ev = ? AND honap = ? AND nap = ? AND oraszam = ?", (table2.item(selectedItem2)['values'][0], table2.item(selectedItem2)['values'][1], table2.item(selectedItem2)['values'][2], table2.item(selectedItem2)['values'][3], table2.item(selectedItem2)['values'][4]))
	conn.commit()
	curs.execute("SELECT * FROM dates WHERE dateid = ? ORDER BY dateid ASC, ev ASC, honap ASC, nap ASC", (table2.item(selectedItem2)['values'][0],))
	datas2 = curs.fetchall()
	table2.delete(*table2.get_children())
	for data2 in datas2:
		table2.insert("", "end", values=(data2[0], data2[1], data2[2], data2[3], data2[4]))
	messagebox.showinfo('Információ', 'Óraszám törölve!')

def db_id_update(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, table, idUpdate, idTorles):
	if not idUpdate.get():
		return
	curs.execute("UPDATE users SET vezeteknev = ?, nev = ?, torzs = ?, telepules = ?, irszam = ?, kozterulet = ?, hazszam = ?, telszam1 = ?, telszam2 = ?, email = ? WHERE rowid = ?", (f'{vezeteknev.get()}', f'{nev.get()}', f'{torzs.get()}', f'{telepules.get()}', f'{irszam.get()}', f'{kozterulet.get()}', f'{hazszam.get()}', f'{telszam1.get()}', f'{telszam2.get()}', f'{email.get()}', f'{idUpdate.get()}',))
	idUpdate.delete(0, 'end')
	idTorles.delete(0, 'end')
	conn.commit()
	db_query(table)
	messagebox.showinfo('Információ', 'Adatok módosítva!')

def ridTo(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, idTorles, idUpdate, userId):
	curs.execute("SELECT rowid FROM users WHERE vezeteknev = ? AND nev = ? AND torzs = ? AND telepules = ? AND irszam = ? AND kozterulet = ? AND hazszam = ? AND telszam1 = ? AND telszam2 = ? AND email = ?", (f'{vezeteknev.get()}', f'{nev.get()}', f'{torzs.get()}', f'{telepules.get()}', f'{irszam.get()}', f'{kozterulet.get()}', f'{hazszam.get()}', f'{telszam1.get()}', f'{telszam2.get()}', f'{email.get()}'))
	rid = curs.fetchall()
	idTorles.delete(0, 'end')
	idTorles.insert(0, rid)
	idUpdate.delete(0, 'end')
	idUpdate.insert(0, rid)
	userId.delete(0, 'end')
	userId.insert(0, rid)
	
def db_export_csv(table2):
	try:
		selectedItem2 = table2.selection()[0]
	except:
		return
	curs.execute("SELECT ev, honap, nap, oraszam FROM dates WHERE dateid = ? ORDER BY dateid ASC, ev ASC, honap ASC, nap ASC", (table2.item(selectedItem2)['values'][0],))
	datas = curs.fetchall()
	with open("users/data.txt", "w", encoding="utf-8") as out_file:
		curs.execute("SELECT vezeteknev, nev FROM users WHERE userid = ?", (table2.item(selectedItem2)['values'][0],))
		datas2 = curs.fetchall()
		for data in datas2:
			out_file.write(" ".join(str(d) for d in data))
			out_file.write("\n")
		out_file.write(", ".join(["Év  ", "Hónap", "Nap", "Óraszám"]))
		out_file.write("\n")
		for data in datas:
			out_file.write(",   ".join(str(d) for d in data))
			out_file.write("\n")
	subprocess.Popen(["notepad", "users/data.txt"])

def db_close():
	if conn and curs:
		print("Adatbazis lezarva.")
		curs.close()
		conn.close()

win = Tk()
win.title("Oraszam")
win.geometry("1300x960")
win.resizable(False, False)

db_create()

Label(win, text="Vezetéknév", font="Helvetica 12 bold").grid(row=1, column=0)
vezeteknev = Entry(win, font="Helvetica 16", width=30)
vezeteknev.grid(row=1, column=1, padx=5, pady=5)

Label(win, text="Keresztnév", font="Helvetica 12 bold").grid(row=2, column=0)
nev = Entry(win, font="Helvetica 16", width=30)
nev.grid(row=2, column=1, padx=5, pady=5)

Label(win, text="Törzsszám", font="Helvetica 12 bold").grid(row=3, column=0)
torzs = Entry(win, font="Helvetica 16", width=30)
torzs.grid(row=3, column=1, padx=5, pady=5)

Label(win, text="Település", font="Helvetica 12 bold").grid(row=4, column=0)
telepules = Entry(win, font="Helvetica 16", width=30)
telepules.grid(row=4, column=1, padx=5, pady=5)

Label(win, text="Irányítószám", font="Helvetica 12 bold").grid(row=5, column=0)
irszam = Entry(win, font="Helvetica 16", width=30)
irszam.grid(row=5, column=1, padx=5, pady=5)

Label(win, text="Közterület", font="Helvetica 12 bold").grid(row=6, column=0)
kozterulet = Entry(win, font="Helvetica 16", width=30)
kozterulet.grid(row=6, column=1, padx=5, pady=5)

Label(win, text="Házszám", font="Helvetica 12 bold").grid(row=7, column=0)
hazszam = Entry(win, font="Helvetica 16", width=30)
hazszam.grid(row=7, column=1, padx=5, pady=5)

Label(win, text="Telefonszám 1", font="Helvetica 12 bold").grid(row=8, column=0)
telszam1 = Entry(win, font="Helvetica 16", width=30)
telszam1.grid(row=8, column=1, padx=5, pady=5)

Label(win, text="Telefonszám 2", font="Helvetica 12 bold").grid(row=9, column=0)
telszam2 = Entry(win, font="Helvetica 16", width=30)
telszam2.grid(row=9, column=1, padx=5, pady=5)

Label(win, text="E-mail", font="Helvetica 12 bold").grid(row=10, column=0)
email = Entry(win, font="Helvetica 16", width=30)
email.grid(row=10, column=1, padx=5, pady=5)

Button(win, text=" Adatrögzítés ", command=lambda: db_insert(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, table), font="Helvetica 12 bold").grid(row=5, column=2, sticky='w', padx=5, pady=5)

Button(win, text="   Teljes lista   ", command=lambda: db_query(table), font="Helvetica 12 bold").grid(row=6, column=2, sticky='w', padx=5, pady=5)

Button(win, text="Összes mező törlése", command=lambda: db_mezok_torlese(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, kereses), font="Helvetica 12 bold").grid(row=7, column=2, sticky='w', padx=5, pady=5)

idUpdate = Entry(win, font="Helvetica 16", width=12)
idUpdate.grid(row=8, column=2, sticky='n', padx=5, pady=5)
Button(win, text="Módosítás Id:", command=lambda: db_id_update(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, table, idUpdate, idTorles), font="Helvetica 12 bold").grid(row=8, column=2, sticky='w', padx=5, pady=5)

idTorles = Entry(win, font="Helvetica 16", width=12)
idTorles.grid(row=9, column=2, sticky='n', padx=5, pady=5)
Button(win, text="    Törlés Id:    ", command=lambda: db_id_torles(table, idTorles, idUpdate, table2, userId, vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, kereses), font="Helvetica 12 bold").grid(row=9, column=2, sticky='w', padx=5, pady=5)

kereses = Entry(win, font="Helvetica 16", width=25)
kereses.grid(row=10, column=2, sticky='w', padx=5, pady=5)
Button(win, text=" Keresés ", command=lambda: db_kereses(table, kereses), font="Helvetica 12 bold").grid(row=10, column=2, sticky='e', padx=5, pady=5)

cols = ("Id", "Vezetéknév", "Név", "Törzsszám", "Település", "Irányítószám", "Közterület", "Házszám", "Telefonszám 1", "Telefonszám 2", "E-mail")
table = ttk.Treeview(win, columns=cols, show="headings", selectmode="browse", height=8)
table.column('Id', width=50)
table.column('Vezetéknév', width=170)
table.column('Név', width=120)
table.column('Törzsszám', width=100)
table.column('Település', width=150)
table.column('Irányítószám', width=80)
table.column('Közterület', width=180)
table.column('Házszám', width=60)
table.column('Telefonszám 1', width=90)
table.column('Telefonszám 2', width=90)
table.column('E-mail', width=200)
for col in cols:
	table.heading(col, text=col)
table.grid(row=12, column=0, columnspan=3, padx=5, pady=5)
scrollbar = ttk.Scrollbar(win, orient='vertical', command=table.yview)
table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=12, column=2, sticky='nse')

cols2 = ("Id", "Év", "Hónap", "Nap", "Óraszám")
table2 = ttk.Treeview(win, columns=cols2, show="headings", selectmode="browse", height=13)
table2.column('Id', width=50)
table2.column('Év', width=70)
table2.column('Hónap', width=60)
table2.column('Nap', width=60)
table2.column('Óraszám', width=80)
for col2 in cols2:
	table2.heading(col2, text=col2)
table2.grid(row=17, column=0, padx=5, pady=5, sticky="e")
scrollbar2 = ttk.Scrollbar(win, orient='vertical', command=table2.yview)
table2.configure(yscroll=scrollbar2.set)
scrollbar2.grid(row=17, column=0, sticky='nse')

def selectItem(a):
	vezeteknev.delete(0,END)
	nev.delete(0, 'end')
	torzs.delete(0, 'end')
	telepules.delete(0, 'end')
	irszam.delete(0, 'end')
	kozterulet.delete(0, 'end')
	hazszam.delete(0, 'end')
	telszam1.delete(0, 'end')
	telszam2.delete(0, 'end')
	email.delete(0, 'end')
	try:
		selectedItem = table.selection()[0]
	except:
		return
	vezeteknev.insert(0, table.item(selectedItem)['values'][1])
	nev.insert(0, table.item(selectedItem)['values'][2])
	torzs.insert(0, table.item(selectedItem)['values'][3])
	telepules.insert(0, table.item(selectedItem)['values'][4])
	irszam.insert(0, table.item(selectedItem)['values'][5])
	kozterulet.insert(0, table.item(selectedItem)['values'][6])
	hazszam.insert(0, table.item(selectedItem)['values'][7])
	telszam1.insert(0, table.item(selectedItem)['values'][8])
	telszam2.insert(0, table.item(selectedItem)['values'][9])
	email.insert(0, table.item(selectedItem)['values'][10])
	ridTo(vezeteknev, nev, torzs, telepules, irszam, kozterulet, hazszam, telszam1, telszam2, email, idTorles, idUpdate, userId)
	kattOra(userId, table2, textBox)
	
def selectItem2(a):
	try:
		selectedItem2 = table2.selection()[0]
	except:
		return
	userId.delete(0, 'end')
	userId.insert(0, table2.item(selectedItem2)['values'][0])
	
frame = ttk.Frame(win)
frame.grid(row=15, column=0, columnspan=3)
Label(frame, text="Id:", font="Helvetica 12 bold").grid(row=0, column=0)
userId = Entry(frame, font="Helvetica 16", width=6)
userId.grid(row=0, column=1, padx=5, pady=5)
Label(frame, text="Dátum:", font="Helvetica 12 bold").grid(row=0, column=2)
ev = Entry(frame, font="Helvetica 16", width=5)
ev.grid(row=0, column=3, padx=5, pady=5)
honap = Entry(frame, font="Helvetica 16", width=3)
honap.grid(row=0, column=4, padx=5, pady=5)
nap = Entry(frame, font="Helvetica 16", width=3)
nap.grid(row=0, column=5, padx=5, pady=5)
Label(frame, text="  Óraszám:", font="Helvetica 12 bold").grid(row=0, column=6)
oraszam = Entry(frame, font="Helvetica 16", width=4)
oraszam.grid(row=0, column=7, padx=5, pady=5)
Button(frame, text=" Adatrögzítés ", command=lambda: oraszam_insert(userId, ev, honap, nap, oraszam, table2, textBox), font="Helvetica 12 bold").grid(row=0, column=8, padx=5, pady=5)
Button(frame, text=" Összes mező törlése ", command=lambda: oraszam_mezok_torlese(ev, honap, nap, oraszam), font="Helvetica 12 bold").grid(row=0, column=9, padx=5, pady=5)
Button(frame, text=" Teljes lista ", command=lambda: ora_query(table2), font="Helvetica 12 bold").grid(row=0, column=10, padx=5, pady=5)
Button(frame, text=" Keresés ", command=lambda: oraKereses(userId, table2, ev, honap, oraszam, textBox), font="Helvetica 12 bold").grid(row=0, column=11, padx=5, pady=5)
Button(win, text=" Nyomtatás ", command=lambda: db_export_csv(table2), font="Helvetica 12 bold").grid(row=17, column=1, padx=5, pady=5, sticky='s')

textBox = Text (win, height=3, width=35, font="Helvetica 12 bold")
textBox.grid(row=17, column=1, padx=5, pady=40, sticky='n')
Button(win, text=" Törlés ", command=lambda: oraTorles(table2), font="Helvetica 12 bold").grid(row=17, column=1, padx=25, pady=5, sticky='sw')

img = PhotoImage(file='logo.png')
Label(win, image=img).grid(row=17, column=2, sticky='se', padx=20)

db_query(table)

table.bind('<ButtonRelease-1>', selectItem)
table2.bind('<ButtonRelease-1>', selectItem2)

win.mainloop()

db_close()

















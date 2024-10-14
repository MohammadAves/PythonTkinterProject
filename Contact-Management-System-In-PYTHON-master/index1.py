from tkinter import *
import sqlite3
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

# Main Application Window
root = Tk()
root.title("Contact List")
width = 800
height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry(f"{width}x{height}+{int(x)}+{int(y)}")
root.resizable(False, False)
root.config(bg="#f0f0f0")

# ============================ Variables =============================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
AGE = StringVar()
ADDRESS = StringVar()
CONTACT = StringVar()

# ============================ Methods ===============================

def Database():
    conn = sqlite3.connect("contact_list.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS member (
            mem_id INTEGER PRIMARY KEY AUTOINCREMENT,
            firstname TEXT,
            lastname TEXT,
            gender TEXT,
            age TEXT,
            address TEXT,
            contact TEXT
        )
    """)
    cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def SubmitData():
    if FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or AGE.get() == "" or ADDRESS.get() == "" or CONTACT.get() == "":
        tkMessageBox.showwarning('Input Error', 'Please complete all required fields.', icon="warning")
    else:
        tree.delete(*tree.get_children())
        conn = sqlite3.connect("contact_list.db")
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO member (firstname, lastname, gender, age, address, contact) 
            VALUES (?, ?, ?, ?, ?, ?)
        """, (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get()))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        clear_form()

def UpdateData():
    if not tree.selection():
        tkMessageBox.showwarning('Select Record', 'Please select a record to update.', icon="warning")
    else:
        curItem = tree.focus()
        contents = tree.item(curItem)
        selecteditem = contents['values']
        conn = sqlite3.connect("contact_list.db")
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE member 
            SET firstname = ?, lastname = ?, gender = ?, age = ?, address = ?, contact = ? 
            WHERE mem_id = ?
        """, (FIRSTNAME.get(), LASTNAME.get(), GENDER.get(), AGE.get(), ADDRESS.get(), CONTACT.get(), selecteditem[0]))
        conn.commit()
        cursor.execute("SELECT * FROM member ORDER BY lastname ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()
        clear_form()

def DeleteData():
    if not tree.selection():
        tkMessageBox.showwarning('Delete Error', 'Please select a record to delete!', icon="warning")
    else:
        result = tkMessageBox.askquestion('Delete Confirmation', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = tree.item(curItem)
            selecteditem = contents['values']
            tree.delete(curItem)
            conn = sqlite3.connect("contact_list.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM member WHERE mem_id = ?", (selecteditem[0],))
            conn.commit()
            cursor.close()
            conn.close()

def clear_form():
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    AGE.set("")
    ADDRESS.set("")
    CONTACT.set("")

def OnSelected(event):
    curItem = tree.focus()
    contents = tree.item(curItem)
    selecteditem = contents['values']
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    AGE.set(selecteditem[4])
    ADDRESS.set(selecteditem[5])
    CONTACT.set(selecteditem[6])

# ============================ UI Layout ==============================
TopFrame = Frame(root, bd=1, relief=SOLID)
TopFrame.pack(side=TOP, fill=X)

MidFrame = Frame(root, bg="#f0f0f0")
MidFrame.pack(side=TOP, pady=20)

ButtonFrame = Frame(MidFrame, bg="#f0f0f0")
ButtonFrame.pack(side=LEFT, padx=20)

FormFrame = Frame(MidFrame, bg="#f0f0f0")
FormFrame.pack(side=LEFT)

lbl_title = Label(TopFrame, text="Contact Management System", font=('Arial', 18), bg="#4682B4", fg="white", height=2)
lbl_title.pack(fill=X)

# Form Labels and Entry Widgets
Label(FormFrame, text="Firstname", font=('Arial', 12), bg="#f0f0f0").grid(row=0, column=0, pady=5, padx=5, sticky=W)
Entry(FormFrame, textvariable=FIRSTNAME, font=('Arial', 12)).grid(row=0, column=1, pady=5, padx=5)

Label(FormFrame, text="Lastname", font=('Arial', 12), bg="#f0f0f0").grid(row=1, column=0, pady=5, padx=5, sticky=W)
Entry(FormFrame, textvariable=LASTNAME, font=('Arial', 12)).grid(row=1, column=1, pady=5, padx=5)

Label(FormFrame, text="Gender", font=('Arial', 12), bg="#f0f0f0").grid(row=2, column=0, pady=5, padx=5, sticky=W)
Radiobutton(FormFrame, text="Male", variable=GENDER, value="Male", font=('Arial', 12), bg="#f0f0f0").grid(row=2, column=1, sticky=W)
Radiobutton(FormFrame, text="Female", variable=GENDER, value="Female", font=('Arial', 12), bg="#f0f0f0").grid(row=2, column=1)

Label(FormFrame, text="Age", font=('Arial', 12), bg="#f0f0f0").grid(row=3, column=0, pady=5, padx=5, sticky=W)
Entry(FormFrame, textvariable=AGE, font=('Arial', 12)).grid(row=3, column=1, pady=5, padx=5)

Label(FormFrame, text="Address", font=('Arial', 12), bg="#f0f0f0").grid(row=4, column=0, pady=5, padx=5, sticky=W)
Entry(FormFrame, textvariable=ADDRESS, font=('Arial', 12)).grid(row=4, column=1, pady=5, padx=5)

Label(FormFrame, text="Contact", font=('Arial', 12), bg="#f0f0f0").grid(row=5, column=0, pady=5, padx=5, sticky=W)
Entry(FormFrame, textvariable=CONTACT, font=('Arial', 12)).grid(row=5, column=1, pady=5, padx=5)

# Buttons
Button(ButtonFrame, text="+ Add New", bg="#66ff66", width=20, command=SubmitData).pack(pady=10)
Button(ButtonFrame, text="Update", bg="#FFA500", width=20, command=UpdateData).pack(pady=10)
Button(ButtonFrame, text="Delete", bg="#FF6347", width=20, command=DeleteData).pack(pady=10)

# Treeview (Table) for displaying contacts
TreeFrame = Frame(root)
TreeFrame.pack(pady=20)
scrollbarx = Scrollbar(TreeFrame, orient=HORIZONTAL)
scrollbary = Scrollbar(TreeFrame, orient=VERTICAL)

tree = ttk.Treeview(TreeFrame, columns=("MemberID", "Firstname", "Lastname", "Gender", "Age", "Address", "Contact"), 
                    height=10, selectmode="extended", 
                    yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)

tree.heading('MemberID', text="ID", anchor=W)
tree.heading('Firstname', text="Firstname", anchor=W)
tree.heading('Lastname', text="Lastname", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Age', text="Age", anchor=W)
tree.heading('Address', text="Address", anchor=W)
tree.heading('Contact', text="Contact", anchor=W)

tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=40)
tree.column('#2', stretch=NO, minwidth=0, width=100)
tree.column('#3', stretch=NO, minwidth=0, width=100)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=150)
tree.column('#6', stretch=NO, minwidth=0, width=120)

tree.pack()
tree.bind('<ButtonRelease-1>', OnSelected)

# Initialize the database and display data
Database()

# Run the application
root.mainloop()

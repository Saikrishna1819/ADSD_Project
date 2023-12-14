#Importing required Libraries
import sqlite3, hashlib
import base64
from tkinter import *
from tkinter import simpledialog
from functools import partial
from cryptography.hazmat.backends import default_backend


backend = default_backend()
salt = b'2444'



with sqlite3.connect('Project_manager.db') as db:
    cursor = db.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS userslogin(
    id INTEGER PRIMARY KEY,
    username TEXT,
    password TEXT NOT NULL
);
""")



cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks(
id INTEGER PRIMARY KEY,
project_name TEXT NOT NULL,
start_date TEXT NOT NULL,
end_date TEXT NOT NULL,
Manager_name TEXT NOT NULL);
""")


def popUp(text):
    answer = simpledialog.askstring("input string", text)

    return answer


window = Tk()
window.update()
window.title("Task Manager")



def firstScreen():
    cursor.execute('DELETE FROM tasks')
        
    for widget in window.winfo_children():
        widget.destroy()
        
    window.geometry('600x400')
    lbl = Label(window, text="Enter username")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=5)

    txt = Entry(window, width=20, show="*")
    txt.pack()
    txt.focus()

    lbl1 = Label(window, text="enter password")
    lbl1.config(anchor=CENTER)
    lbl1.pack(pady=5)
    
    txt1 = Entry(window, width=20, show="*")
    txt1.pack()
    
    lbl2 = Label(window, text="enter confirm password")
    lbl2.config(anchor=CENTER)
    lbl2.pack(pady=5)

    
    txt2 = Entry(window, width=20, show="*")
    txt2.pack()
   

    def savePassword():
        if txt1.get() == txt2.get():
            sql = "DELETE FROM userslogin WHERE id = 1"
            cursor.execute(sql)
            entered_password = txt.get()
            entered_hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
            cursor.execute('SELECT * FROM userslogin WHERE id = 1 AND password = ?', (entered_hashed_password,))
            
            master_password = txt1.get()
            hashed_password = hashlib.sha256(master_password.encode()).hexdigest()
            insert_password = """INSERT INTO userslogin(username, password) VALUES(?, ?) """
            cursor.execute(insert_password, ('admin', hashed_password))
            db.commit()
            taskScreen()
            
        else:
            lbl.config(text="Passwords doesnot match", fg='red')
        
        
    

    btn = Button(window, text="Sign Up", command=savePassword)
    btn.pack(pady=10)
    

def loginScreen():
    for widget in window.winfo_children():
        widget.destroy()

    window.geometry('600x250')
    lbl = Label(window, text="Enter username")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=10)
    
    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()
    
    lbl = Label(window, text="Enter password")
    lbl.config(anchor=CENTER)
    lbl.pack(pady=10)

    txt = Entry(window, width=20)
    txt.pack()
    txt.focus()

    lbl1 = Label(window)
    lbl1.config(anchor=CENTER)
    lbl1.pack(side=TOP)
    def getMasterPassword(entered_password):
        entered_hashed_password = hashlib.sha256(entered_password.encode()).hexdigest()
        cursor.execute('SELECT * FROM userslogin WHERE id = 1 AND password = ?', (entered_hashed_password,))
        return cursor.fetchall()

    def checkPassword():
        entered_password = txt.get()
        password = getMasterPassword(entered_password)

        if password:
            taskScreen()
        else:
            txt.delete(0, 'end')
            lbl1.config(text="Wrong Password", fg='red')

    
   
    btn = Button(window, text="Sign In", command=checkPassword)
    btn.pack(pady=3)
def taskScreen():
    for widget in window.winfo_children():
        widget.destroy()

    def addEntry():
        text1 = "Project_Name"
        text2 = "Start_Date"
        text3 = "End_Date"
        text4 = "Manager_Name"
        project_name = popUp(text1)
        start_date = popUp(text2)
        end_date = popUp(text3)
        manager_name = popUp(text4)
        insert_fields = """INSERT INTO tasks(project_name, start_date, end_date, manager_name) 
        VALUES(?, ?, ?, ?) """
        cursor.execute(insert_fields, (project_name, start_date, end_date, manager_name))
        db.commit()

        taskScreen()
    def removeEntry(input):
        cursor.execute("DELETE FROM tasks WHERE id = ?", (input,))
        db.commit()
        taskScreen()

    def updateEntry(task_id):
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        current_task = cursor.fetchone()

        update_window = Tk()
        update_window.title("Update Task")

        project_name_var = StringVar(update_window, value=current_task[1])
        start_date_var = StringVar(update_window, value=current_task[2])
        end_date_var = StringVar(update_window, value=current_task[3])
        manager_name_var = StringVar(update_window, value=current_task[4])

        lbl1 = Label(update_window, text="Project Name")
        lbl1.grid(row=0, column=0)
        entry1 = Entry(update_window, textvariable=project_name_var)
        entry1.grid(row=0, column=1)

        lbl2 = Label(update_window, text="Start Date")
        lbl2.grid(row=1, column=0)
        entry2 = Entry(update_window, textvariable=start_date_var)
        entry2.grid(row=1, column=1)

        lbl3 = Label(update_window, text="End Date")
        lbl3.grid(row=2, column=0)
        entry3 = Entry(update_window, textvariable=end_date_var)
        entry3.grid(row=2, column=1)

        lbl4 = Label(update_window, text="Manager Name")
        lbl4.grid(row=3, column=0)
        entry4 = Entry(update_window, textvariable=manager_name_var)
        entry4.grid(row=3, column=1)

        def saveChanges():
                updated_project_name = project_name_var.get()
                updated_start_date = start_date_var.get()
                updated_end_date = end_date_var.get()
                updated_manager_name = manager_name_var.get()

                cursor.execute("""
                    UPDATE tasks
                    SET project_name=?, start_date=?, end_date=?, manager_name=?
                    WHERE id=?
                """, (updated_project_name, updated_start_date, updated_end_date, updated_manager_name, task_id))

                db.commit()
                update_window.destroy()
                taskScreen()

        btn_save = Button(update_window, text="Save Changes", command=saveChanges)
        btn_save.grid(row=4, column=0, columnspan=2, pady=10)



    
    window.geometry('800x800')
    window.resizable(height=None, width=None)
    lbl = Label(window, text="Project Manager", font=("Arial", 20))
    lbl.grid(column=1)
    lbl.config(anchor=CENTER)
    
    btn = Button(window, text="Add a New Project", command=addEntry)
    btn.grid(column=1, pady=10)
    btn.config(anchor=CENTER)


    lbl = Label(window, text="Project_Name")
    lbl.grid(row=2, column=0, padx=40)
    lbl = Label(window, text="Start_Date")
    lbl.grid(row=2, column=1, padx=80)
    lbl = Label(window, text="End_Date")
    lbl.grid(row=2, column=2, padx=80)
    lbl = Label(window, text="Manager_Name")
    lbl.grid(row=2, column=3, padx=80)
    cursor.execute('SELECT * FROM tasks')
    if (cursor.fetchall() != None):
        i = 0
        while True:
            cursor.execute('SELECT * FROM tasks')
            array = cursor.fetchall()

            if (len(array) == 0):
                break
            lbl1 = Label(window, text=(array[i][1]), font=("Arial", 12))
            lbl1.grid(column=0, row=(i+3))
            lbl2 = Label(window, text=(array[i][2]), font=("Arial", 12))
            lbl2.grid(column=1, row=(i+3))
            lbl3 = Label(window, text=(array[i][3]), font=("Arial", 12))
            lbl3.grid(column=2, row=(i+3))
            lbl4 = Label(window, text=(array[i][4]), font=("Arial", 12))
            lbl4.grid(column=3, row=(i+3))
            btn = Button(window, text="Delete", command=  partial(removeEntry, array[i][0]))
            btn.grid(column=4, row=(i+3), pady=10, padx=50)
            btn1 = Button(window, text="Update", command=lambda i=array[i][0]: updateEntry(i))
            btn1.grid(column=5, row=(i+3), pady=50)   
            i = i +1
            cursor.execute('SELECT * FROM tasks')
            if (len(cursor.fetchall()) <= i):
                break
cursor.execute('SELECT * FROM userslogin')
if (cursor.fetchall()):
    loginScreen()
else:
    firstScreen()
window.mainloop()

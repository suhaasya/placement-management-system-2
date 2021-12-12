# Multi-frame Placement Management System application v3.0
import csv
from tkinter.constants import END, INSERT
from configurations import config
import tkinter as tk
from data.randomDate import *
from PIL import ImageTk, Image
from tkinter import Frame, messagebox
import ctypes
from tkinter import filedialog
from tkinter import ttk
import os
import sys
import mysql.connector
import pymysql
sys.path.append(f'{os.getcwd()}')

# to Increase Quality of Output
ctypes.windll.shcore.SetProcessDpiAwareness(1)

det = {
    "username": "",
    "password": ""
}


def mysqlSetUp():

    global MySQLusername, MySQLpassword, adc
    master = tk.Tk()
    master.title("MySQL Login")
    master.geometry('400x300')
    master.iconphoto(False,
                     tk.PhotoImage(file="businessman.png"))
    master.configure(bg="#96D4D4")

    homeHeadingLable = tk.Label(master, text="MySQL Login", font=("Ärial", 20, "bold"),
                                background="#96D4D4", foreground="#282A35")
    homeHeadingLable.pack(pady=10)

    usernameLabel = tk.Label(master, text="Username", font=(
        "Ärial", 12, "bold"), foreground="black", background='#96D4D4')
    usernameLabel.pack(pady=5)

    MySQLusername = tk.Entry(master, width=30)
    MySQLusername.pack()

    passwordLabel = tk.Label(master, text="Password", font=(
        "Ärial", 12, "bold"),  background='#96D4D4', foreground="black")
    passwordLabel.pack(pady=5)

    MySQLpassword = tk.Entry(master, width=30)
    MySQLpassword.pack()

    def submit():
        user = MySQLusername.get()
        password = MySQLpassword.get()
        det["username"] = user
        det["password"] = password
        master.destroy()

    submitbtn = tk.Button(master, text="Submit", width=19, command=submit, font=(
        "Ärial", 12, "bold"), foreground="#fff", background="#059862")
    submitbtn.pack(pady=25)

    master.mainloop()


mysqlSetUp()

MYUSERNAME = str(det["username"])
MYPASS = str(det["password"])
MYDATABASE = "PMSDB"

# Add your own database name and password here to reflect in the code
mypass = MYPASS
mydatabase = MYDATABASE
myusername = MYUSERNAME


try:
    # Database Connection
    con = mysql.connector.connect(
        host="localhost",
        user=myusername,
        password=mypass
    )
except:
    quit()

cur = con.cursor()
cur.execute(f"CREATE DATABASE IF NOT EXISTS {mydatabase}")
cur.execute(f"USE {mydatabase}")

# Enter Table Names here
studentTable = "student"  # student table
studentEduTable = "studentEdu"  # student education details table
companiesTable = "companies"  # companiesTable


def init():
    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {studentTable} (
    PRN VARCHAR(255) PRIMARY KEY NOT NULL,
    fname VARCHAR(255),
    lname VARCHAR(255),
    gender VARCHAR(255),
    phone_no BIGINT,
    Email VARCHAR(255),
    DOB VARCHAR(255)
    )""")

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {studentEduTable} (
    PRN VARCHAR(255) PRIMARY KEY NOT NULL,
    department VARCHAR(255),
    roll_no VARCHAR(255),
    backlogs INT,
    avg_cgpa FLOAT
    )""")

    cur.execute(f"""
    CREATE TABLE IF NOT EXISTS {companiesTable} (
    company_id VARCHAR(255) PRIMARY KEY NOT NULL,
    company_name VARCHAR(255),
    required_cgpa FLOAT,
    Email VARCHAR(255),
    Phone_No BIGINT
    )""")


class SampleApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack(side="top", fill="both", expand=True)


class StartPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#282A35")

        master.title("Home")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))
        homeHeadingLable = tk.Label(self, text="Welcome to Placement Cell", font=("Ärial", 45, "bold"),
                                    background="#282A35", foreground="white")
        homeHeadingLable.pack(pady=100, padx=25)

        goToStudent = tk.Button(self, text="Student section", command=lambda: master.switch_frame(StudentSection),
                                bg='#059862', fg='#ffffff', font=('Verdana', 20))
        goToStudent.pack(pady=25, ipadx=12)

        goToCompany = tk.Button(self, text="Company section", command=lambda: master.switch_frame(
            CompanySection), bg='#059862', fg='#ffffff', font=('Verdana', 20))
        goToCompany.pack(pady=25)

        quit = tk.Button(self, text="Quit", command=exit,
                         bg='#ffffff', fg='#000000', font=('Verdana', 20))
        quit.pack(pady=25)


class StudentSection(tk.Frame):

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#D9EEE1")
        master.title("Student Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        homeHeadingLable = tk.Label(self, text="Welcome to Student Section", font=("Ärial", 45, "bold"),
                                    background="#D9EEE1", foreground="#000000")
        homeHeadingLable.pack(pady=100, padx=25)

        addStudent = tk.Button(self, text="Add Student Data", command=lambda: master.switch_frame(AddStudentData),
                               bg='#282A35', fg='#ffffff', font=('Verdana', 20))
        addStudent.pack(pady=25, ipadx=60)

        viewStudent = tk.Button(
            self, text="View Student Data", bg='#282A35', fg='#ffffff', command=lambda: master.switch_frame(ViewStudentData),
            font=('Verdana', 20))
        viewStudent.pack(pady=25, ipadx=53)

        removeStudent = tk.Button(
            self, text="Remove Student Data", bg='#282A35', fg='#ffffff', font=('Verdana', 20), command=lambda: master.switch_frame(DeleteStudentData))
        removeStudent.pack(pady=25, ipadx=25)

        viewEligibleCompanies = tk.Button(self, text="view Eligible Companies", bg='#282A35', fg='#ffffff', command=lambda: master.switch_frame(ViewEligibleCompaniesData),
                                          font=('Verdana', 20))
        viewEligibleCompanies.pack(pady=25, ipadx=8)

        backBtn = tk.Button(self, text="back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(StartPage), font=('Verdana', 12))
        backBtn.place(relx=0.41, rely=0.9, relwidth=0.18, relheight=0.08)


class AddStudentData(tk.Frame):
    init()

    def importData(a):
        rows = []
        # print(a)

        def openFile():
            filepath = filedialog.askopenfilename()
            file = open(filepath)
            csvreader = csv.reader(file)
            err = False
            for row in csvreader:
                rows.append(row)
                insertStudents = f"insert into {studentTable} values('{row[0]}','{row[1]}','{row[2]}','{row[9]}',{row[6]},'{row[5]}','{randomDate()}')"
                insertScores = f"insert into {studentEduTable} values('{row[0]}','{row[7]}','{row[3]}',0,{row[4]})"

                try:
                    cur.execute(insertStudents)

                    con.commit()

                    cur.execute(insertScores)

                    con.commit()

                    # print('Success', "Student details added successfully")
                except:
                    err = True
                    # print("Error", "Can't add data into Database Data Already Added")

                    continue
            # print(rows)
            if(not err):
                # print(err)
                messagebox.showinfo(
                    'Success', "Student details added successfully")
            else:
                messagebox.showinfo(
                    "Error", "Can't add data into Database Data Already Added")

            file.close()
            window.destroy()

        window = tk.Tk()
        button = tk.Button(window, text="select csv file", command=openFile)
        button.pack(padx=100, pady=10)
        window.mainloop()

    def studentRegister(a):
        PRN = stdInfo1.get()
        fname = stdInfo2.get()
        fname = fname.capitalize()

        lname = stdInfo3.get()
        lname = lname.capitalize()

        gender = str(defaultGender.get())
        DOB = f"{defaultDate.get()} {defaultMonth.get()} {defaultYear.get()}"
        phone_no = stdInfoPno.get()
        Email = stdInfoEmail.get()
        Email = Email.lower()

        department = defaultDepartment.get()
        roll_no = stdInfo11.get()
        backlogs = str(defaultBacklog.get())
        avg_cgpa = stdInfo13.get()

        insertStudents = f"INSERT INTO {studentTable} VALUES('{PRN}','{fname}','{lname}','{gender}',{phone_no},'{Email}','{DOB}')"
        insertScores = f"INSERT INTO {studentEduTable} VALUES('{PRN}','{department}','{roll_no}',{backlogs},{avg_cgpa})"
        # print(insertStudents)
        # print(insertScores)
        try:
            cur.execute(insertStudents)
            con.commit()
            cur.execute(insertScores)
            con.commit()
            messagebox.showinfo(
                'Success', "Student details added successfully")
        except:
            messagebox.showinfo("Error", "Can't add data into Database")

    def __init__(self, master):
        global stdInfo1, stdInfo2, stdInfo3, stdInfo4, stdInfo5, stdInfo7, stdInfo10, stdInfo11, stdInfo12, stdInfo13, stdInfoPno, stdInfoEmail, Canvas1, con, cur, studentTable, root, studentEduTable, defaultGender, defaultDate, defaultMonth, defaultYear, defaultDepartment, defaultBacklog

        tk.Frame.__init__(self, master, bg="#D9EEE1")
        master.title("Student Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        HeadingLable = tk.Label(self, text="Add student data", font=("Ärial", 45, "bold"),
                                background="#D9EEE1", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        # student ID
        lb1 = tk.Label(self, text="PRN : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb1.place(relx=0.14, rely=0.3, relheight=0.04)

        stdInfo1 = tk.Entry(self)
        stdInfo1.place(relx=0.28, rely=0.3, relwidth=0.59, relheight=0.04)

        # first name
        lb2 = tk.Label(self, text="First Name : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb2.place(relx=0.14, rely=0.35, relheight=0.04)

        stdInfo2 = tk.Entry(self)
        stdInfo2.place(relx=0.28, rely=0.35, relwidth=0.22, relheight=0.04)

        # last name
        lb3 = tk.Label(self, text="Last Name : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb3.place(relx=0.5, rely=0.35, relheight=0.04)

        stdInfo3 = tk.Entry(self)
        stdInfo3.place(relx=0.64, rely=0.35, relwidth=0.23, relheight=0.04)

        # gender
        lb4 = tk.Label(self, text="Gender : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb4.place(relx=0.14, rely=0.40, relheight=0.04)

        defaultGender = tk.StringVar()
        defaultGender.set("Select Your Gender")
        stdInfo4 = tk.OptionMenu(
            self, defaultGender, "Male", "Female", "LGBTQ")
        stdInfo4.pack()
        stdInfo4.place(relx=0.28, rely=0.40, relwidth=0.18, relheight=0.04)

        # date of birth

        lb5 = tk.Label(self, text="DOB : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb5.place(relx=0.5, rely=0.40, relheight=0.04)

        defaultDate = tk.StringVar()
        defaultDate.set("date")
        date = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16,
                17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        stdInfo5 = tk.OptionMenu(self, defaultDate, *date)
        stdInfo5.pack()
        stdInfo5.place(relx=0.61, rely=0.40, relwidth=0.07, relheight=0.04)

        defaultMonth = tk.StringVar()
        defaultMonth.set("month")
        month = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'Semptember', 'November', 'December']
        stdInfo6 = tk.OptionMenu(self, defaultMonth, *month)
        stdInfo6.pack()
        stdInfo6.place(relx=0.68, rely=0.40, relwidth=0.12, relheight=0.04)

        defaultYear = tk.StringVar()
        defaultYear.set("year")
        year = [1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991,
                1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005]
        stdInfo7 = tk.OptionMenu(self, defaultYear, *year)
        stdInfo7.pack()
        stdInfo7.place(relx=0.8, rely=0.40, relwidth=0.07, relheight=0.04)

        # Phone No.
        lbpno = tk.Label(self, text="Phone No. : ", bg="#D9EEE1",
                         fg='#282A35', font=('Verdana', 12, "bold"))
        lbpno.place(relx=0.14, rely=0.45, relheight=0.04)

        stdInfoPno = tk.Entry(self)
        stdInfoPno.place(relx=0.28, rely=0.45, relwidth=0.22, relheight=0.04)

        # last name
        lbEmail = tk.Label(self, text="Email : ", bg="#D9EEE1",
                           fg='#282A40', font=('Verdana', 12, "bold"))
        lbEmail.place(relx=0.5, rely=0.45, relheight=0.04)

        stdInfoEmail = tk.Entry(self)
        stdInfoEmail.place(relx=0.64, rely=0.45, relwidth=0.23, relheight=0.04)

        # educational details
        lb8 = tk.Label(self, text="Educational details", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb8.place(relx=0.14, rely=0.55, relheight=0.04)

        # department

        lb10 = tk.Label(self, text="Department : ", bg="#D9EEE1",
                        fg='#282A35', font=('Verdana', 12, "bold"))
        lb10.place(relx=0.14, rely=0.60, relheight=0.04)
        defaultDepartment = tk.StringVar()
        defaultDepartment.set("Select Department")
        department = ["Computer Science", "Information Technology", "Electronics & Tele.",
                      "Mechanical Engineering", "Civil Engineering", "Bio-Technology", "Chemical Engineering"]
        stdInfo10 = tk.OptionMenu(self, defaultDepartment, *department)
        stdInfo10.pack()
        stdInfo10.place(relx=0.28, rely=0.60, relwidth=0.22, relheight=0.04)

        # rollno
        lb11 = tk.Label(self, text="Roll No : ", bg="#D9EEE1",
                        fg='#282A35', font=('Verdana', 12, "bold"))
        lb11.place(relx=0.5, rely=0.60, relheight=0.04)

        stdInfo11 = tk.Entry(self)
        stdInfo11.place(relx=0.64, rely=0.60, relwidth=0.23, relheight=0.04)

        # backlogs
        lb12 = tk.Label(self, text="Backlogs : ", bg="#D9EEE1",
                        fg='#282A35', font=('Verdana', 12, "bold"))
        lb12.place(relx=0.14, rely=0.65, relheight=0.04)
        defaultBacklog = tk.StringVar()
        defaultBacklog.set("Select No. Of Backlogs")
        backlogs = [0, 1, 2, 3]
        stdInfo12 = tk.OptionMenu(self, defaultBacklog, *backlogs)
        stdInfo12.pack()
        stdInfo12.place(relx=0.28, rely=0.65, relwidth=0.22, relheight=0.04)

        # average cgpa
        lb13 = tk.Label(self, text="Avg CGPA : ", bg="#D9EEE1",
                        fg='#282A35', font=('Verdana', 12, "bold"))
        lb13.place(relx=0.5, rely=0.65, relheight=0.04)

        stdInfo13 = tk.Entry(self)
        stdInfo13.place(relx=0.64, rely=0.65, relwidth=0.23, relheight=0.04)

        # import data from csv
        ImportBtn = tk.Button(self, text="Or Import Data from csv file.", command=self.importData,
                              bg='#FFF4A3', fg='#282A35',  font=('Verdana', 12))
        ImportBtn.place(relx=0.14, rely=0.75, relwidth=0.73, relheight=0.04)

        # Submit tk.Button
        SubmitBtn = tk.Button(self, text="SUBMIT", bg='#059862', command=self.studentRegister,
                              fg='#ffffff',  font=('Verdana', 12))
        SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

        quitBtn = tk.Button(self, text="Back", bg='#059862', fg='#ffffff', command=lambda: master.switch_frame(StudentSection),
                            font=('Verdana', 12))
        quitBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)


class ViewStudentData(tk.Frame):
    init()

    def __init__(self, master):

        tk.Frame.__init__(self, master, bg="#D9EEE1")
        master.title("Student Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        HeadingLable = tk.Label(self, text="Add student data", font=("Ärial", 45, "bold"),
                                background="#D9EEE1", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        view_frame = tk.Frame(self)
        view_frame.pack()

        game_scroll = tk.Scrollbar(view_frame, orient='vertical')
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        viewC = ttk.Treeview(view_frame, height=20)
        viewC.pack()

        style = ttk.Style()
        style.theme_use()
        style.configure("Treeview.Heading", font=(
            'Verdana', 12, 'bold'), rowheight=25)
        style.configure("Treeview", font=('Verdana', 10),
                        rowheight=25,)

        viewC.config(yscrollcommand=game_scroll.set)
        game_scroll.config(command=viewC.yview)
        # game_scroll.config(command=viewC.xview)

        viewC['columns'] = ('PRN', 'Name', 'Department', 'Roll_No.', 'Gender',
                            'Email', "Phone_No.", "Date_of_Birth", "Avg_CGPA", "Backlogs")

        viewC.column("#0", width=0,  stretch='NO')
        viewC.column("PRN", anchor=tk.W, width=120)
        viewC.column("Department", anchor=tk.W, width=170)
        viewC.column("Roll_No.", anchor=tk.W, width=100)
        viewC.column("Name", anchor=tk.W, width=255)
        viewC.column("Gender", anchor=tk.W, width=100)
        viewC.column("Email", anchor=tk.W, width=400)
        viewC.column("Phone_No.", anchor=tk.W, width=130)
        viewC.column("Date_of_Birth", anchor=tk.W, width=160)
        viewC.column("Avg_CGPA", anchor=tk.W, width=130)
        viewC.column("Backlogs", anchor=tk.W, width=120)

        viewC.heading("#0", text="", anchor=tk.W,)
        viewC.heading("PRN", text="PRN", anchor=tk.W)
        viewC.heading("Department", text="Department", anchor=tk.W)
        viewC.heading("Roll_No.", text="Roll No.", anchor=tk.W)
        viewC.heading("Name", text="Name", anchor=tk.W)
        viewC.heading("Gender", text="Gender", anchor=tk.W)
        viewC.heading("Email", text="Email", anchor=tk.W)
        viewC.heading("Phone_No.", text="Phone No.", anchor=tk.W)
        viewC.heading("Date_of_Birth", text="Date of Birth", anchor=tk.W)
        viewC.heading("Avg_CGPA", text="Avg CGPA", anchor=tk.W)
        viewC.heading("Backlogs", text="Backlogs", anchor=tk.W)

        getStudent = f"select * from {studentTable}, {studentEduTable} where {studentTable}.PRN = {studentEduTable}.PRN"
        try:

            cur.execute(getStudent)
            for i in cur:
                viewC.insert(parent='', index='end', iid=i, text='', values=(
                    i[0], f"{i[1]} {i[2]}", i[8], i[9], i[3], i[5], i[4], i[6], i[11], i[10]))
        except:
            messagebox.showinfo("Failed to fetch files from database")

        viewC.pack()

        backBtn = tk.Button(self, text="back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(StudentSection), font=('Verdana', 12))
        backBtn.place(relx=0.41, rely=0.9, relwidth=0.18, relheight=0.08)


class DeleteStudentData(tk.Frame):
    # global removeStudentData

    init()

    # List To store all company IDs

    def removeStudentData(a):
        global allPrn
        allPrn = []

        prn = deletePRNinput.get()
        # print(prn)

        selectStatement = f'SELECT * from {studentTable} WHERE PRN="{prn}";'
        # print(selectStatement)
        try:
            cur.execute(selectStatement)
            for i in cur:
                # print(i)
                allPrn.append(i[0])
            # print(allPrn)

            if prn not in allPrn:
                # print(prn)
                messagebox.showinfo(
                    "Error", "Student with this ID not present")
                return
        except:
            messagebox.showinfo("Error", "Can't fetch Student Data")

        deleteStudentStatement = f'DELETE FROM {studentTable} WHERE PRN="{prn}";'
        deleteStudentEduStatement = f'DELETE FROM {studentEduTable} WHERE PRN="{prn}";'

        try:
            cur.execute(deleteStudentStatement)
            con.commit()
            cur.execute(deleteStudentEduStatement)
            con.commit()
            messagebox.showinfo('Success', "Student removed")

        except:
            messagebox.showinfo(
                "Search Error", "The value entered is wrong, Try again")

    def __init__(self, master):

        tk.Frame.__init__(self, master, bg="#D9EEE1")
        master.title("Student Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        global deletePRNinput

        HeadingLable = tk.Label(self, text="Remove student data", font=("Ärial", 45, "bold"),
                                background="#D9EEE1", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        # student ID
        lb1 = tk.Label(self, text="Enter PRN : ", bg="#D9EEE1",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb1.place(relx=0.12, rely=0.3, relheight=0.04)

        deletePRNinput = tk.Entry(self)
        deletePRNinput.place(relx=0.25, rely=0.3,
                             relwidth=0.62, relheight=0.04)

        # Submit Button
        SubmitBtn = tk.Button(self, text="Remove Student", bg='#059862',
                              fg='#ffffff', command=self.removeStudentData, font=('Verdana', 12))
        SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

        backBtn = tk.Button(self, text="Back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(StudentSection), font=('Verdana', 12))
        backBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)


class ViewEligibleCompaniesData(tk.Frame):
    init()

    def __init__(self, master):

        tk.Frame.__init__(self, master, bg="#D9EEE1")
        master.title("Student Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        HeadingLable = tk.Label(self, text="View Eligible Companies", font=("Ärial", 45, "bold"),
                                background="#D9EEE1", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        PRNinputCompanyLabel = tk.Label(self, text="Enter PRN : ", bg="#D9EEE1",
                                        fg='#282A35', font=('Verdana', 12, "bold"))
        PRNinputCompanyLabel.place(relx=0.193, rely=0.23, relheight=0.04)

        global PRNinputCompany
        PRNinputCompany = tk.Entry(self)
        PRNinputCompany.place(relx=0.27, rely=0.23,
                              relwidth=0.535, relheight=0.04)

        view_frame = tk.Frame(self)
        view_frame.pack()

        game_scroll = tk.Scrollbar(view_frame, orient='vertical')
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        viewC = ttk.Treeview(view_frame, height=20)
        viewC.pack()

        style = ttk.Style()
        style.theme_use()
        style.configure("Treeview.Heading", font=(
            'Verdana', 12, 'bold'), rowheight=25)
        style.configure("Treeview", font=('Verdana', 10),
                        rowheight=25,)

        viewC.config(yscrollcommand=game_scroll.set)
        game_scroll.config(command=viewC.yview)

        viewC['columns'] = ('CID', 'Name', 'Required Score',
                            'email', 'phone_no')

        viewC.column("#0", width=0,  stretch=tk.NO)
        viewC.column("CID", anchor=tk.W, width=100)
        viewC.column("Name", anchor=tk.W, width=300)
        viewC.column("Required Score", anchor=tk.W, width=200)
        viewC.column("email", anchor=tk.W, width=400)
        viewC.column("phone_no", anchor=tk.W, width=150)

        viewC.heading("#0", text="", anchor=tk.W)
        viewC.heading("CID", text="CID", anchor=tk.W)
        viewC.heading("Name", text="Name", anchor=tk.W)
        viewC.heading("Required Score", text="Required Score", anchor=tk.W)
        viewC.heading("email", text="Email", anchor=tk.W)
        viewC.heading("phone_no", text="Phone No.", anchor=tk.W)

        def findCompanies():
            # Database Connection
            con = pymysql.connect(
                host="localhost",
                user=myusername,
                password=mypass
            )

            cur = con.cursor()
            cur.execute(f"USE {mydatabase}")

            allPrn = []

            prn = PRNinputCompany.get()
            prn = prn.upper()
            # print(prn)

            selectStatement = f'SELECT * from {studentTable} WHERE PRN="{prn}";'
            print(selectStatement)
            try:
                cur.execute(selectStatement)
                for i in cur:
                    print(i)
                    allPrn.append(i[0])
                # print(allPrn)

                if prn not in allPrn:
                    print(prn)
                    messagebox.showinfo(
                        "Error", "Student with this ID not present")
                    return
            except:
                messagebox.showinfo("Error", "Can't fetch Student Data")

            PRN = PRNinputCompany.get()
            getCompanies1 = f"SELECT @student_score := avg_cgpa FROM {studentEduTable} WHERE PRN='{PRN}';"
            getCompanies2 = f"SELECT * FROM {companiesTable} WHERE required_cgpa <= @student_score;"
            # print(getCompanies1, getCompanies2)
            try:
                cur.execute(getCompanies1)
                # print(cur)
                con.commit()
                cur.execute(getCompanies2)
                con.commit()

                # print(cur)
                try:
                    for i in cur:
                        # print(i)
                        viewC.insert(parent='', index='end', iid=i,
                                     text='', values=(i[0], i[1], i[2], i[3], i[4]))
                except:
                    if(len(cur.fetchall()) == 0):
                        messagebox.showinfo(
                            "You are not eligible for any companies")

            except:
                messagebox.showinfo("Failed to fetch files from database")

        viewC.config()

        submitBtn = tk.Button(self, text="Search", bg='#059862', command=findCompanies,
                              fg='#ffffff', font=('Verdana', 12, "bold"))
        submitBtn.place(relx=0.25, rely=0.9, relwidth=0.18, relheight=0.08)

        backBtn = tk.Button(self, text="back", bg='#059862', font=('Verdana', 12, "bold"), command=lambda: master.switch_frame(StudentSection),
                            fg='#ffffff')
        backBtn.place(relx=0.50, rely=0.9, relwidth=0.18, relheight=0.08)


class CompanySection(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#FFF4A3")
        master.title("Company Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        homeHeadingLable = tk.Label(self, text="Welcome to Company Section", font=("Ärial", 45, "bold"),
                                    background="#FFF4A3", foreground="#000000")
        homeHeadingLable.pack(pady=100, padx=24)

        addCompany = tk.Button(self, text="Add Company Data", command=lambda: master.switch_frame(AddCompanyData),
                               bg='#282A35', fg='#ffffff', font=('Verdana', 20))
        addCompany.pack(pady=25, ipadx=57)

        viewCompany = tk.Button(
            self, text="View Company Data", bg='#282A35', command=lambda: master.switch_frame(ViewCompanyData), fg='#ffffff', font=('Verdana', 20))
        viewCompany.pack(pady=25, ipadx=50)

        removeCompany = tk.Button(
            self, text="Remove Company Data", bg='#282A35', fg='#ffffff', command=lambda: master.switch_frame(DeleteCompanyData), font=('Verdana', 20))
        removeCompany.pack(pady=25, ipadx=22)

        viewEligibleStudents = tk.Button(self, text="view Eligible Students", command=lambda: master.switch_frame(ViewEligibleStudents), bg='#282A35', fg='#ffffff',
                                         font=('Verdana', 20))
        viewEligibleStudents.pack(pady=25, ipadx=35)

        backBtn = tk.Button(self, text="back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(StartPage), font=('Verdana', 12))
        backBtn.place(relx=0.41, rely=0.9, relwidth=0.18, relheight=0.08)


class AddCompanyData(tk.Frame):
    init()

    def importData(a):
        rows = []

        def openFile():
            filepath = filedialog.askopenfilename()
            file = open(filepath)
            csvreader = csv.reader(file)
            err = False
            for row in csvreader:
                rows.append(row)

                insertCompany = f"insert into {companiesTable} values({row[0]},'{row[1]}',{(row[2])},'{row[3]}',{row[4]})"

                try:
                    # print(insertCompany)
                    cur.execute(insertCompany)
                    con.commit()

                except:
                    err = True

            # print(rows)
            if(not err):
                # print(err)
                messagebox.showinfo(
                    'Success', "Student details added successfully")
            else:
                messagebox.showinfo(
                    "Error", "Can't add data into Database Data Already Added")

            file.close()
            window.destroy()

        window = tk.Tk()
        button = tk.Button(window, text="select csv file", command=openFile)
        button.pack(padx=100, pady=10)
        window.mainloop()

    def AddCompany(a):
        company_id = compInfo1.get()
        company_name = compInfo2.get()
        required_cgpa = compInfo3.get()
        Email = compInfo4.get()
        Email = Email.lower()
        phone_no = compInfo5.get()

        insertCompany = f"INSERT INTO {companiesTable} VALUES('{company_id}', '{company_name}', {required_cgpa},'{Email}',{phone_no})"
        try:
            cur.execute(insertCompany)
            con.commit()
            messagebox.showinfo(
                'Success', "Company details added successfully")
        except:
            messagebox.showinfo("Error", "Can't add data into Database")

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#FFF4A3")
        master.title("Company Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        homeHeadingLable = tk.Label(self, text="Add Company Data", font=("Ärial", 45, "bold"),
                                    background="#FFF4A3", foreground="#000000")
        homeHeadingLable.pack(pady=100, padx=24)

        global compInfo1, compInfo2, compInfo3, compInfo4, compInfo5

        # # companyId
        cidLabel = tk.Label(self, text="CID : ", bg="#FFF4A3",
                            fg='#282A35', font=('Verdana', 12, "bold"))
        cidLabel.place(relx=0.1, rely=0.3, relheight=0.04)

        compInfo1 = tk.Entry(self)
        compInfo1.place(relx=0.3, rely=0.3, relwidth=0.62, relheight=0.04)

        # company name
        cNameLabel = tk.Label(self, text="Name : ", bg="#FFF4A3",
                              fg='#282A35', font=('Verdana', 12, "bold"))
        cNameLabel.place(relx=0.1, rely=0.35, relheight=0.04)

        compInfo2 = tk.Entry(self)
        compInfo2.place(relx=0.3, rely=0.35, relwidth=0.62, relheight=0.04)

        # required score
        cCGPALabel = tk.Label(self, text="Required_Score : ", bg="#FFF4A3",
                              fg='#282A35', font=('Verdana', 12, "bold"))
        cCGPALabel.place(relx=0.1, rely=0.40, relheight=0.04)

        compInfo3 = tk.Entry(self)
        compInfo3.place(relx=0.3, rely=0.40, relwidth=0.62, relheight=0.04)

        # email
        cEmailLabel = tk.Label(self, text="Email : ", bg="#FFF4A3",
                               fg='#282A35', font=('Verdana', 12, "bold"))
        cEmailLabel.place(relx=0.1, rely=0.45, relheight=0.04)

        compInfo4 = tk.Entry(self)
        compInfo4.place(relx=0.3, rely=0.45, relwidth=0.62, relheight=0.04)

        # phone no
        cPhoneNoLabel = tk.Label(self, text="Phone No. : ", bg="#FFF4A3",
                                 fg='#282A35', font=('Verdana', 12, "bold"))
        cPhoneNoLabel.place(relx=0.1, rely=0.50, relheight=0.04)

        compInfo5 = tk.Entry(self)
        compInfo5.place(relx=0.3, rely=0.50, relwidth=0.62, relheight=0.04)

        # import data
        # import data from csv
        ImportBtn = tk.Button(self, text="Or Import Data from csv file.", command=self.importData,
                              bg='#D9EEE1', fg='#282A35', font=('Verdana', 12))
        ImportBtn.place(relx=0.14, rely=0.75, relwidth=0.73, relheight=0.04)

        # Submit tk.Button
        SubmitBtn = tk.Button(self, text="SUBMIT", bg='#059862', command=self.AddCompany,
                              fg='#ffffff',  font=('Verdana', 12))
        SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

        backBtn = tk.Button(self, text="back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(CompanySection), font=('Verdana', 12))
        backBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)


class ViewCompanyData(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#FFF4A3")
        master.title("Company Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        homeHeadingLable = tk.Label(self, text="Company Data", font=("Ärial", 45, "bold"),
                                    background="#FFF4A3", foreground="#000000")
        homeHeadingLable.pack(pady=100, padx=24)

        view_frame = tk.Frame(self)
        view_frame.pack()

        game_scroll = tk.Scrollbar(view_frame, orient='vertical')
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        viewC = ttk.Treeview(view_frame, height=20)
        viewC.pack()

        style = ttk.Style()
        style.theme_use()
        style.configure("Treeview.Heading", font=(
            'Verdana', 12, 'bold'), rowheight=25)
        style.configure("Treeview", font=('Verdana', 10),
                        rowheight=25,)

        viewC.config(yscrollcommand=game_scroll.set)
        game_scroll.config(command=viewC.yview)

        viewC['columns'] = ('CID', 'Name', 'Required Score',
                            'email', 'phone_no')

        viewC.column("#0", width=0,  stretch=tk.NO)
        viewC.column("CID", anchor=tk.W, width=100)
        viewC.column("Name", anchor=tk.W, width=300)
        viewC.column("Required Score", anchor=tk.W, width=200)
        viewC.column("email", anchor=tk.W, width=400)
        viewC.column("phone_no", anchor=tk.W, width=150)

        viewC.heading("#0", text="", anchor=tk.W)
        viewC.heading("CID", text="CID", anchor=tk.W)
        viewC.heading("Name", text="Name", anchor=tk.W)
        viewC.heading("Required Score", text="Required Score", anchor=tk.W)
        viewC.heading("email", text="Email", anchor=tk.W)
        viewC.heading("phone_no", text="Phone No.", anchor=tk.W)

        getCompany = f"SELECT * FROM {companiesTable}"
        try:
            cur.execute(getCompany)
            for i in cur:
                # print(i)
                viewC.insert(parent='', index='end', iid=i, text='',
                             values=(i[0], i[1], i[2], i[3], i[4]))
        except:
            messagebox.showinfo("Failed to fetch files from database")

        viewC.pack()

        backBtn = tk.Button(self, text="back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(CompanySection), font=('Verdana', 12))
        backBtn.place(relx=0.41, rely=0.9, relwidth=0.18, relheight=0.08)


class DeleteCompanyData(tk.Frame):

    init()

    # List To store all company IDs

    def removeCompanyData(a):

        allCID = []

        cid = deletePRNinput.get()
        # print(cid)

        selectStatement = f'SELECT * from {companiesTable} WHERE company_id="{cid}";'
        # print(selectStatement)
        try:
            cur.execute(selectStatement)
            for i in cur:
                # print(i)
                allCID.append(i[0])
            # print(allCID)

            if cid not in allCID:
                messagebox.showinfo(
                    "Error", "Company with this ID is not present")
                return
        except:
            messagebox.showinfo("Error", "Can't fetch Company Data")

        deleteCompanyDataStatement = f'DELETE FROM {companiesTable} WHERE company_id="{cid}";'

        try:
            cur.execute(deleteCompanyDataStatement)
            con.commit()
            messagebox.showinfo('Success', "Company data removed")

        except:
            messagebox.showinfo(
                "Search Error", "The value entered is wrong, Try again")

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#FFF4A3")
        master.title("Company Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        global deletePRNinput

        HeadingLable = tk.Label(self, text="Remove Company data", font=("Ärial", 45, "bold"),
                                background="#FFF4A3", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        # student ID
        lb1 = tk.Label(self, text="Enter CID : ", bg="#FFF4A3",
                       fg='#282A35', font=('Verdana', 12, "bold"))
        lb1.place(relx=0.12, rely=0.3, relheight=0.04)

        deletePRNinput = tk.Entry(self)
        deletePRNinput.place(relx=0.25, rely=0.3,
                             relwidth=0.62, relheight=0.04)

        # Submit Button
        SubmitBtn = tk.Button(self, text="Remove Company", bg='#059862',
                              fg='#ffffff', command=self.removeCompanyData, font=('Verdana', 12))
        SubmitBtn.place(relx=0.28, rely=0.9, relwidth=0.18, relheight=0.08)

        backBtn = tk.Button(self, text="Back", bg='#059862', fg='#ffffff',
                            command=lambda: master.switch_frame(CompanySection), font=('Verdana', 12))
        backBtn.place(relx=0.53, rely=0.9, relwidth=0.18, relheight=0.08)


class ViewEligibleStudents(tk.Frame):
    init()

    def __init__(self, master):
        tk.Frame.__init__(self, master, bg="#FFF4A3")
        master.title("Company Section")
        master.minsize(width=1080, height=720)
        master.state("zoomed")
        master.iconphoto(False,
                         tk.PhotoImage(file="businessman.png"))

        HeadingLable = tk.Label(self, text="Find Eligible Students", font=("Ärial", 45, "bold"),
                                background="#FFF4A3", foreground="#000000")
        HeadingLable.pack(pady=100, padx=25)

        CIDInputStudentsLabel = tk.Label(self, text="Enter CID : ", bg="#FFF4A3",
                                         fg='#282A35', font=('Verdana', 12, "bold"))
        CIDInputStudentsLabel.place(relx=0.193, rely=0.23, relheight=0.04)

        global CIDInputStudent
        CIDInputStudent = tk.Entry(self)
        CIDInputStudent.place(relx=0.27, rely=0.23,
                              relwidth=0.535, relheight=0.04)

        view_frame = tk.Frame(self)
        view_frame.pack()

        game_scroll = tk.Scrollbar(view_frame, orient='vertical')
        game_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        viewC = ttk.Treeview(view_frame, height=20)
        viewC.pack()

        style = ttk.Style()
        style.theme_use()
        style.configure("Treeview.Heading", font=(
            'Verdana', 12, 'bold'), rowheight=25)
        style.configure("Treeview", font=('Verdana', 10),
                        rowheight=25,)

        viewC.config(yscrollcommand=game_scroll.set)
        game_scroll.config(command=viewC.yview)
        # game_scroll.config(command=viewC.xview)

        viewC['columns'] = ('PRN', 'Name', 'Department',  'Gender',
                            'Email', "Phone_No.",  "Avg_CGPA")

        viewC.column("#0", width=0,  stretch='NO')
        viewC.column("PRN", anchor=tk.W, width=120)
        viewC.column("Department", anchor=tk.W, width=170)
        viewC.column("Name", anchor=tk.W, width=255)
        viewC.column("Gender", anchor=tk.W, width=100)
        viewC.column("Email", anchor=tk.W, width=400)
        viewC.column("Phone_No.", anchor=tk.W, width=130)
        viewC.column("Avg_CGPA", anchor=tk.W, width=130)

        viewC.heading("#0", text="", anchor=tk.W,)
        viewC.heading("PRN", text="PRN", anchor=tk.W)
        viewC.heading("Department", text="Department", anchor=tk.W)
        viewC.heading("Name", text="Name", anchor=tk.W)
        viewC.heading("Gender", text="Gender", anchor=tk.W)
        viewC.heading("Email", text="Email", anchor=tk.W)
        viewC.heading("Phone_No.", text="Phone No.", anchor=tk.W)
        viewC.heading("Avg_CGPA", text="Avg CGPA", anchor=tk.W)

        def findStudents():
            # Database Connection
            con = pymysql.connect(
                host="localhost",
                user=myusername,
                password=mypass
            )

            cur = con.cursor()
            cur.execute(f"USE {mydatabase}")

            cid = CIDInputStudent.get()
            allCID = []

            selectStatement = f'SELECT * from {companiesTable} WHERE company_id="{cid}";'
            # print(selectStatement)
            try:
                cur.execute(selectStatement)
                for i in cur:
                    # print(i)
                    allCID.append(i[0])
                # print(allCID)

                if cid not in allCID:
                    messagebox.showinfo(
                        "Error", "Company with this ID is not present")
                    return
            except:
                messagebox.showinfo("Error", "Can't fetch Company Data")

            getStudent1 = f'''
                            SELECT @required_cgpa := required_cgpa from {companiesTable} where company_id={cid};'''

            getStudent2 = f'''select * from {studentTable}, {studentEduTable} where {studentTable}.PRN = {studentEduTable}.PRN AND {studentEduTable}.avg_cgpa >= @required_cgpa;'''

            try:
                cur.execute(getStudent1)
                con.commit()
                cur.execute(getStudent2)
                con.commit()
                for i in cur:
                    # print(i)
                    viewC.insert(parent='', index='end', iid=i, text='', values=(
                        i[0], f"{i[1]} {i[2]}", i[8], i[3], i[5], i[4], i[11]))
            except:
                messagebox.showinfo("Failed to fetch files from database")

        viewC.pack()

        submitBtn = tk.Button(self, text="Search", bg='#059862', command=findStudents,
                              fg='#ffffff', font=('Verdana', 12, "bold"))
        submitBtn.place(relx=0.25, rely=0.9, relwidth=0.18, relheight=0.08)

        backBtn = tk.Button(self, text="back", bg='#059862', font=('Verdana', 12, "bold"), command=lambda: master.switch_frame(CompanySection),
                            fg='#ffffff')
        backBtn.place(relx=0.50, rely=0.9, relwidth=0.18, relheight=0.08)


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()

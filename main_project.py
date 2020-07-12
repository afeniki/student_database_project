import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter.ttk import *
from PIL import ImageTk, Image
import pymysql
import os
import shutil
import config_project





def on_tab_selected(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")

    if tab_text == "All  Students Records":
        print("All Records Tab Selected")
    if tab_text == "Add New Records":
        print("Add New Records Tab Selected")


def connection():
    return pymysql.connect(host=config_project.DB_SERVER,
                           user=config_project.DB_USER,
                           password=config_project.DB_PASS,
                           database=config_project.DB)


# Function to connect to database
def load_database_results():
    global rows
    global num_of_rows
    try:
        con = connection()

        # input your query
        sql = "SELECT * FROM tbl_student"
        cursor = con.cursor()
        # execute your query
        cursor.execute(sql)  # this goes out to pull all the messages sent from the database
        rows = cursor.fetchall()
        num_of_rows = cursor.rowcount
        cursor.close()
        con.close()
        has_loaded_successfully = True
        messagebox.showinfo("Connected to Database!")
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    return has_loaded_successfully


# load_database_results()

def database_error(err):
    messagebox.showinfo("Error", err)
    return False


def image_path(file_path):
    open_image = Image.open(file_path)
    image = ImageTk.PhotoImage(open_image)
    return image

def load_photo_tab_one(file_path):
    global imgLabelTabOne

    image = image_path(file_path)
    imgLabelTabOne.configure(image=image)
    imgLabelTabOne.image = image

def select_image():
    global image_selected
    global image_file_name
    global file_new_home
    global file_to_copy

    path_to_image = filedialog.askopenfilename(initialdir="/",
                                               title="Openfile",
                                               filetypes=(("PNGs", "*.png"), ("GIFs", "*.gif"),
                                                          ("ALL Files", "*.*")))
    try:
        if path_to_image:
            image_file_name = os.path.basename(path_to_image)  # this extracts the name of the fiile
            file_new_home = config_project.PHOTO_DIRECTORY + image_file_name
            file_to_copy = path_to_image  # contains the original path of the file
            image_selected = True
            load_photo_tab_one(file_to_copy)

    except IOError as err:
        image_selected = False
        messagebox.showinfo("File Error", err)


# Function to insert into database
def insert_database(sun_name_field, first_name_field, middle_name_field, phone_number_field, email_address_field,
                    gender_field,
                    first_course_field,
                    second_course_field,
                    first_duration_field,
                    second_duration_field,
                    amount_first_course_field,
                    amount_second_course_field,
                    total_amount_field,
                    photo_field):
    try:
        con = connection()
        sql = "INSERT INTO tbl_student(SurnName, FirstName, MiddleName," \
              "PhoneNumber, EmailAddress, Gender, 1stCourse, 2ndCourse, Duration_1stCourse," \
              "Duration2ndCourse, Amount_1stCourse, Amount_2ndCourse, Total_Amount, Photo)" \
              "Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        vals = (sun_name_field, first_name_field, middle_name_field, phone_number_field, email_address_field,
                gender_field,
                first_course_field,
                second_course_field,
                first_duration_field,
                second_duration_field,
                amount_first_course_field,
                amount_second_course_field,
                total_amount_field,
                photo_field)
        cursor = con.cursor()
        cursor.execute(sql, vals)
        con.commit()
        cursor.close()
        con.close()

        messagebox.showinfo("Successful Addition", "Record Has Been Added to Database")
    except pymysql.InternalError as e:
        database_error(e)
    except pymysql.OperationalError as e:
        database_error(e)
    except pymysql.ProgrammingError as e:
        database_error(e)
    except pymysql.DataError as e:
        database_error(e)
    except pymysql.IntegrityError as e:
        database_error(e)
    except pymysql.NotSupportedError as e:
        database_error(e)


def add_new_record():
    global blank_text_boxes_tab_two
    global file_new_home
    global file_to_copy
    blank_text_box_count = 0
    if SurName_For_TabOne.get() is "":
        blank_text_box_count += 1
    if FirstName_For_TabOne.get() is "":
        blank_text_box_count += 1
    if MiddleName_For_TabOne.get() is "":
        blank_text_box_count += 1
    if PhoneNumber_For_TabOne.get() is "":
        blank_text_box_count += 1
    if Email_For_TabOne.get() is "":
        blank_text_box_count += 1
    if Gender_For_TabOne.get() is "":
        blank_text_box_count += 1
    if course_1.get() is "":
        blank_text_box_count += 1
    if First_Duration_For_TabOne.get() is "":
        blank_text_box_count += 1
    if First_Amount_For_TabOne.get() is "":
        blank_text_box_count += 1
    if course_2.get() is "":
        blank_text_box_count += 1
    if Second_Duration_For_TabOne.get() is "":
        blank_text_box_count += 1
    if Second_Amount_For_TabOne.get() is "":
        blank_text_box_count += 1
    if Total_Amount_For_TabOne.get() is "":
        blank_text_box_count += 1

    if blank_text_box_count > 0:
        blank_text_boxes_tab_two = True
        messagebox.showinfo("Entry Error", "Blank Text boxes")
    elif blank_text_box_count is 0:
        blank_text_boxes_tab_two = False

        if image_selected:
            try:
                shutil.copy(file_to_copy, file_new_home)
            except shutil.SameFileError:
                pass
            insert_database(
                            SurName_For_TabOne.get(),
                            FirstName_For_TabOne.get(),
                            MiddleName_For_TabOne.get(),
                            PhoneNumber_For_TabOne.get(),
                            Email_For_TabOne.get(),
                            Gender_For_TabOne.get(),
                            course_1.get(),
                            course_2.get(),
                            First_Duration_For_TabOne.get(),
                            Second_Duration_For_TabOne.get(),
                            First_Amount_For_TabOne.get(),
                            Second_Amount_For_TabOne.get(),
                            Total_Amount_For_TabOne.get(),
                            image_file_name)
        else:
            messagebox.showinfo("File Error", "Please Select an Image")

def delete():
    global delete_box
    try:
        con = connection()
        cursor = con.cursor()
        cursor.execute("DELETE from tbl_student WHERE ID= " + delete_box.get())

        delete_box.delete(0, tk.END)

        con.commit()
        messagebox.showinfo('Delete Status', ' Successful Deletion of Record')
        has_loaded_successfully = True
        con.close()
    except pymysql.InternalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.OperationalError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.ProgrammingError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.DataError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.IntegrityError as e:
        has_loaded_successfully = database_error(e)
    except pymysql.NotSupportedError as e:
        has_loaded_successfully = database_error(e)
    return has_loaded_successfully


def scroll_data():
    SurName_For_TabOne.set(rows[column_counter][1])
    FirstName_For_TabOne.set(rows[column_counter][2])
    MiddleName_For_TabOne.set(rows[column_counter][3])
    PhoneNumber_For_TabOne .set(rows[column_counter][4])
    Email_For_TabOne.set(rows[column_counter][5])
    Gender_For_TabOne.set(rows[column_counter][6])
    course_2.set(rows[column_counter][7])
    course_1.set(rows[column_counter][8])
    First_Duration_For_TabOne.set(rows[column_counter][9])
    First_Amount_For_TabOne.set(rows[column_counter][10])
    Second_Duration_For_TabOne.set(rows[column_counter][11])
    Second_Amount_For_TabOne.set(rows[column_counter][12])
    Total_Amount_For_TabOne.set(rows[column_counter][13])

    try:
        ph_path = config_project.PHOTO_DIRECTORY + rows[column_counter][14]
        load_photo_tab_one(ph_path)
    except FileNotFoundError:
        load_photo_tab_one(config_project.PHOTO_DIRECTORY + file_name)


def scroll_right():
    global column_counter
    global num_of_rows

    if column_counter >= (num_of_rows - 1):
        messagebox.showinfo("Database Error", "End of Database")
    else:
        column_counter = column_counter + 1
        scroll_data()


def scroll_left():
    global column_counter
    if column_counter is 0:
        messagebox.showinfo("Database Error", "End of Database")
    else:
        column_counter = column_counter - 1
        scroll_data()


# Total amount function
def total_am():
    print("amountEntryTabOne.get() " + amountEntryTabOne.get())
    print("amount2EntryTabOne.get() " + amount2EntryTabOne.get())
    a = float(amountEntryTabOne.get())
    b = float(amount2EntryTabOne.get())
    answer = a + b
    print("answer" + str(answer))
    totalamountEntryTabOne.insert(0, answer)

# Function to display records
def display():
    success = load_database_results()
    if success:
        SurName_For_TabOne.set(rows[0][1])
        FirstName_For_TabOne.set(rows[0][2])
        MiddleName_For_TabOne.set(rows[0][3])
        PhoneNumber_For_TabOne.set(rows[0][4])
        Email_For_TabOne.set(rows[0][5])
        Gender_For_TabOne.set(rows[0][6])
        course_1.set(rows[0][7])
        course_2.set(rows[0][8])
        First_Duration_For_TabOne.set(rows[0][9])
        Second_Duration_For_TabOne.set(rows[0][10])
        First_Amount_For_TabOne.set(rows[0][11])
        Second_Amount_For_TabOne.set(rows[0][12])
        Total_Amount_For_TabOne.set(rows[0][13])
        photo_path = config_project.PHOTO_DIRECTORY + rows[0][14]
        load_photo_tab_one(photo_path)

# Function to clear registration form
def clear():
    LastEntryTabOne.delete(0, tk.END)
    firstEntryTabOne.delete(0, tk.END)
    middleEntryTabOne.delete(0, tk.END)
    phoneEntryTabOne.delete(0, tk.END)
    emailEntryTabOne.delete(0, tk.END)
    genderEntryTabOne.delete(0, tk.END)
    courseEntryTabOne.delete(0, tk.END)
    durationEntryTabOne.delete(0, tk.END)
    amountEntryTabOne.delete(0, tk.END)
    course2EntryTabOne.delete(0, tk.END)
    duration2EntryTabOne.delete(0, tk.END)
    amount2EntryTabOne.delete(0, tk.END)
    totalamountEntryTabOne.delete(0, tk.END)


# SEARCH METHOD
def search_records():
    global search_text_var
    global options_var
    try:

        con = connection()
        sql_query = "SELECT * FROM tbl_student WHERE FirstName=%s AND 1stCourse=%s"
        vals = (search_text_var.get(), options_var.get())
        cursor = con.cursor()
        cursor.execute(sql_query, vals)
        my_rows = cursor.fetchall()
        total_rows = cursor.rowcount
        cursor.close()
        con.close()
        messagebox.showinfo("TOTAL FOUND: ", 'Record Found:' + str(total_rows) + " " + "\n\n" + str(my_rows))
    except pymysql.InternalError as e:
        database_error(e)
    except pymysql.OperationalError as e:
        database_error(e)
    except pymysql.ProgrammingError as e:
        database_error(e)
    except pymysql.DataError as e:
        database_error(e)
    except pymysql.IntegrityError as e:
        database_error(e)
    except pymysql.NotSupportedError as e:
        database_error(e)


file_name = "default.png"
path = config_project.PHOTO_DIRECTORY + file_name
rows = None  # none is an object that contains nothing
num_of_rows = None
column_counter=0


image_selected = False
image_file_name = None
file_to_copy = None
file_new_home = None
blank_text_boxes_tab_two = False

form =tk.Tk()
form.title("Student's Database")
form.geometry("1200x480")
tab_parent = ttk.Notebook(form)
tab_1 = ttk.Frame(tab_parent)
tab_2 = ttk.Frame(tab_parent)

tab_parent.bind("<<NotebookTabChanged>>")

tab_parent.add(tab_1, text="All  Students Records")
tab_parent.add(tab_2, text="Search")

course_2 = tk.StringVar()
course_1 = tk.StringVar()
SurName_For_TabOne = tk.StringVar()
FirstName_For_TabOne = tk.StringVar()
MiddleName_For_TabOne = tk.StringVar()
PhoneNumber_For_TabOne = tk.StringVar()
Email_For_TabOne = tk.StringVar()
Gender_For_TabOne = tk.StringVar()
First_Duration_For_TabOne = tk.StringVar()
First_Amount_For_TabOne = tk.StringVar()
Second_Duration_For_TabOne = tk.StringVar()
Second_Amount_For_TabOne = tk.StringVar()
Total_Amount_For_TabOne = tk.StringVar()


# First DropDOwn Menu
courses = ['course', 'Python', 'Web Development', 'COMPTIA', 'CCNA', 'ORACLE', 'Java']
course_1.set(courses[0])

popupmenue = OptionMenu(tab_1, course_1, *courses)
popupmenue.config(width=20)
Label(tab_1, text="choose a course :").grid(row=3, column=1, padx=15, pady=15)
popupmenue.grid(row=3, column=2, padx=15, pady=15)

# second dropdown
courses = ['course', 'Python', 'Web Development', 'COMPTIA', 'ORACLE', 'CCNA', 'Java']
course_2.set(courses[0])

popupmenue = OptionMenu(tab_1, course_2, *courses)
popupmenue.config(width=20)
Label(tab_1, text="choose a course :").grid(row=3, column=3, padx=15, pady=15)
popupmenue.grid(row=3, column=4, padx=15, pady=15)

heading = tk.Label(tab_1, text="STUDENT REGISTRATION FORM", font=('Helvetica', 16), width=30, anchor="c")
LastLabelTabOne = tk.Label(tab_1, text="Surname")
firstLabelTabOne = tk.Label(tab_1, text="FirstName")
middleLabelTabOne = tk.Label(tab_1, text="MiddleName")
phoneLabelTabOne = tk.Label(tab_1, text="Phone number")
emailLabelTabOne = tk.Label(tab_1, text="Email Address")
genderLabelTabOne = tk.Label(tab_1, text="Gender")
courseLabelTabOne = tk.Label(tab_1, text="1st Course of Study")
durationLabelTabOne = tk.Label(tab_1, text="Duration of 1st Course of Study")
amountLabelTabOne = tk.Label(tab_1, text="Amount Paid for 1st Course")
course2LabelTabOne = tk.Label(tab_1, text="2nd Course of Study")
duration2LabelTabOne = tk.Label(tab_1, text="Duration of 2nd Course of Study")
amount2LabelTabOne = tk.Label(tab_1, text="Amount Paid for 2nd Course")
totalamountLabelTabOne = tk.Label(tab_1, text="Total Amount Paid")
delete_Label = tk.Label(tab_1, text=' Enter ID number :').grid(row=7, column=4, pady=(180, 0))
Id_Label = tk.Label(tab_1, text="Student ID :").grid(row=3, column=5)

LastEntryTabOne = tk.Entry(tab_1, textvariable=SurName_For_TabOne)
firstEntryTabOne = tk.Entry(tab_1, textvariable=FirstName_For_TabOne)
middleEntryTabOne = tk.Entry(tab_1, textvariable=MiddleName_For_TabOne)
phoneEntryTabOne = tk.Entry(tab_1, textvariable=PhoneNumber_For_TabOne)
emailEntryTabOne = tk.Entry(tab_1, textvariable=Email_For_TabOne)
genderEntryTabOne = tk.Entry(tab_1, textvariable=Gender_For_TabOne)
courseEntryTabOne = tk.Entry(tab_1, textvariable=course_1)
durationEntryTabOne = tk.Entry(tab_1, textvariable=First_Duration_For_TabOne)
amountEntryTabOne = tk.Entry(tab_1, textvariable=First_Amount_For_TabOne)
course2EntryTabOne = tk.Entry(tab_1, textvariable=course_2)
duration2EntryTabOne = tk.Entry(tab_1, textvariable=Second_Duration_For_TabOne)
amount2EntryTabOne = tk.Entry(tab_1, textvariable=Second_Amount_For_TabOne)
totalamountEntryTabOne = tk.Entry(tab_1, textvariable=Total_Amount_For_TabOne)
Id_Entry = tk.Entry(tab_1, textvariable=Id_Label).grid(row=3, column=6)


openImageTabOne = Image.open(path)
imgTabOne = ImageTk.PhotoImage(openImageTabOne, master=tab_1)
imgLabelTabOne = tk.Label(tab_1, image=imgTabOne)

# Buttons
buttonAmount = tk.Button(tab_1, text="total amount", command=total_am)
buttonAddImage = tk.Button(tab_1, text="Add Image", command=select_image)
buttonAddRecord = tk.Button(tab_1, text="Add New Record", command=add_new_record)
buttonDisplay = tk.Button(tab_1, text='Display Records', command=display)#
buttonDelete = tk.Button(tab_1, text="Delete Record", command=delete)
buttonClear = tk.Button(tab_1, text='Clear', command=clear)#
buttonPrevious = tk.Button(tab_1, text='Previous Records', command=scroll_left)
buttonNext = tk.Button(tab_1, text='Next Records', command=scroll_right)


# WIDGETS

heading.grid(row=0, column=2, columnspan=4)
LastLabelTabOne.grid(row=1, column=1, padx=15, pady=15)
LastEntryTabOne.grid(row=1, column=2, padx=15, pady=15)
firstLabelTabOne.grid(row=1, column=3, padx=15, pady=15)
firstEntryTabOne.grid(row=1, column=4, padx=15, pady=15)
middleLabelTabOne.grid(row=1, column=5, padx=15, pady=15)
middleEntryTabOne.grid(row=1, column=6, padx=15, pady=15)
phoneLabelTabOne.grid(row=2, column=1, padx=15, pady=15)
phoneEntryTabOne.grid(row=2, column=2, padx=15, pady=15)
emailLabelTabOne.grid(row=2, column=3, padx=15, pady=15)
emailEntryTabOne.grid(row=2, column=4, padx=15, pady=15)
genderLabelTabOne.grid(row=2, column=5, padx=15, pady=15)
genderEntryTabOne.grid(row=2, column=6, padx=15, pady=15)
durationLabelTabOne.grid(row=4, column=1, padx=15, pady=15)
durationEntryTabOne.grid(row=4, column=2, padx=15, pady=15)
duration2LabelTabOne.grid(row=4, column=3, padx=15, pady=15)
duration2EntryTabOne.grid(row=4, column=4, padx=15, pady=15)
amountLabelTabOne.grid(row=5, column=1, padx=15, pady=15)
amountEntryTabOne.grid(row=5, column=2, padx=15, pady=15)
amount2LabelTabOne.grid(row=5, column=3, padx=15, pady=15)
amount2EntryTabOne.grid(row=5, column=4, padx=15, pady=15)
totalamountEntryTabOne.grid(row=6, column=3, padx=15, pady=15)
delete_box = Entry(tab_1, width=30,)
delete_box.grid(row=7, column=5, pady=(180, 0))

imgLabelTabOne.grid(row=0, column=0, rowspan=3, padx=20, pady=20)

buttonAddRecord.grid(row=7, column=3, padx=15, pady=(200, 0))
buttonAmount.grid(row=6, column=2, padx=15, pady=15)
buttonAddImage.grid(row=4, column=0)
buttonDisplay.grid(row=7, column=1, padx=15, pady=(200, 0))
buttonDelete.grid(row=8, column=5)

buttonClear.grid(row=7, column=2, pady=(200, 0))
buttonPrevious.grid(row=7, column=0, pady=(200, 0))
buttonNext.grid(row=7, column=6, pady=(200, 0))

# Second Tab
search_text_var = tk.StringVar()
search_family = tk.Entry(tab_2, textvariable=search_text_var)

contents = {'ORACLE', 'JAVA', 'Python', 'Web Development', 'COMPTIA', 'CCNA'}


options_var = tk.StringVar()

options_var.set("Select 1stCourse")
dropdown = tk.OptionMenu(tab_2, options_var, *contents)

buttonSearch = tk.Button(tab_2, text='Search', command=search_records)

search_family.grid(row=0, column=0, padx=15, pady=15)
dropdown.grid(row=0, column=1, padx=15, pady=15)
buttonSearch.grid(row=0, column=2, padx=15, pady=15)

#create an update
editButton = Button(tab_2, text='EDIT RECORDS')
editButton.grid(row=1, column=0, columnspan=3, ipadx=135)


tab_parent.pack(expand=1, fill="both")
form.mainloop()






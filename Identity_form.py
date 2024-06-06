import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import ctypes
import sqlite3
#Jumping to the next field with Enter
def jump_to_next_entry(event):
    event.widget.tk_focusNext().focus()
#Jumping to the previous field with Shift + Enter
def jump_to_previous_entry(event):
    event.widget.tk_focusPrev().focus()
#Disabling house wife form the job list while selcting male gender
def define_jobs():
    if gender.get() == "Male":
        dropdown_job["values"]=["Student", "Worker", "Employee", "Self employed"] #can be done with config
    else:
        dropdown_job["values"]=["Student", "Worker", "Employee", "Self employed", "House wife"]
#Disabling salary fields for student and house wife jobs
def define_salary_status(event):
    if dropdown_job.get() in ["Student", "House wife"]:
        text_salary.delete(0,tk.END)
        text_salary.config(state="disabled")
        text_tax.delete(0,tk.END)
        text_tax.config(state="disabled")
        text_insurance.delete(0,tk.END)
        text_insurance.config(state="disabled")
        text_netsalary.config(state="normal")
        text_netsalary.delete(0,tk.END)
        text_netsalary.config(state="disabled")
    else:
        text_salary.config(state="normal")
        text_tax.config(state="normal")
        text_insurance.config(state="normal")
#Calculating and inserting net salary and moving to the next field by clicking Enter on tax field
def calculate_net_salary(event):
    try:
        net_salary = float(text_salary.get()) * (1 - (float(text_tax.get()) + float(text_insurance.get())) / 100)
        text_netsalary.config(state="normal")
        text_netsalary.delete(0, tk.END)
        if net_salary >= 0.01 * float(text_salary.get()):
            text_netsalary.insert(0,f"{int(net_salary):,}")  
        else:
            text_netsalary.insert(0,"")
        text_netsalary.config(state="disabled")
        event.widget.tk_focusNext().focus()
    except:
        text_netsalary.config(state="normal")
        text_netsalary.delete(0, tk.END)
        text_netsalary.config(state="disabled")
        event.widget.tk_focusNext().focus()
#Activating save button by checking accept field and making sure that net salary has been inserted
def activate_save():
    if accept.get() == 1:
        save_button.config(state="normal")
        try:
            net_salary = float(text_salary.get()) * (1 - (float(text_tax.get()) + float(text_insurance.get())) / 100)
            text_netsalary.config(state="normal")
            text_netsalary.delete(0, tk.END)
            if net_salary >= 0.01 * float(text_salary.get()):
                text_netsalary.insert(0,f"{int(net_salary):,}")  
            else:
                text_netsalary.insert(0,"")
            text_netsalary.config(state="disabled")
        except:
            text_netsalary.config(state="normal")
            text_netsalary.delete(0, tk.END)
            text_netsalary.config(state="disabled")
    else:
        save_button.config(state="disabled")
#Save button function
def save_form(event):
    #Checking accept button status
    if accept.get() == 1:
        errors = []
        #Checking ID number limitations
        if text_ID.get() == "":
            errors.append("- Please enter your ID number.")
            text_ID.config(background="#ffc0cb")
        elif text_ID.get().isnumeric() == False:
            errors.append("- ID number can only contain digits.")
            text_ID.config(background="#ffc0cb")
        elif len(text_ID.get()) != 10:
            errors.append("- ID number must contain 10 digits.")
            text_ID.config(background="#ffc0cb")
        else:
            text_ID.config(background="white")
        #Checking first name limitations
        if text_first.get() == "":
            errors.append("- Please enter your first name.")
            text_first.config(background="#ffc0cb")
        elif text_first.get().replace(" ", "").isalpha() == False:
            errors.append("- First name can only contain letters and spaces.")
            text_first.config(background="#ffc0cb")
        elif len(text_first.get().replace(" ", "")) < 3:
            errors.append("- First name can't have less than 3 letters.")
            text_first.config(background="#ffc0cb")
        elif len(text_first.get().replace(" ", "")) > 30:
            errors.append("- First name can't have more than 30 letters.")
            text_first.config(background="#ffc0cb")
        else:
            text_first.config(background="white")
        #Checking last name limitations
        if text_last.get() == "":
            errors.append("- Please enter your last name.")
            text_last.config(background="#ffc0cb")
        elif text_last.get().replace(" ", "").isalpha() == False:
            errors.append("- Last name can only contain letters and spaces.")
            text_last.config(background="#ffc0cb")
        elif len(text_last.get().replace(" ", "")) < 3:
            errors.append("- Last name can't have less than 3 letters.")
            text_last.config(background="#ffc0cb")
        elif len(text_last.get().replace(" ", "")) > 30:
            errors.append("- Last name can't have more than 30 letters.")
            text_last.config(background="#ffc0cb")
        else:
            text_last.config(background="white")
        #Checking age limitations
        if text_age.get() == "":
            errors.append("- Please enter your age.")
            text_age.config(background="#ffc0cb")
        elif text_age.get().replace("-", "", 1).isnumeric() == False:
            errors.append("- Age must be an integer.")
            text_age.config(background="#ffc0cb")
        elif text_age.get().startswith("-") == True:
            errors.append("- Age can't be a negative number.")
            text_age.config(background="#ffc0cb")
        elif text_age.get().count("-") == 1:
            errors.append("- Age must be an integer.")
            text_age.config(background="#ffc0cb")
        elif int(text_age.get()) < 1:
            errors.append("- Age can't be less than 1 year.")
            text_age.config(background="#ffc0cb")
        elif int(text_age.get()) > 120:
            errors.append("- Age can't be greater than 120 years.")
            text_age.config(background="#ffc0cb")
        else:
            text_age.config(background="white")
        #Checking height limitations
        if text_height.get() == "":
            errors.append("- Please enter your height.")
            text_height.config(background="#ffc0cb")
        elif text_height.get().replace("-", "", 1).replace(".", "", 1).isnumeric() == False:
            errors.append("- Height must be a float.")
            text_height.config(background="#ffc0cb")
        elif text_height.get().startswith("-") == True:
            errors.append("- Height can't be a negative number.")
            text_height.config(background="#ffc0cb")
        elif text_height.get().count("-") == 1:
            errors.append("- Height must be a float.")
            text_height.config(background="#ffc0cb")
        elif float(text_height.get()) < 0.4:
            errors.append("- Height can't be less than 40 cm.")
            text_height.config(background="#ffc0cb")
        elif float(text_height.get()) > 2.5:
            errors.append("- Height can't be greater than 2.5 m.")
            text_height.config(background="#ffc0cb")
        else:
            text_height.config(background="white")
        #Checking weight limitations
        if text_weight.get() == "":
            errors.append("- Please enter your weight.")
            text_weight.config(background="#ffc0cb")
        elif text_weight.get().replace("-", "", 1).replace(".", "", 1).isnumeric() == False:
            errors.append("- Weight must be a float.")
            text_weight.config(background="#ffc0cb")
        elif text_weight.get().startswith("-") == True:
            errors.append("- Weight can't be a negative number.")
            text_weight.config(background="#ffc0cb")
        elif text_weight.get().count("-") == 1:
            errors.append("- Weight must be a float.")
            text_weight.config(background="#ffc0cb")
        elif float(text_weight.get()) < 1:
            errors.append("- Weight can't be less than 1 Kg.")
            text_weight.config(background="#ffc0cb")
        else:
            text_weight.config(background="white")
        #Checking gender limitations
        if gender.get() == "Not defined":
            errors.append("- Please define your gender.")
            label_gender.config(background="#ffc0cb")
        else:
            label_gender.config(background="#ccc")
        #Checking phone number limitations
        if text_phone.get() == "":
            errors.append("- Please enter your phone number.")
            text_phone.config(background="#ffc0cb")
        elif text_phone.get().isnumeric() == False:
            errors.append("- Phone number can only contain digits.")
            text_phone.config(background="#ffc0cb")
        elif len(text_phone.get()) != 11:
            errors.append("- Phone number must contain 11 digits.")
            text_phone.config(background="#ffc0cb")
        elif text_phone.get().startswith("09") == False:
            errors.append("- Phone number must start with 09.")
            text_phone.config(background="#ffc0cb")
        else:
            text_phone.config(background="white")
        #Checking email limitations
        if text_Email.get() == "":
            errors.append("- Please enter your Email.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().replace(" ","") != text_Email.get():
            errors.append("- Email address can't contain spaces.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().count("@") == 0:
            errors.append("- Email address must contain @.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().count("@") != 1:
            errors.append("- Email address must contain just one @.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().startswith("@"):
            errors.append("- Email must have a username with at least one character.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().endswith("@"):
            errors.append("- Email must have a domain.")
            text_Email.config(background="#ffc0cb")
        elif text_Email.get().endswith(".com") == False:
            errors.append("- Email's domain must end with .com.")
            text_Email.config(background="#ffc0cb")
        elif len(text_Email.get()[text_Email.get().find("@")+1:]) < 5:
            errors.append("- Email's domain must contain at least one character before .com.")
            text_Email.config(background="#ffc0cb")
        else:
            text_Email.config(background="white")
        #Checking job limitations
        if dropdown_job.get() not in dropdown_job["values"]: #Can be done with cget
            errors.append("- Please select your job from the list.")
            style.configure("TCombobox", fieldbackground="#ffc0cb")
        else:
            style.configure("TCombobox", fieldbackground="white")
        #Checking salary limitations
        if dropdown_job.get() not in ["Student", "House wife"]:
            if text_salary.get() == "":
                errors.append("- Please enter your salary.")
                text_salary.config(background="#ffc0cb")
            elif text_salary.get().replace("-", "", 1).replace(".", "", 1).isnumeric() == False:
                errors.append("- Salary must be a float.")
                text_salary.config(background="#ffc0cb")
            elif text_salary.get().startswith("-") == True:
                errors.append("- Salary can't be a negative number.")
                text_salary.config(background="#ffc0cb")
            elif text_salary.get().count("-") == 1:
                errors.append("- Salary must be a float.")
                text_salary.config(background="#ffc0cb")
            else:
                text_salary.config(background="white")
            if text_tax.get() == "":
                errors.append("- Please enter your tax percentage.")
                text_tax.config(background="#ffc0cb")
            elif text_tax.get().replace("-", "", 1).replace(".", "", 1).isnumeric() == False:
                errors.append("- Tax percentage must be a float.")
                text_tax.config(background="#ffc0cb")
            elif text_tax.get().startswith("-") == True:
                errors.append("- Tax percentage can't be a negative number.")
                text_tax.config(background="#ffc0cb")
            elif text_tax.get().count("-") == 1:
                errors.append("- Tax percentage must be a float.")
                text_tax.config(background="#ffc0cb")
            elif float(text_tax.get()) > 99:
                errors.append("- Tax percentage must be between 0 and 99.")
                text_tax.config(background="#ffc0cb")
            else:
                text_tax.config(background="white")
            if text_insurance.get() == "":
                errors.append("- Please enter your insurance percentage.")
                text_insurance.config(background="#ffc0cb")
            elif text_insurance.get().replace("-", "", 1).replace(".", "", 1).isnumeric() == False:
                errors.append("- Insurance percentage must be a float.")
                text_insurance.config(background="#ffc0cb")
            elif text_insurance.get().startswith("-") == True:
                errors.append("- Insurance percentage can't be a negative number.")
                text_insurance.config(background="#ffc0cb")
            elif text_insurance.get().count("-") == 1:
                errors.append("- Insurance percentage must be a float.")
                text_insurance.config(background="#ffc0cb")
            elif float(text_insurance.get()) > 99:
                errors.append("- Insurance percentage must be between 0 and 99.")
                text_insurance.config(background="#ffc0cb")
            else:
                text_insurance.config(background="white")
            try:
                reduction_percentage = float(text_tax.get()) + float(text_insurance.get())
                if reduction_percentage > 99:
                    errors.append("- The sum of tax and insurace percentage can't be greater than 99.")
                    text_tax.config(background="#ffc0cb")
                    text_insurance.config(background="#ffc0cb")
            except:
                pass
        #Checking errors status and showing errors via message box
        if len(errors) != 0:
            errors.insert(0, "Please correct below items to proceed:\n")
            error_message = "\n".join(errors)
            messagebox.showerror("Error",error_message)
            accept.set(0)
            save_button.config(state="disabled")
        #Importing data into database and showing a success window via message box
        else:
            salary = text_salary.get()
            tax = text_tax.get()
            insurance = text_insurance.get()
            net_salary = text_netsalary.get().replace(",","")
            if salary == "":
                salary = 0
            if tax == "":
                tax = 0
            if insurance == "":
                insurance = 0
            if net_salary == "":
                net_salary = 0
            try:
                myCursor.execute("insert into identity values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(text_ID.get(),text_first.get(),text_last.get(),int(text_age.get()),float(text_height.get()),float(text_weight.get()),gender.get(),text_phone.get(),text_Email.get(),dropdown_job.get(),float(salary),float(tax),float(insurance),float(net_salary)))
                connector.commit()
                messagebox.showinfo("Success","Your data is successfully saved.")
                clear_form("event")
            #Showing an error via messagebox if ID number already exists
            except sqlite3.IntegrityError:
                 text_ID.config(background="#ffc0cb")
                 messagebox.showerror("Error","Please correct below items to proceed:\n\n- ID number already exists.")
#Clear button function
def clear_form(event):
    text_ID.delete(0,tk.END)
    text_ID.config(background="white")
    text_first.delete(0,tk.END)
    text_first.config(background="white")
    text_last.delete(0,tk.END)
    text_last.config(background="white")
    text_age.delete(0,tk.END)
    text_age.config(background="white")
    text_height.delete(0,tk.END)
    text_height.config(background="white")
    text_weight.delete(0,tk.END)
    text_weight.config(background="white")
    gender.set("Not defined")
    label_gender.config(background="#ccc")
    text_phone.delete(0,tk.END)
    text_phone.config(background="white")
    text_Email.delete(0,tk.END)
    text_Email.config(background="white")
    dropdown_job.set("")
    dropdown_job["values"] = ["Student", "Worker", "Employee", "Self employed", "House wife"]
    style.configure("TCombobox", fieldbackground="white")
    text_salary.config(state="normal")
    text_salary.delete(0,tk.END)
    text_salary.config(background="white")
    text_tax.config(state="normal")
    text_tax.delete(0,tk.END)
    text_tax.config(background="white")
    text_insurance.config(state="normal")
    text_insurance.delete(0,tk.END)
    text_insurance.config(background="white")
    text_netsalary.config(state="normal")
    text_netsalary.delete(0,tk.END)
    text_netsalary.config(state="disabled")
    accept.set(0)
    save_button.config(state="disabled")
    text_ID.focus()
#Quit button function
def quit_form(event):
    form.destroy()
#Connecting program to the database and creating the main table
connector = sqlite3.connect("identity_database.db")
myCursor = connector.cursor()
myCursor.execute("create table if not exists identity(id text primary key,first_name text,last_name text,age integer,height real,weight real,gender text,phone_number text,email text,job text,salary real,tax real,insurance real,net_salary real)")
connector.commit()
#Creating form window
form = tk.Tk()
screen_height = form.winfo_screenheight()
screen_width = form.winfo_screenwidth()
form.title("Identity Form")
#Defining taskbar icon
taskbar_icon = 'mycompany.myproduct.subproduct.version'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(taskbar_icon)
form.iconbitmap("identity.ico")
#Adjusting form window's appearance
form.config(background="#ccc")
form.attributes("-alpha","0.9")
form.geometry(f"685x405+{(screen_width - 685) // 2}+{(screen_height - 405) // 2}")
form.resizable(False, False)
#Defining shortcuts for form window
form.bind("<Control-s>",save_form)
form.bind("<Control-z>",clear_form)
form.bind("<Escape>",quit_form)
#Creating elements and assigning commands and shortcuts
label_ID = tk.Label(form, text="ID Number:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_ID = tk.Entry(form, width=10, font=("Arial",14))
text_ID.bind("<Return>",jump_to_next_entry)
text_ID.bind("<Shift-Return>",jump_to_previous_entry)
label_name = tk.Label(form, text="Full Name:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_first = tk.Entry(form, width=15, font=("Arial",14))
text_first.bind("<Return>",jump_to_next_entry)
text_first.bind("<Shift-Return>",jump_to_previous_entry)
text_last = tk.Entry(form, width=15, font=("Arial",14))
text_last.bind("<Return>",jump_to_next_entry)
text_last.bind("<Shift-Return>",jump_to_previous_entry)
label_age = tk.Label(form, text="Age:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_age = tk.Entry(form, width=5, font=("Arial",14))
text_age.bind("<Return>",jump_to_next_entry)
text_age.bind("<Shift-Return>",jump_to_previous_entry)
label_height = tk.Label(form, text="Height (m):",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_height = tk.Entry(form, width=5, font=("Arial",14))
text_height.bind("<Return>",jump_to_next_entry)
text_height.bind("<Shift-Return>",jump_to_previous_entry)
label_weight = tk.Label(form, text="Weight (Kg):",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_weight = tk.Entry(form, width=5, font=("Arial",14))
text_weight.bind("<Return>",jump_to_next_entry)
text_weight.bind("<Shift-Return>",jump_to_previous_entry)
label_gender = tk.Label(form, text="Gender:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
gender = tk.StringVar(value="Not defined")
gender1 = tk.Radiobutton(form, text="Male", background="#ccc", foreground="black", font=("Arial",14,"bold"), variable=gender, value="Male", command = define_jobs)
gender1.bind("<Return>",jump_to_next_entry)
gender1.bind("<Shift-Return>",jump_to_previous_entry)
gender2 = tk.Radiobutton(form, text="Female", background="#ccc", foreground="black", font=("Arial",14,"bold"), variable=gender, value="Female", command = define_jobs)
gender2.bind("<Return>",jump_to_next_entry)
gender2.bind("<Shift-Return>",jump_to_previous_entry)
label_phone = tk.Label(form, text="Phone Number:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_phone = tk.Entry(form, width=15, font=("Arial",14))
text_phone.bind("<Return>",jump_to_next_entry)
text_phone.bind("<Shift-Return>",jump_to_previous_entry)
label_Email = tk.Label(form, text="Email:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_Email = tk.Entry(form, width=20, font=("Arial",14))
text_Email.bind("<Return>",jump_to_next_entry)
text_Email.bind("<Shift-Return>",jump_to_previous_entry)
label_job = tk.Label(form, text="Job:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
dropdown_job = ttk.Combobox(width=14, values=["Student", "Worker", "Employee", "Self employed", "House wife"], font=("Arial",14))
dropdown_job.bind("<<ComboboxSelected>>", define_salary_status)
dropdown_job.bind("<Return>",jump_to_next_entry)
dropdown_job.bind("<Shift-Return>",jump_to_previous_entry)
#Assigning style in order to change dropdown's background color
style = ttk.Style()
style.theme_use("clam")
label_salary = tk.Label(form, text="Salary:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_salary = tk.Entry(form, width=10, font=("Arial",14))
text_salary.bind("<Return>",jump_to_next_entry)
text_salary.bind("<Shift-Return>",jump_to_previous_entry)
label_tax = tk.Label(form, text="Tax (%):",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_tax = tk.Entry(form, width=5, font=("Arial",14))
text_tax.bind("<Return>",jump_to_next_entry)
text_tax.bind("<Shift-Return>",jump_to_previous_entry)
label_insurance = tk.Label(form, text="Insurance (%):",background="#ccc",foreground="black",font=("Arial",14,"bold"), width=15)
text_insurance = tk.Entry(form, width=5, font=("Arial",14))
text_insurance.bind("<Return>",calculate_net_salary)
text_insurance.bind("<Shift-Return>",jump_to_previous_entry)
label_netsalary = tk.Label(form, text="Net Salary:",background="#ccc",foreground="black",font=("Arial",14,"bold"))
text_netsalary = tk.Entry(form, width=10, font=("Arial",14), state="disabled")
accept = tk.IntVar()
accept_button = tk.Checkbutton(form, text="I confirmed my information are true.", background="#ccc", foreground="black", font=("Arial",14), variable=accept, onvalue=1, offvalue=0, command=activate_save)
accept_button.bind("<Return>",jump_to_next_entry)
accept_button.bind("<Shift-Return>",jump_to_previous_entry)
#Creating buttons and assigning hover-over commands
save_button = tk.Button(form, text="Save", font=("Arial",14), padx=20,activebackground="green", activeforeground="white", command=lambda:save_form("event"), state="disabled")
save_button.bind("<Return>",jump_to_next_entry)
save_button.bind("<Shift-Return>",jump_to_previous_entry)
save_button.bind("<Enter>",lambda event: save_button.config(background="#00c04b", foreground="white"))
save_button.bind("<Leave>",lambda event: save_button.config(background="SystemButtonFace", foreground="black"))
clear_button = tk.Button(form, text="Clear", font=("Arial",14), padx=20,activebackground="blue", activeforeground="white", command=lambda:clear_form("event"))
clear_button.bind("<Return>",jump_to_next_entry)
clear_button.bind("<Shift-Return>",jump_to_previous_entry)
clear_button.bind("<Enter>",lambda event: clear_button.config(background="#33abf9", foreground="white"))
clear_button.bind("<Leave>",lambda event: clear_button.config(background="SystemButtonFace", foreground="black"))
quit_button = tk.Button(form, text="Quit", font=("Arial",14), padx=20,activebackground="red", activeforeground="white", command=lambda:quit_form("event"))
quit_button.bind("<Return>",jump_to_next_entry)
quit_button.bind("<Shift-Return>",jump_to_previous_entry)
quit_button.bind("<Enter>",lambda event: quit_button.config(background="#ff7f7f", foreground="white"))
quit_button.bind("<Leave>",lambda event: quit_button.config(background="SystemButtonFace", foreground="black"))
#Griding elements into form window
label_ID.grid(row=0, column=0, sticky="w")
text_ID.grid(row=0, column=1, sticky= "w")
label_name.grid(row=0, column=2, sticky= "e")
text_first.grid(row=0, column=3, columnspan=2, sticky="w")
text_last.grid(row=0, column=5, columnspan=2, sticky="w", padx=5)
label_age.grid(row=1, column=0, sticky="w", pady=15)
text_age.grid(row=1, column=1, sticky="w", pady=15)
label_height.grid(row=1, column=2, sticky="e", pady=15)
text_height.grid(row=1, column=3, sticky="w", pady=15)
label_weight.grid(row=1, column=4, columnspan=2, sticky="e", pady=15)
text_weight.grid(row=1, column=6, sticky="w", pady=15)
label_gender.grid(row=2, column=0, rowspan=2, sticky="w")
gender1.grid(row=2, column=1, sticky="w")
gender2.grid(row=3, column=1, sticky="w")
label_phone.grid(row=2, column=3, rowspan=2, columnspan=2, sticky="e")
text_phone.grid(row=2, column=5, rowspan=2, columnspan=2, sticky="w", padx=5)
label_Email.grid(row=4, column=0, sticky="w", pady=15)
text_Email.grid(row=4, column=1, columnspan=2, sticky="w", pady=15)
label_job.grid(row=4, column=3, columnspan=2, sticky="e", pady=15)
dropdown_job.grid(row=4, column=5, columnspan=2, sticky="w",padx=5)
label_salary.grid(row=5, column=0, sticky="w")
text_salary.grid(row=5, column=1, sticky="w")
label_tax.grid(row=5, column=2, sticky="e")
text_tax.grid(row=5, column=3, sticky="w")
label_insurance.grid(row=5, column=4, columnspan=2, sticky="e",padx=1)
text_insurance.grid(row=5, column=6, sticky="w")
label_netsalary.grid(row=6, column=0, sticky="w", pady=15)
text_netsalary.grid(row=6, column=1, sticky="w", pady=15)
accept_button.grid(row=7, column=0, columnspan=4,sticky="w")
save_button.grid(row=8, column=0, columnspan=2, pady=15)
clear_button.grid(row=8, column=2, columnspan=2, pady=15)
quit_button.grid(row=8, column=4, columnspan=3, pady=15, padx=30)
#Assigning focus to the first field
text_ID.focus()
form.mainloop()
# modules importing
import customtkinter
from tkinter import *
from tkinter.ttk import Label,Button
import os
from PIL import Image, ImageTk
from tkinter import filedialog
import sqlite3
import pandas as pd
import openpyxl
from worksheet_updates import updates

customtkinter.set_appearance_mode("system")
customtkinter.set_default_color_theme("dark-blue")


#class MyFrame(customtkinter.CTkFrame):
    #def __init__(self, master, **kwargs):
        #super().__init__(master, **kwargs)

        # add widgets onto the frame...
        #self.label = customtkinter.CTkLabel(self)
        #self.label.grid(row=0, column=1, padx=20)

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        window_width = 1350
        window_height = 900
        screen_width = self.winfo_screenwidth()
        screen_heigth = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_heigth/2 - window_height/2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.title("Work A Flow")
        self.configure(fg_color="black")

        def import_func(event=None):
            filename = filedialog.askopenfilename(initialdir="C:\\Users\\Desktop",
                                        title="Upload file...",
                                        filetypes=(("Microsoft Excel Document",".xlsx"), ("CSV Document","*.csv"), ("All Files","*.*")))
            #To create dataframe
            df = pd.read_excel(filename, header=3)
            df.drop(df.iloc[:, 9:41], axis=1, inplace=True)
            #To convert to csv
            df.to_csv ("attendance.csv", 
                        index = False,
                        header=False)
            #To establish connection
            connection = sqlite3.connect('CHRS.db')
            c=connection.cursor()
            #To create employee table 
            c.execute('''
            CREATE TABLE IF NOT EXISTS attendance
            (
                SNo REAL,Emp_Code VARCHAR,Name VARCHAR,DOJ VARCHAR,DOR VARCHAR,DOL VARCHAR,Designation VARCHAR,Department VARCHAR,Team VARCHAR,
                No_Days_Present REAL,EL REAL,Weeky_Off REAL,Holiday REAL,Comp_Off REAL,LOP REAL,LOPR REAL,Total_Days REAL,Days_Payable REAL,Total_OT_Hours REAL,
                NS_Amount REAL,Other_Pay REAL,Company_CTC REAL,Basic REAL,Special_Allowance REAL,CCA REAL,Remarks VARCHAR,Status VARCHAR
            )
            ''')
            connection.commit()
            
            #To create worksheet table
            c.execute('''
            CREATE TABLE IF NOT EXISTS worksheet
            ([SNo] INTEGER, [EmployeeCode] VARCHAR(50),[Name] VARCHAR(50),[UAN_NUMBER] VARCHAR(50),
                                                                [Department] VARCHAR(100),
                                                                [Designation] VARCHAR(50),
                                                                [DOJ] VARCHAR(15),
                                                                [daysinmonth] REAL,
                                                                [Total_Payable_Days] REAL,
                                                                [Bonus1] REAL,
                                                                [Others_Pay1] REAL,
                                                                [OT_Hrs] REAL,
                                                                [Basic1] REAL,
                                                                [HRA] REAL,
                                                                [Bonus2] REAL,
                                                                [Con] REAL,
                                                                [Special_Allowance1] REAL,
                                                                [CCA1] REAL,
                                                                [Total] REAL,
                                                                [emp_PF] REAL,
                                                                [emp_CTC] REAL,
                                                                [PF_admn_charges] REAL,
                                                                [emp_ESI] REAL,
                                                                [Company_CTC] REAL,
                                                                [Basic2] REAL,
                                                                [HRA2] REAL,
                                                                [Special_Allowance2] REAL,
                                                                [CCA2] REAL,
                                                                [Conv] REAL,
                                                                [Arrear] REAL,
                                                                [Total_Other_allowance] REAL,
                                                                [Others_pay2] REAL,
                                                                [N_S_Allowances] REAL,
                                                                [Bonus] REAL,                                                                 
                                                                [Employee_Gross] REAL,
                                                                [Notice_pay] REAL,
                                                                [PF] REAL,
                                                                [PF_Arrears] REAL,
                                                                [ESI] REAL,
                                                                [PT] REAL,
                                                                [Advance/deduction] REAL,
                                                                [Total_Deduction] REAL,
                                                                [Net_Salary] REAL,
                                                                [EMPLOYER_PF] REAL,
                                                                [LWF] REAL,
                                                                [EMPLOYER_ESI] REAL,
                                                                [CTC] REAL,
                                                                [In_amount] REAL,                                                                
                                                                [Management_Fee] REAL,
                                                                [Billing] REAL,
                                                                [status] VARCHAR,
                                                                [Remarks] VARCHAR,
                                                                [Signature] VARCHAR)
            ''')
            connection.commit()
            #To Create insert_trigger
            c.execute(""" CREATE TRIGGER insert_trigger AFTER INSERT ON attendance
                                BEGIN
                                     INSERT INTO worksheet (SNo,EmployeeCode,Name,Department,Designation,DOJ,daysinmonth,Total_Payable_Days,Others_Pay1,OT_Hrs,Basic1,Special_Allowance1,CCA1,Company_CTC,N_S_Allowances,Remarks)
                                     VALUES (NEW.SNo,NEW.Emp_Code,NEW.Name,NEW.Department,NEW.Designation,NEW.DOJ,NEW.Total_days,NEW.Days_payable,NEW.Other_Pay,NEW.Total_OT_Hours,NEW.Basic,NEW.Special_Allowance,NEW.CCA,NEW.Company_CTC,NEW.NS_Amount,NEW.Status);
                                END;""" )
            connection.commit()

            #To insert values into attendance
            with open("attendance.csv") as file:
                records = 0
                for row in file:
                    c.execute(
                    ''' 
                    INSERT INTO attendance VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''' , row.split(",") )
            connection.commit()
            records += 1   

            #To remove null value
            c.execute(
                ''' 
                DELETE FROM attendance WHERE Emp_Code = '';
                '''  ) 
            connection.commit()
            c.execute(
                ''' 
                DELETE FROM worksheet WHERE EmployeeCode = '';
                '''  ) 
            connection.commit()  
            #To update values in worksheet
            updates()

            connection.close()

        self.label = customtkinter.CTkLabel(master=self, text="Chethana \nHR \nSolutions", font=("Roboto", 50), text_color="#D1E8E2")
        self.label.grid(row=0, column=1)
        self.button = customtkinter.CTkButton(master=self, text="Import File", command=import_func,corner_radius=50, height=50, width=50, font=("Roboto", 30))
        self.button.grid(row=2, column=1, padx=(300,300), pady=(300,0), sticky="nsew")
        self.label2 = customtkinter.CTkLabel(master=self, text="Upload only .csv, .xlxs and relatable files only", font=("Roboto", 18))
        self.label2.grid(row=3, column=1, padx=(20, 10), pady=(10, 10), sticky="ew")

        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)

        self.sidebar_frame = customtkinter.CTkFrame(self, width=400, corner_radius=0, fg_color="#1F2833")
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Welcome to Admin \nDashboard", font=("Roboto", 30), text_color="#116466")
        self.logo_label.grid(row=0, column=0, padx=20, pady=40)

        #self.my_frame = MyFrame(master=self)
        #self.my_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")


app = App()
app.mainloop()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pymysql

class employee():
    def __init__(self,root):
        self.root = root
        self.root.title("Encrypt & Decrypt")

        self.width = self.root.winfo_screenwidth()
        self.height = self.root.winfo_screenheight()
        self.root.geometry(f"{self.width}x{self.height}+0+0")

        title = tk.Label(self.root,text="Password Encryption and Decryption", bd=4, relief="raised", bg="brown",fg="white", font=("Elephant",40,"italic"))
        title.pack(side="top", fill="x")

        # add frame 
        addFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(240,100,180))
        addFrame.place(width=self.width/3, height=self.height-180, x=70, y=100)

        supBtn = tk.Button(addFrame,command=self.supFrameFun, text="Sign_Up", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        supBtn.grid(row=0, column=0, padx=30, pady=60)

        sinBtn = tk.Button(addFrame,command=self.sinFrameFun, text="Sign_In", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        sinBtn.grid(row=1, column=0, padx=30, pady=60)

        closeBtn = tk.Button(addFrame, text="Close",command=self.desMain, width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        closeBtn.grid(row=2, column=0, padx=30, pady=60)

        # detail frame

        self.detFrame = tk.Frame(self.root, bd=5, relief="ridge", bg=self.clr(100,240,180))
        self.detFrame.place(width=self.width/2, height=self.height-180, x=self.width/3+140, y=100)

        title = tk.Label(self.detFrame, text="Person Details", bg=self.clr(100,240,180), font=("Elephant",30,"bold"))
        title.pack(side="top", fill="x")

        self.tabFun()

    def tabFun(self):
        tabFrame = tk.Frame(self.detFrame, bd=4, relief="sunken", bg="cyan")
        tabFrame.place(width=self.width/2-40, height=self.height-280, x=17, y=70)

        x_scrol = tk.Scrollbar(tabFrame, orient="horizontal")
        x_scrol.pack(side="bottom", fill="x")

        y_scrol = tk.Scrollbar(tabFrame, orient="vertical")
        y_scrol.pack(side="right", fill="y")

        self.table = ttk.Treeview(tabFrame, xscrollcommand=x_scrol.set, yscrollcommand=y_scrol.set,
                                  columns=("id","name","des","addr","pw"))
        
        x_scrol.config(command=self.table.xview)
        y_scrol.config(command=self.table.yview)
        
        self.table.heading("id",text="Employee_ID")
        self.table.heading("name",text="Employee_Name")
        self.table.heading("des",text="Designation")
        self.table.heading("addr",text="Employee_Addr")
        self.table.heading("pw",text="Passwords")
        self.table["show"] = "headings"
        
        self.table.pack(fill="both", expand=1)

    def supFrameFun(self):
        self.suFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(100,150,240))
        self.suFrame.place(width=self.width/3, height=self.height-200, x=self.width/3+140, y=120)

        idLbl = tk.Label(self.suFrame, text="User_ID: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        idLbl.grid(row=0, column=0, padx=20, pady=25)
        self.id = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.id.grid(row=0, column=1, padx=10, pady=25)

        nameLbl = tk.Label(self.suFrame, text="User_Name: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        nameLbl.grid(row=1, column=0, padx=20, pady=25)
        self.name = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.name.grid(row=1, column=1, padx=10, pady=25)

        desLbl = tk.Label(self.suFrame, text="Designation: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        desLbl.grid(row=2, column=0, padx=20, pady=25)
        self.des = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.des.grid(row=2, column=1, padx=10, pady=25)

        addrLbl = tk.Label(self.suFrame, text="Address: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        addrLbl.grid(row=3, column=0, padx=20, pady=25)
        self.addr = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.addr.grid(row=3, column=1, padx=10, pady=25)

        pwLbl = tk.Label(self.suFrame, text="Password: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        pwLbl.grid(row=4, column=0, padx=20, pady=25)
        self.pw = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.pw.grid(row=4, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.suFrame,command=self.signUpFun, text="SignUp", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=5, column=0, padx=30, pady=30, columnspan=2)

    def desFrame(self):
        self.suFrame.destroy()

    def signUpFun(self):
        id = self.id.get()
        name = self.name.get()
        des = self.des.get()
        addr = self.addr.get()
        pw = self.pw.get()

        if id and name and des and addr and pw:
            id_int = int(id)

            encrypted = ''.join(chr((ord(char)+3)%256)for char in pw)
            try:
                self.dbFun()
                self.cur.execute("insert into employee(emp_id,name,desig,addr,pw) values(%s,%s,%s,%s,%s)",(id_int,name,des,addr,encrypted))
                self.con.commit()
                tk.messagebox.showinfo("Success", f"Employee.{name} Registered Successfuly!")
                self.desFrame()

                self.table.delete(*self.table.get_children())
                self.cur.execute("select * from employee where emp_id=%s",id_int)
                row = self.cur.fetchone()
                self.table.insert('',tk.END,values=row)

                self.con.close()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Error: {e}")
                self.desFrame()
        else:
            tk.messagebox.showerror("Error", "Please Fill All Input Fields!")

    def sinFrameFun(self):
        self.suFrame = tk.Frame(self.root, bd=4, relief="ridge", bg=self.clr(100,150,240))
        self.suFrame.place(width=self.width/3, height=self.height-350, x=self.width/3+140, y=120)

        idLbl = tk.Label(self.suFrame, text="User_ID: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        idLbl.grid(row=0, column=0, padx=20, pady=25)
        self.idin = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.idin.grid(row=0, column=1, padx=10, pady=25)


        pwLbl = tk.Label(self.suFrame, text="Password: ", bg=self.clr(100,150,240), font=("Arial",15,"bold"))
        pwLbl.grid(row=1, column=0, padx=20, pady=25)
        self.pwin = tk.Entry(self.suFrame, width=18, bd=2, font=("Arial",15,"bold"))
        self.pwin.grid(row=1, column=1, padx=10, pady=25)

        okBtn = tk.Button(self.suFrame,command=self.sinFun, text="SignIn", width=20, bd=3, relief="raised", font=("Arial",20,"bold"))
        okBtn.grid(row=2, column=0, padx=30, pady=30, columnspan=2)

    def sinFun(self):
        id = int(self.idin.get())
        pw = self.pwin.get()

        try:
            self.dbFun()
            self.cur.execute("select pw,name from employee where emp_id=%s",id)
            row = self.cur.fetchone()
            if row:
                decrypted = ''.join(chr((ord(char)-3)%256)for char in row[0])
                if pw==decrypted:
                    tk.messagebox.showinfo("Success",f"Wellcome Mr/Mrs.{row[1]}")
                    self.desFrame()
                    self.table.delete(*self.table.get_children())
                    self.cur.execute("select * from employee where emp_id=%s",id)
                    data = self.cur.fetchone()
                    self.table.insert('',tk.END, values=data)

                    self.con.close()
                else:
                    tk.messagebox.showerror("Error","Please Enter A Valid Employee Password!")
            else:
                tk.messagebox.showerror("Error","Please Enter A Valid Employee ID!")

        except Exception as e:
            tk.messagebox.showerror("Error", f"Error: {e}")
            self.desFrame()

    def dbFun(self):
        self.con = pymysql.connect(host="localhost", user="root", passwd="admin", database="rec")
        self.cur = self.con.cursor()


    def clr(self,r,g,b):
        return f"#{r:02x}{g:02x}{b:02x}"

    def desMain(self):
        self.root.destroy()


root =  tk.Tk()
obj = employee(root)
root.mainloop()
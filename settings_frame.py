import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesno
import sqlManage

class body(tk.Toplevel):
    def __init__(self, master):
        self.width = 300
        self.height = 300

        super().__init__(master)
        self.master = master

        self.position()
        self.build()

    def change_var(self):
        # display an error message when seshes are even

        try:
            int(self.setProdTime.get())
            int(self.setBreakTime.get())
            int(self.setSeshes.get())
        except ValueError:
            self.error.config(text="Time and cycles should be numbers", fg="red", font=("Bodoni 72", 15))
            return


        if int(self.setProdTime.get()) < 1 or int(self.setBreakTime.get()) < 1 or int(self.setSeshes.get()) < 1:
            self.error.config(text="Time and cycles should be positive", fg="red", font=("Bodoni 72", 15))
            return
        else:
            self.error.config(text="")

        if int(self.setSeshes.get()) % 2 == 0:
            self.error.config(text="Number of cycles should be odd", fg="red", font=("Bodoni 72", 15))
            return
        else:
            self.error.config(text="")

        self.master.timeset_prod = int(self.setProdTime.get())
        self.master.timeset_break = int(self.setBreakTime.get())
        self.master.seshset = int(self.setSeshes.get())

        sqlManage.main_page(self.master.user).write_prefs(self.master.timeset_prod, self.master.timeset_break, self.master.seshset)
        
        # update the clock in the parent window
        self.master.times.set("{:02d}:{:02d}".format(self.master.timeset_prod // 60, self.master.timeset_prod % 60))
        self.master.sesh_indic.config(text=f"{self.master.sesh * '●' + (self.master.seshset - self.master.sesh) * '○'}")
        self.master.time = -2
        self.master.reset()
        self.destroy()


    def position(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))


    def build(self):
        style = ttk.Style()
        style.configure('W.TButton', font =
               ('Bodoni 72', 30, 'bold', 'underline'), background="#002B4D")


        self.resizable(False, False)
        self.title("Pomodoro Settings")
        self.mainframe = tk.Frame(self, width=300, height=300, bg="#002B4D")
        self.mainframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        self.button = tk.Button(self.mainframe, text="SAVE", command=self.change_var,height=1, width=3, highlightbackground="#002B4D", fg="#002B4D", font=("Bodoni 72", 25), bd=0, highlightthickness=1, activebackground="#F7F7F7", activeforeground="#002B4D")
        self.button.place(relx=0.5, y=205, anchor=tk.CENTER)

        self.error = tk.Label(self.mainframe, text="", font=("Bodoni 72", 1), bg="#002B4D", fg="#F7F7F7")
        self.error.place(x=150, y=235, anchor=tk.CENTER)

        # add delete user button
        self.delete = tk.Button(self.mainframe, text="DELETE USER", height=1, width=10,  fg="red", font=("Bodoni 72", 25), bd=0,  activebackground="#F7F7F7", activeforeground="#002B4D", # add red border 
        highlightcolor="red", highlightbackground="red", highlightthickness=1)
        self.delete.place(relx=0.5, y=270, anchor=tk.CENTER)

        # bind the delete button to a function sqlManage.delete_user(self.master.user)
        self.delete.bind("<Button-1>", self.deleteLogOut)


        self.prodTime = tk.StringVar()
        self.breakTime = tk.StringVar()
        self.seshes = tk.StringVar()

        self.prodTime.set(self.master.timeset_prod)
        self.breakTime.set(self.master.timeset_break)
        self.seshes.set(self.master.seshset)

        self.setProdTime = tk.Entry(self.mainframe, width=5, textvariable=self.prodTime, font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7", justify="center", bd=0, highlightthickness=1, selectbackground="#F7F7F7", selectforeground="#002B4D", highlightbackground="#F7F7F7")
        self.setProdTime.place(x=220, y=30, anchor=tk.CENTER)

        self.setBreakTime = tk.Entry(self.mainframe,textvariable=self.breakTime, width=5, font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7", justify="center", bd=0, highlightthickness=1, selectbackground="#F7F7F7", selectforeground="#002B4D", highlightbackground="#F7F7F7")
        self.setBreakTime.place(x=220, y=90, anchor=tk.CENTER)

        self.setSeshes = tk.Entry(self.mainframe,textvariable=self.seshes, width=5, font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7", justify="center", bd=0, highlightthickness=1, selectbackground="#F7F7F7", selectforeground="#002B4D", highlightbackground="#F7F7F7")
        self.setSeshes.place(x=220, y=150, anchor=tk.CENTER)

        self.prodTimeLabel = tk.Label(self.mainframe, text="Work time, s: ", font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7")
        self.prodTimeLabel.place(x=10, y=27, anchor=tk.W) 

        self.breakTimeLabel = tk.Label(self.mainframe, text="Break time, s: ", font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7")
        self.breakTimeLabel.place(x=10, y=87, anchor=tk.W)

        self.seshesLabel = tk.Label(self.mainframe, text="Cycles:", font=("Bodoni 72", 30), bg="#002B4D", fg="#F7F7F7")
        self.seshesLabel.place(x=10, y=147, anchor=tk.W)

    def deleteLogOut(self, event):
            answer = askyesno(title='Confirmation',
                          message='Are you sure that you want to delete an account?')
            if answer:
                self.destroy()

                sqlManage.delete_user([self.master.user])
                self.master.logOut()

# otworz nowe okno, na dole przycsisk save [DONE]
# change time for break [DONE]
# change time for work [DONE]
# change number of seshes [DONE]
# log out user
# delete user

import tkinter as tk
from functools import partial
import main_frame
import sqlManage

# region
# class button(tk.Canvas):
#     def __init__(self, master, command, width=200, height=50, bg="white", fg="black"):
#         super().__init__(master, width=width, height=height, bg=bg, highlightthickness=0)
#         self.button = self.round_rectangle(50, 50, 150, 100, radius=20, fill="blue")
#         self.command = command
#         self.bind("<Button-1>", self.command)
# endregion

class RoundedButton(tk.Button):
    def __init__(self, parent, text, command, bg, size, type, width=None, height=None, ):
        tk.Button.__init__(self, parent, text=text, command=command,
                           bg=bg, width=width, height=height, relief=tk.FLAT, bd=0)
        self.config(font=(type, size))
        self.config(highlightbackground=bg)

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, event):
        self.config(bg="light grey")

    def _on_leave(self, event):
        self.config(bg=self["bg"])

    def _on_press(self, event):
        pass

    def _on_release(self, event):
        if self.command is not None:
            self.command()


class login(tk.Frame):
    def __init__(self, master):

        self.width = 700
        self.height = 500
        self.master = master
        super().__init__(master, width=self.width, height=self.height, bg="#F7F7FF")

        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        master.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.layout()
        self.actionWidgets()
        

    def layout(self):
        self.greet = tk.Frame(self, width=400, height=100, bg="#F7F7FF")
        self.action = tk.Frame(self, width=300, height=450, bg="#3F826D")


        self.greet.place(x=self.width/2, y=70, anchor=tk.CENTER)
        self.action.place(x=self.width/2, y=400, anchor=tk.CENTER)


        self.welcome_big = tk.Label(self.greet, text="TOMATO TIME", font=(
            "Bodoni 72", 40), bg="#F7F7FF", fg="black")
        self.welcome_small = tk.Label(self.greet, text="The ultimate Pomodoro Timer", font=(
            "Bodoni 72", 21, "italic"), bg="#F7F7FF", fg="black")


        self.welcome_big.place(relx=0.5, rely=0.5, anchor='center')
        self.welcome_small.place(relx=0.5, rely=0.8, anchor='center')

        self.config(background="#002B4D")
        self.greet.config(bg="#002B4D")
        self.welcome_big.config(bg="#002B4D", fg="#F7F7FF")
        self.welcome_small.config(bg="#002B4D", fg="#F7F7FF")


    def actionWidgets(self):
        # self.username = tk.Label(self.action, text="Username", font=("Arial", 20), bg="green", fg="white")
        def validateLogin(username, password):
            usr = username.get()
            pswd = password.get()
            check = sqlManage.login_page(usr, pswd)
            correct = check.validate_login_sql()
            if correct:

                self.login_error.set("LOGIN SUCCESS")
                self.status_label.config(text=self.login_error.get(), fg="black")
                self.small_status_label.config(text="")

                self.loginSuccess(user=usr)
                return
            else:
                self.login_error.set("INCORRET LOGIN INFORMATION")
                self.status_label.config(text=self.login_error.get(), fg="orange")
                self.small_status_label.config(text="")
            return
            
        def createUser(username, password):
            if username.get() == "" or password.get() == "":
                self.small_status_label.config(text="EMPTY FIELDS", fg="orange")
                self.login_error.set("")
                self.status_label.config(text=self.login_error.get())
                return
            # check if the record doesnt already exist



            huh = sqlManage.login_page(username.get(), password.get())
            correct = huh.user_exists()
            if correct:
                self.small_status_label.config(text="USER ALREADY EXISTS", fg="orange")
                self.login_error.set("")
                self.status_label.config(text=self.login_error.get())
                return

            make = sqlManage.login_page(username.get(), password.get())
            make.create_user()
            self.small_status_label.config(text="USER ADDED", fg="white")
            self.login_error.set("")
            self.status_label.config(text=self.login_error.get())

            return


        self.username = tk.StringVar(self, "Username")
        self.name_entry = tk.Entry(self.action, textvariable=self.username, foreground="#545E75", font=(
            "Bodoni 72", 25), width=15, bd=0, bg="white", highlightthickness=0.5)
        self.name_entry.place(relx=0.5, rely=0.1, anchor=tk.CENTER)


        self.password = tk.StringVar(self, "TEST")
        self.password_entry = tk.Entry(self.action, textvariable=self.password, show='*', foreground="black",
                                  font=("Bodoni 72", 25), width=15, bd=0, bg="white", highlightthickness=0.5)
        self.password_entry.place(relx=0.5, rely=0.20, anchor=tk.CENTER)


        self.login_button = tk.Button(self.action, text="LOG IN", command=partial(validateLogin, self.username, self.password), bg="light blue", width=15, height=1, font=("Bodoni 72", 20), bd=0, highlightthickness=0)
        self.login_button.place(relx=0.5, rely=0.32, anchor=tk.CENTER)

        self.login_error = tk.StringVar(self, "")
        self.status_label = tk.Label(self.action, text=self.login_error.get(), font=("Bodoni 72", 12), bg="#3F826D", fg="orange")
        self.status_label.place(relx=0.5, rely=0.4, anchor="center")


        self.first_time = tk.Label(self.action, text="First time using the app?", font=(
            "Bodoni 72", 21), bg="#3F826D", fg="black")
        self.first_time.place(relx=0.5, rely=0.5, anchor='center')


        self.sign_in = RoundedButton(self.action, "SIGN UP", command=partial(createUser, self.username, self.password), bg="gray", size=18, type="Bodoni 72")
        self.sign_in.place(relx=0.5, rely=0.57, anchor=tk.CENTER)

        
        self.small_status_label = tk.Label(self.action, text="", font=("Bodoni 72", 12), bg="#3F826D", fg="white")
        self.small_status_label.place(relx=0.5, rely=0.63, anchor="center")


        def clrNameEntry(event):
            self.name_entry.delete(0, "end")
            return None

        def clrPasswdEntry(event):
            self.password_entry.delete(0, "end")
            return None

        self.name_entry.bind("<Button-1>", clrNameEntry)
        self.password_entry.bind("<Button-1>", clrPasswdEntry)


    def loginSuccess(self, user):
        # TO-DO: create new frame with timer
        self.newr = tk.Toplevel()
        self.newr.title('Pomodoro Timer')
        self.newr.resizable(False, False)
        app = main_frame.body(self.newr, user=user)
        app.pack()
        #self.master.destroy()
        self.status_label.config(text="")

        self.newr.mainloop()
        # threading.Thread(target=app.start_timer).start()    
        return
    
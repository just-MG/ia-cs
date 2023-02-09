from functools import partial
import tkinter as tk
from tkinter import Canvas, ttk
import sql_manage
# import time
# import datetime
# import os
# import sys # to exit the application
import mysql.connector

# class button(tk.Canvas):
#     def __init__(self, master, command, width=200, height=50, bg="white", fg="black"):
#         super().__init__(master, width=width, height=height, bg=bg, highlightthickness=0)
#         self.button = self.round_rectangle(50, 50, 150, 100, radius=20, fill="blue")
#         self.command = command
#         self.bind("<Button-1>", self.command)

class RoundedButton(tk.Button):
    def __init__(self, parent, text, command, bg, size, type, width=None, height=None, ):
        tk.Button.__init__(self, parent, text=text, command=command, bg=bg, width=width, height=height, relief=tk.FLAT, bd=0)
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
        super().__init__(master, width=self.width, height=self.height, bg="#F7F7FF")

        #self.name_var = tk.StringVar()

        self.layout()
        self.action_widgets()
        self.new_user_widget()
        

    def layout(self):
        self.greet = tk.Frame(self, width=400, height=100, bg="#F7F7FF")
        self.action = tk.Frame(self, width=300, height=250, bg="#3F826D")
        self.new_user = tk.Frame(self, width=300, height=80, bg="#F7F7FF")

        self.greet.place(x=self.width/2, y=70, anchor=tk.CENTER)
        self.action.place(x=self.width/2, y=275, anchor=tk.CENTER)
        self.new_user.place(x=self.width/2, y=450, anchor=tk.CENTER)
        

        self.welcome_big = tk.Label(self.greet, text="TOMATO TIME", font=("Bodoni 72", 40), bg="#F7F7FF", fg="black")
        self.welcome_small = tk.Label(self.greet, text="The ultimate Pomodoro Timer", font=("Bodoni 72", 21, "italic"), bg="#F7F7FF", fg="black")

        self.welcome_big.place(relx=0.5, rely=0.5, anchor='center')
        self.welcome_small.place(relx=0.5, rely=0.8, anchor='center')


    def action_widgets(self):
        #self.username = tk.Label(self.action, text="Username", font=("Arial", 20), bg="green", fg="white")
        def validateLogin(username, password):
            check = sql_manage.user_check(username.get(), password.get())
            correct = check.validate_login_sql()

            if correct:
                name_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                self.login_succes()
            else:
                print("Login failed")


            return

        canvas = tk.Canvas(self.action, bg="#545E75", height=50, width=270, bd=0, highlightthickness=0)
        #canvas.place(relx=0.5, rely=0.15, anchor=tk.CENTER)

        username = tk.StringVar(self, "Username")

        name_entry = tk.Entry(self.action, textvariable=username, foreground="#545E75", font=("Futura", 25), width=15, bd=0, bg="white", highlightthickness=0.5)
        # format entry box
        name_entry.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

        password = tk.StringVar(self)
        password_entry = tk.Entry(self.action, textvariable=password, show='*', foreground="black", font=("Futura", 25), width=15, bd=0, bg="white", highlightthickness=0.5)
        password_entry.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        fuckit = tk.Button(self.action, text="☞ LOGIN", command=partial(validateLogin, username, password), bg="light blue", width=15, height=1, font=("Futura", 20), bd=0, highlightthickness=0)
        # fuckit = RoundedButton(self.action, "☞ LOG IN", command=, bg="light blue", size=20, type="Futura")

        fuckit.place(relx=0.5, rely=0.8, anchor=tk.CENTER)

    
    

        # self.cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (self.name_var, self.password_var))
        # self.results = self.cursor.fetchall()
        # if self.results:
        #    print("Login successful")
        # else:
        #    print("Login failed")
        

    def new_user_widget(self):
        # inherit name entry from the method action_widgets()
        
        
        def validateLogin(username, password):
            check = sql_manage.user_check(username.get(), password.get())
            correct = check.validate_login_sql()
            
            if correct:
                name_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
                self.login_succes()
            else:
                print("Login failed")


            return

        self.first_time = tk.Label(self.new_user, text="First time using the app?", font=("Futura", 21), bg="#F7F7FF",fg="black")
        self.first_time.place(relx=0.5, rely=0.3, anchor='center')

        sign_in = RoundedButton(self.new_user, "SIGN UP", command=lambda: print("hello world"), bg="gray", size=15, type="Futura")
        sign_in.place(relx=0.5, rely=0.7, anchor=tk.CENTER)

    def login_succes(self):
        print("Login successful")

# class main_frame(tk.Frame):
#     def __init__(self, master):
#         super().__init__(master, width=700, height=500, bg="#F7F7FF")
#         self.layout()
#         self.action_widgets()
#         self.new_user_widget()
    

def main():
    root = tk.Tk()
    root.title('login Timer')
    root.resizable(False, False)
    app = login(root)
    app.pack()
    root.mainloop()

main()


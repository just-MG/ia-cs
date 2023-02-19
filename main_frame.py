import tkinter as tk
from tkinter import simpledialog
import datetime
import time
from tkinter.messagebox import askyesno
import sqlManage, settings_frame, stats


class body(tk.Frame):
    def __init__(self, master, user):
        self.width = 700
        self.height = 500
        self.master = master
        
        self.user = user
        super().__init__(master, width=self.width, height=self.height, bg="#F7F7FF")
        screen_width = master.winfo_screenwidth()
        screen_height = master.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        master.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.setVars()
        self.build()
        self.timer()
        self.colors(True)

    def setVars(self):
        get = sqlManage.main_page(self.user)
        results = get.obtain_prefs()

        self.timeset_prod = results[0]
        self.timeset_break = results[1]
        self.seshset = results[2]

        self.time = -2
        self.start = 0
        self.end = 0
        self.pauses = 0
        self.sesh = 1
        self.complete = False
        self.running = False
        self.should_pause = True
        self.taskName = tk.StringVar()
        self.taskName.set("Productivity")
        self.timeleft = self.timeset_prod

    def build(self):
        self.namesL = tk.Frame(self, width=70, height=500)
        self.namesR = tk.Frame(self, width=70, height=500)
        self.greet = tk.Frame(self, width=400, height=160, bg="#F7F7FF")
        self.timer_body = tk.Frame(self, width=400, height=250, bg="#002B4D")
        self.actions = tk.Frame(self, width=400, height=80, bg="#002B4D", highlightbackground="black", highlightthickness=1, bd=1, relief=tk.FLAT)
        self.stats = tk.Frame(self, width=150, height=80, bg="#002B4D", highlightbackground="black", highlightthickness=1, bd=1, relief=tk.FLAT)

        self.namesL.place(x=35, y=250, anchor=tk.CENTER) 
        self.namesR.place(x=600, y=250, anchor=tk.CENTER)
        self.greet.place(x=self.width/2, y=40, anchor=tk.CENTER)
        self.timer_body.place(x=self.width/2, y=260, anchor=tk.CENTER)
        self.actions.place(x=self.width/2, y=450, anchor=tk.CENTER)

        self.welcome_big = tk.Label(self.greet, text="TOMATO TIME", font=(
            "Bodoni 72", 40), bg="#F7F7FF", fg="black")
        self.welcome_small = tk.Label(self.greet, text="The ultimate Pomodoro Timer", font=(
            "Bodoni 72", 21, "italic"), bg="#F7F7FF", fg="black")
        self.welcome_user = tk.Label(self.greet, text=f"Welcome back, {self.user}.", font=(
            "Bodoni 72", 21), bg="#F7F7FF", fg="black")

        self.welcome_big.place(relx=0.5, rely=0.4, anchor='center')
        self.welcome_small.place(relx=0.5, rely=0.6, anchor='center')
        self.welcome_user.place(relx=0.5, rely=0.93, anchor='center')

        self.canvas = tk.Canvas(self.namesL, width=200, height=700, background="#3F826D", bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack()
        self.canvas2 = tk.Canvas(self.namesR, width=200, height=700, background="#3F826D", bd=0, highlightthickness=0, relief='ridge')
        self.canvas2.pack()

        self.text = self.canvas.create_text(110, 350, text=self.taskName.get(), font=("Bodoni 72", 50), angle=90)
        self.text2 = self.canvas2.create_text(155, 350, text=self.taskName.get(), font=("Bodoni 72", 50), angle=270)

        self.canvas.bind("<Button-1>", self.getName)
        self.canvas2.bind("<Button-1>", self.getName)

        self.base_stat = tk.Button(self.actions, text="Overview", font=("Bodoni 72", 20), bg="#002B4D", fg="black", command=self.baseStat, width=7, height=1, bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="black", activeforeground="black", relief="flat")
        self.full_stat = tk.Button(self.actions, text="History", font=("Bodoni 72", 20), bg="#002B4D", fg="black", command=self.advancedStat, width=7, height=1, bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="black", activeforeground="black", relief="flat")

        self.config(background="#3F826D")
        self.greet.config(bg="#3F826D")
        self.welcome_big.config(bg="#3F826D", fg="#F7F7FF")
        self.welcome_small.config(bg="#3F826D", fg="#F7F7FF")
        self.welcome_user.config(bg="#3F826D", fg="#F7F7FF")

    def baseStat(self):
        child_window = stats.base(self)

    def advancedStat(self):
        child_window = stats.full(self)
        
    def getName(self, event):
        user_input = simpledialog.askstring("Pomodoro Name", "Your task name:")
        if user_input is not None:
            self.taskName.set(user_input)
            self.canvas.itemconfig(self.text, text=user_input)
            self.canvas2.itemconfig(self.text2, text=user_input)
            return user_input

    def timer(self):
        self.seshdots = tk.StringVar()
        self.seshdots.set(self.sesh * "●" + (self.seshset - self.sesh) * "○")
        self.sesh_indic = tk.Label(self.timer_body, text=self.seshdots.get(), font=("Bodoni 72", 20), bg="#3F826D", fg="black")
        self.sesh_indic.place(relx=0.5, rely=0.1, anchor='center')

        self.motivate = tk.Label(self.timer_body, text="Work!", font=("Bodoni 72", 20), bg="#3F826D", fg="black")
        self.motivate.place(relx=0.5, rely=0.2, anchor='center')

        self.times = tk.StringVar()
        self.times.set("{:02d}:{:02d}".format(self.timeset_prod // 60, self.timeset_prod % 60))

        self.clock = tk.Entry(self.timer_body, textvariable=self.times, bg='#3F826D', bd=0, width = 10, font = ('Bodoni 72', 130), fg="black", justify='center', highlightthickness=0, highlightcolor="black", highlightbackground="black", disabledbackground="#3F826D", disabledforeground="black", state='disabled')
        self.clock.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        
        self.start_button = tk.Button(self.actions, text="⏵", command=self.timerOptimal, bg="#3F826D", font=("Bodoni 72", 30), width=1, height=1, bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="#3F826D", activeforeground="black", fg="black", relief="flat")

        self.reset_button = tk.Button(self.actions, text="↻", command=self.reset, bg="#3F826D", width=1, height=1, font=("Bodoni 72", 30), bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="#3F826D", activeforeground="black", fg="black", relief="flat")

        self.setttings_button = tk.Button(self.actions, text="⚙", command=self.settings, bg="#3F826D", width=1, height=1, font=("Bodoni 72", 30), bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="#3F826D", activeforeground="black", fg="black", relief="flat")

        self.logout_button = tk.Button(self.actions, text="Log out", command=self.logOut, bg="#3F826D", width=7, height=1, font=("Bodoni 72", 20), bd=0, highlightthickness=0, highlightcolor="black", highlightbackground="black", activebackground="#3F826D", activeforeground="black", fg="black", relief="flat")

        self.start_button.grid(row=0, column=0, padx=0, pady=5)
        self.reset_button.grid(row=0, column=1, padx=0, pady=5)
        self.setttings_button.grid(row=0, column=2, padx=10, pady=5)
        self.logout_button.grid(row=1, column=2, padx=10, pady=5)
        self.base_stat.grid(row=1, column=0, padx=10, pady=10)
        self.full_stat.grid(row=1, column=1, padx=10, pady=10)
        
    def colors(self, prod):
        if prod:
            self.motivate.config(text="Work!", fg="#F7F7FF")
            self.timer_body.config(bg="#002B4D")
            self.sesh_indic.config(bg="#002B4D", fg="#F7F7FF")
            self.clock.config(bg="#002B4D", disabledbackground="#002B4D", fg="#F7F7FF", disabledforeground="#F7F7FF")
            self.motivate.config(bg="#002B4D", fg="#F7F7FF")
        else:
            self.motivate.config(text="Rest!", fg="#002B4D")
            self.timer_body.config(bg="#F7F7FF")
            self.sesh_indic.config(bg="#F7F7FF", fg="#002B4D")
            self.clock.config(bg="#F7F7FF", disabledbackground="#F7F7FF", fg="#002B4D", disabledforeground="#002B4D")
            self.motivate.config(bg="#F7F7FF", fg="#002B4D")
        
    def timerOptimal(self):
        self.prod = True if self.sesh % 2 == 1 else False
        self.determineTime()
        self.running = not self.running
        self.should_pause = not self.should_pause

        if not self.should_pause:
            if self.prod:
                self.colors(True)
            else:
                self.colors(False)
        
            if self.running:
                if self.start == 0:
                    self.start = time.time()

                self.start_button.config(text="⏸")

                while self.running and self.time >= 0:
                    self.minutes = self.time // 60
                    self.seconds = self.time % 60
                    self.time -= 1
                    self.times.set("{:02d}:{:02d}".format(self.minutes, self.seconds))
                    self.update()
                    time.sleep(1)
                if not self.should_pause and self.time == -1:
                    self.should_pause = not self.should_pause
                    self.sesh += 1
                    if self.sesh == self.seshset+1:
                        self.motivate.config(text="00:00", fg="#F7F7FF")
                        self.times.set("DONE")
                        self.start_button.config(text="⏹", command=self.reset)
                        self.clock.config(textvariable=self.times)
                        self.complete = True
                        self.stop()
                    else:
                        self.seshdots.set(self.sesh * '●' + (self.seshset - self.sesh) * '○')
                        self.sesh_indic.config(text=self.seshdots.get())
                        self.running = False
                        self.time = 0
                        self.timerOptimal()
        else: 
            self.running = False
            self.start_button.config(text="⏵")
            self.pauses += 1
            return

    def determineTime(self):
        if self.time == -2 or self.time == 0:
            if self.sesh % 2 == 1:
                self.time = self.timeset_prod
            else:
                self.time = self.timeset_break
        else:
            self.time = self.time

    def stop(self):
        self.running = True
        self.reportRec()

    def reportRec(self):
        self.end = time.time()
        if self.time == -2: return
        self.sesh = self.sesh - 1 if self.sesh > 1 else 1

        self.total_prod = self.sesh // 2 * self.timeset_prod
        if self.sesh % 2 == 1:
            self.total_prod += self.timeset_prod - self.time - 1 if self.time != self.timeset_prod else self.timeset_prod
        elif self.complete:
            self.total_prod += self.timeset_prod

        self.total_break = (self.sesh - 1) // 2 * self.timeset_break
        if self.sesh % 2 == 0:
            self.total_break += self.timeset_break - self.time - 1 if self.time != self.timeset_break else self.timeset_break


        self.write = sqlManage.main_page(self.user)
        self.write.insert_record(pomodoroName=self.taskName.get(), beginTime=datetime.datetime.fromtimestamp(self.start).strftime('%Y-%m-%d %H:%M:%S'), endTime=datetime.datetime.fromtimestamp(self.end).strftime('%Y-%m-%d %H:%M:%S'), duration=round(self.end - self.start,2), seshes=self.sesh, status=self.complete, timesStopped=self.pauses, total_prod=self.total_prod, total_break=self.total_break)

        self.time = -2
        self.start = 0
        self.end = 0
        self.total_prod = 0
        self.total_break = 0
        self.pauses = 0
        self.sesh = 1
        self.complete = False

    def settings(self):
        answer = askyesno(title='Confirmation',
                          message='This will terminate your current session. Proceed?')
        if answer:
                self.openSet()
    
    def openSet(self):
        self.reportRec()
        child_window = settings_frame.body(self)
        
        
    def reset(self):
        self.sesh += 1
        self.reportRec()

        self.sesh = 1
        self.seshdots.set(self.sesh * '●' + (self.seshset - self.sesh) * '○')
        self.sesh_indic.config(text=self.seshdots.get())
        self.times.set("{:02d}:{:02d}".format(self.timeset_prod // 60, self.timeset_prod % 60))
        self.clock.config(textvariable=self.times)
        self.motivate.config(text="Work!", fg="#F7F7FF")
        self.running = False
        self.should_pause = False
        self.start_button.config(text="⏵", command=self.timerOptimal)
        self.colors(True)
    
    def logOut(self):
        self.reportRec()
        self.master.destroy()
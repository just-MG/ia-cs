import tkinter as tk
import sqlManage

class base(tk.Toplevel):
    def __init__(self, master):
        self.width = 350
        self.height = 500

        super().__init__(master)
        self.master = master
        self.user = master.user

        self.get = sqlManage.main_page(self.user)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.resizable(False, False)
        self.title("Pomodoro Statistics")
        self.mainframe = tk.Frame(self, width=self.width, height=self.height, bg="#002B4D")
        self.mainframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.initVals()
        self.obtainVals()
        self.text = tk.Text(self.mainframe, width=25, height=12, bg="#013259", fg="white", font=("Bodoni 72", 23), borderwidth=0, highlightthickness=0, spacing1=10, wrap=tk.WORD)

        self.buildText()

    def buildText(self):
        self.text.insert(tk.INSERT, "Overview", "there")
        self.text.insert(tk.INSERT, "\nTotal pomodoros done: ")
        self.text.insert(tk.INSERT, f"{self.total}", "here")
        self.text.insert(tk.INSERT, "\nTotal pomodoros completed: ")
        self.text.insert(tk.INSERT, f"{self.completed}", "here")
        self.text.insert(tk.INSERT, "\nSession completion rate: ")
        self.text.insert(tk.INSERT, f"{self.completeion_rate}%", "here")
        self.text.insert(tk.INSERT, "\nAverage session length: ")
        self.text.insert(tk.INSERT, f"{self.avg_session} s", "here")
        self.text.insert(tk.INSERT, "\nTotal productivity time: ")
        self.text.insert(tk.INSERT, f"{self.total_productivity} s", "here")
        self.text.insert(tk.INSERT, "\nTotal break time: ")
        self.text.insert(tk.INSERT, f"{self.total_break} s", "here")
        self.text.insert(tk.INSERT, "\nProductivity rate: ")
        self.text.insert(tk.INSERT, f"{self.productivity_rate}%", "here")
        self.text.insert(tk.INSERT, "\nTotal sessions done: ")
        self.text.insert(tk.INSERT, f"{self.sessions}", "here")
        self.text.insert(tk.INSERT, "\nLongest session: ")
        self.text.insert(tk.INSERT, f"{self.longest_session[0][8]} s", "here")
        self.text.insert(tk.INSERT, "\nMost common name: ")
        self.text.insert(tk.INSERT, f"{self.most_common}", "here")

        self.text.tag_configure("here", background="#3F826D", foreground="#F7F7F7", spacing1=10)
        self.text.tag_configure("there", foreground="#F7F7F7", justify=tk.CENTER, font=("Bodoni 72", 30, "bold"))


        # self.text.tag_config("start", background="black", foreground="green")
        self.text.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.text.config(state=tk.DISABLED)

    def initVals(self):
        self.total = 0
        self.completed = 0
        self.completeion_rate = 0
        self.total = 0
        self.avg_session = 0
        self.total_productivity = 0
        self.total_break = 0
        self.productivity_rate = 0
        self.sessions = 0
        self.longest_session = [[0]*9]
        self.most_common = None
        self.results = None

    def obtainVals(self):
        self.total = self.get.total_pomodoro()
        if self.total == 0:
            return
        self.completed = self.get.complted_pomodoro()
        self.completeion_rate = round(round(self.completed / self.total, 3)*100 if self.total != 0 else 0, 3)
        self.avg_session = self.get.average_duration()
        self.total_productivity = self.get.obtain_total_prod()
        self.total_break = self.get.obtain_total_break()
        self.productivity_rate = round(self.total_productivity / (self.total_productivity + self.total_break), 2)*100 if self.total_productivity != 0 else 0
        self.sessions = self.get.obtain_total_seshes()
        self.longest_session = self.get.obtain_longest_pom()
        self.results = self.get.most_common_name()[0]
        
        self.most_common = f"{self.results[0]} ({self.results[1]})"



# 4. Total number of pomodoros done
# 5. Total number of pomodoros completed
# 1.Session completion rate
# 2. Average session length
# 3. Productivity rate
# 6. toatl number of sessions donee
# 7. total productiv time
# 8. total break time
# total history per user

class full(tk.Toplevel):
    def __init__(self, master):
        self.width = 800
        self.height = 400

        super().__init__(master)
        self.master = master
        self.user = master.user

        self.get = sqlManage.main_page(self.user)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width/2) - (self.width/2)
        y = (screen_height/2) - (self.height/2)
        self.geometry('%dx%d+%d+%d' % (self.width, self.height, x, y))

        self.resizable(False, False)
        self.title("Pomodoro History")
        self.mainframe = tk.Frame(self, width=self.width, height=self.height, bg="#002B4D")
        self.mainframe.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        self.subframe = tk.Frame(self.mainframe, width=self.width, height=self.height, bg="#013259")
        self.subframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(self.subframe, bg="#013259", width=self.width, height=self.height)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.scrollbar = tk.Scrollbar(self.subframe, command=self.canvas.yview)
        # self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.scrollbar.place(relx=0.995, rely=0, relheight=1, anchor=tk.NE)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.results_frame = tk.Frame(self.canvas, bg="#013259")
        self.canvas.create_window((0, 0), window=self.results_frame, anchor=tk.NW)
        self.res = (self.get.obtain_last_30_entries_without_fist_column())
        
        self.widths = [10, 16, 16, 6, 6, 7, 7, 7, 6]
        self.headings = ["Name", "Start time", "End time", "Sessions", "Pauses", "Completed","Duration", "Productivity", "Break"]
        for j in range(len(self.headings)):
            e = tk.Label(self.results_frame, width=self.widths[j], fg='white', bg='#002B4D', font=('Bodoni 72', 15)) 
            e.grid(row=0, column=j) 
            e.config(state=tk.DISABLED,text=self.headings[j])
        
        for i, student in enumerate(self.res): 
            for j in range(len(student)):
                e = tk.Label(self.results_frame, width=self.widths[j], fg='white', bg='#013259', font=('Bodoni 72', 14)) 
                e.grid(row=i+1, column=j) 
                e.config(state=tk.DISABLED,text=self.res[i][j])
        
        self.results_frame.update_idletasks()
        
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

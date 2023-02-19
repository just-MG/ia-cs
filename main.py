import login_frame
import tkinter as tk
import sqlManage

def main():
    root = tk.Tk()
    root.title('Pomodoro Login')
    root.resizable(False, False)
    app = login_frame.login(root)
    app.pack()
    root.mainloop()

if __name__ == "__main__":
    #print(sqlManage.return_users())
    # sqlManage.reset_table()

    main()
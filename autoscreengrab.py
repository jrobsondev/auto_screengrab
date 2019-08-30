import tkinter as tk
from tkinter import filedialog

class mainWindow:
    def __init__(self):
        #? Variables
        HEIGHT = 300
        WIDTH = 400
        self.root = tk.Tk()
        #! PRESENTATION LAYER !#

        #? Canvas
        self.canvas = tk.Canvas(self.root, height=HEIGHT, width=WIDTH)
        self.canvas.pack()
        #? Folder select
        self.frameFolderSelect = tk.Frame(self.root)
        self.frameFolderSelect.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.2, anchor='n')
        self.lblFolderSelect = tk.Label(self.frameFolderSelect, text='Save Location')
        self.lblFolderSelect.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entryFolderSelect = tk.Entry(self.frameFolderSelect, )
        self.entryFolderSelect.place(relx=0, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')
        self.btnFolderSelect = tk.Button(self.frameFolderSelect, text='browse', command = self.BtnFolderSelectPressed)
        self.btnFolderSelect.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')

        #? Interval
        self.frameInterval = tk.Frame(self.root)
        self.frameInterval.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.2, anchor='n')
        self.lblInterval = tk.Label(self.frameInterval, text='Interval')
        self.lblInterval.place(relx=0, rely=0, relwidth=0.15, relheight=0.25, anchor='nw')
        self.entryInterval = tk.Entry(self.frameInterval, justify='center')
        self.entryInterval.place(relx=0, rely=0.5, relwidth=0.2, relheight=0.5, anchor='w')
        self.lblMinutes = tk.Label(self.frameInterval, text='minutes')
        self.lblMinutes.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=0.5, anchor='w')

        #? Info section
        self.frameInfo = tk.Frame(self.root)
        self.frameInfo.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.1, anchor='n')
        self.lblScreenshotsTaken = tk.Label(self.frameInfo, text=f'Screenshots taken: ')
        self.lblScreenshotsTaken.place(relx=0.5, rely=0, relwidth=0.8, relheight=0.45, anchor='n')
        self.lblTimeRunning = tk.Label(self.frameInfo, text=f'Time Running: ')
        self.lblTimeRunning.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor='n')

        #? Start/Stop buttons
        self.frameStartStop = tk.Frame(self.root)
        self.frameStartStop.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor='n')
        self.btnStart = tk.Button(self.frameStartStop, text='start', command = self.BtnStartPressed)
        self.btnStart.place(relx=0, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')
        self.btnStop = tk.Button(self.frameStartStop, text='stop', state='disabled', command = self.BtnStopPressed)
        self.btnStop.place(relx=0.6, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')

        self.root.mainloop()

        #! BUSINESS LAYER !#

    def BtnFolderSelectPressed(self):
        file_path = filedialog.askdirectory()
        self.entryFolderSelect.delete(0, 'end')
        self.entryFolderSelect.insert(0, file_path)

    def BtnStartPressed(self):
        #? Enable stop button
        self.btnStop.config(state='active')
        #? Disable start button, browse button, interval entry
        self.btnStart.config(state='disabled')
        self.btnFolderSelect.config(state='disabled')
        self.entryInterval.config(state='readonly')
        #TODO: Start timer
        #TODO: Update screenshots taken

    def BtnStopPressed(self):
        #? Disable stop button
        self.btnStop.config(state='disabled')
        #? Enable start button, browse button, interval entry
        self.btnStart.config(state='active')
        self.btnFolderSelect.config(state='active')
        self.entryInterval.config(state='normal')
        #TODO: open popup window prompting to open screenshot folder

if __name__ == '__main__':
    mainWindow = mainWindow()
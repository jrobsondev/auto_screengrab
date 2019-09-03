import tkinter as tk
from tkinter import filedialog
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage
import os

class mainWindow:
    #? Variables
    HEIGHT = 300
    WIDTH = 400
    running = True
    callback = None
    screenshotCount = 1

    def __init__(self):
        #! PRESENTATION LAYER !#
        #? Start root
        self.root = tk.Tk()

        #? Canvas
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        #? Folder select
        self.frameFolderSelect = tk.Frame(self.root)
        self.frameFolderSelect.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.2, anchor='n')
        self.lblFolderSelect = tk.Label(self.frameFolderSelect, text='Save Location')
        self.lblFolderSelect.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entryFolderSelect = tk.Entry(self.frameFolderSelect, state="readonly")
        self.entryFolderSelect.place(relx=0, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')
        self.btnFolderSelect = tk.Button(self.frameFolderSelect, text='browse', command = self.BtnFolderSelectPressed)
        self.btnFolderSelect.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')

        #? Interval
        self.frameInterval = tk.Frame(self.root)
        self.frameInterval.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.2, anchor='n')
        self.lblInterval = tk.Label(self.frameInterval, text='Interval (mins)')
        self.lblInterval.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entryInterval = tk.Entry(self.frameInterval, justify='center')
        self.entryInterval.place(relx=0, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')
        self.entryInterval.insert(0, '1')

        #? Project name
        self.lblProjectName = tk.Label(self.frameInterval, text='Project Name')
        self.lblProjectName.place(relx=0.3, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entryProjectName = tk.Entry(self.frameInterval)
        self.entryProjectName.place(relx=0.3, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')

        #? Info section
        self.frameInfo = tk.Frame(self.root)
        self.frameInfo.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.1, anchor='n')
        self.lblScreenshotsTaken = tk.Label(self.frameInfo, text=f'Screenshots taken: 0')
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

        #? End root
        self.root.mainloop()

    #! BUSINESS LAYER !#
    def BtnFolderSelectPressed(self):
        self.entryFolderSelect.config(state='normal')
        filePath = filedialog.askdirectory()
        self.entryFolderSelect.delete(0, 'end')
        self.entryFolderSelect.insert(0, filePath)
        self.entryFolderSelect.config(state='readonly')

    def BtnStartPressed(self):
        interval = int(self.entryInterval.get())
        self.running = True
        self.lblScreenshotsTaken.config(text='Screenshots taken: 0')
        #? Enable stop button
        self.btnStop.config(state='active')
        #? Disable start button, browse button, interval entry, project name
        self.btnStart.config(state='disabled')
        self.btnFolderSelect.config(state='disabled')
        self.entryInterval.config(state='readonly')
        self.entryProjectName.config(state='readonly')
        #TODO: Start timer
        #? Take screenshot
        self.TakeScreenshot(interval)
        #? Start updating screenshots taken
        self.UpdateLblScreenshotsTaken(interval)

    def BtnStopPressed(self):
        #? Disable stop button
        self.btnStop.config(state='disabled')
        #? Enable start button, browse button, interval entry, project name
        self.btnStart.config(state='active')
        self.btnFolderSelect.config(state='active')
        self.entryInterval.config(state='normal')
        self.entryProjectName.config(state='normal')
        #TODO: open popup window prompting to open screenshot folder
        #? Stop updating screenshots taken
        self.running = False
        self.root.after_cancel(self.callback)
        #? Reset screenshot count back to 1
        self.screenshotCount = 1

    def UpdateLblScreenshotsTaken(self, interval):
        if self.running:
            screenshots_taken = int(self.lblScreenshotsTaken.cget('text').split(':')[1].strip())
            screenshots_taken = screenshots_taken + 1
            #! change interval multiplication back to *60000
            self.lblScreenshotsTaken.config(text=f'Screenshots taken: {str(screenshots_taken)}')
            self.callback = self.root.after(interval*6000, lambda: self.UpdateLblScreenshotsTaken(int(self.entryInterval.get())))

    def TakeScreenshot(self, interval):
        if self.running:
            screen = getRectAsImage(getDisplayRects()[1])
            filePath = self.entryFolderSelect.get()
            fileName = self.entryProjectName.get() + '_' + str(self.screenshotCount) + '.png'
            screen.save(os.path.join(filePath, fileName), format='png')
            self.screenshotCount += 1
            #! change interval multiplication back to *60000
            self.callback = self.root.after(interval*6000, lambda: self.TakeScreenshot(int(self.entryInterval.get())))

if __name__ == '__main__':
    mainWindow = mainWindow()
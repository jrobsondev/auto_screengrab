import tkinter as tk

HEIGHT = 300
WIDTH = 400

root = tk.Tk()

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

#? Folder select
frameFolderSelect = tk.Frame(root)
frameFolderSelect.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.2, anchor='n')
lblFolderSelect = tk.Label(frameFolderSelect, text='Save Location')
lblFolderSelect.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
entryFolderSelect = tk.Entry(frameFolderSelect)
entryFolderSelect.place(relx=0, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')
btnFolderSelect = tk.Button(frameFolderSelect, text='browse')
btnFolderSelect.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')

#? Interval
frameInterval = tk.Frame(root)
frameInterval.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.2, anchor='n')
lblInterval = tk.Label(frameInterval, text='Interval')
lblInterval.place(relx=0, rely=0, relwidth=0.15, relheight=0.25, anchor='nw')
entryInterval = tk.Entry(frameInterval, justify='center')
entryInterval.place(relx=0, rely=0.5, relwidth=0.2, relheight=0.5, anchor='w')
lblMinutes = tk.Label(frameInterval, text='minutes')
lblMinutes.place(relx=0.25, rely=0.5, relwidth=0.15, relheight=0.5, anchor='w')

#? Info section
frameInfo = tk.Frame(root)
frameInfo.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.1, anchor='n')
lblScreenshotsTaken = tk.Label(frameInfo, text=f'Screenshots taken: ')
lblScreenshotsTaken.place(relx=0.5, rely=0, relwidth=0.8, relheight=0.45, anchor='n')
lblTimeRunning = tk.Label(frameInfo, text=f'Time Running: ')
lblTimeRunning.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor='n')

#? Start/Stop buttons
frameStartStop = tk.Frame(root)
frameStartStop.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor='n')
btnStart = tk.Button(frameStartStop, text='start')
btnStart.place(relx=0, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')
btnStop = tk.Button(frameStartStop, text='stop')
btnStop.place(relx=0.6, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')

root.mainloop()
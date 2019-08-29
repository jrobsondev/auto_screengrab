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



#? Info section



#? Start/Stop buttons

root.mainloop()
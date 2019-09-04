import tkinter as tk
from tkinter import filedialog
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage
import os


class MainWindow:
    # ? Variables
    HEIGHT = 300
    WIDTH = 400
    running = True
    callback = None
    screenshotCount = 1

    def __init__(self):
        # ! PRESENTATION LAYER !#
        # ? Start root
        self.root = tk.Tk()

        # ? Canvas
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        # ? Folder select
        self.frame_folder_select = tk.Frame(self.root)
        self.frame_folder_select.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.2, anchor='n')
        self.lbl_folder_select = tk.Label(self.frame_folder_select, text='Save Location')
        self.lbl_folder_select.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entry_folder_select = tk.Entry(self.frame_folder_select, state="readonly")
        self.entry_folder_select.place(relx=0, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')
        self.btn_folder_select = tk.Button(self.frame_folder_select, text='browse',
                                           command=self.btn_folder_select_pressed)
        self.btn_folder_select.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')

        # ? Interval
        self.frame_interval = tk.Frame(self.root)
        self.frame_interval.place(relx=0.5, rely=0.3, relwidth=0.9, relheight=0.2, anchor='n')
        self.lbl_interval = tk.Label(self.frame_interval, text='Interval (mins)')
        self.lbl_interval.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entry_interval = tk.Entry(self.frame_interval, justify='center')
        self.entry_interval.place(relx=0, rely=0.5, relwidth=0.25, relheight=0.5, anchor='w')
        self.entry_interval.insert(0, '1')

        # ? Project name
        self.lbl_project_name = tk.Label(self.frame_interval, text='Project Name')
        self.lbl_project_name.place(relx=0.3, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entry_project_name = tk.Entry(self.frame_interval)
        self.entry_project_name.place(relx=0.3, rely=0.5, relwidth=0.7, relheight=0.5, anchor='w')

        # ? Info section
        self.frame_info = tk.Frame(self.root)
        self.frame_info.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.1, anchor='n')
        self.lbl_screenshots_taken = tk.Label(self.frame_info, text=f'Screenshots taken: 0')
        self.lbl_screenshots_taken.place(relx=0.5, rely=0, relwidth=0.8, relheight=0.45, anchor='n')
        self.lbl_time_running = tk.Label(self.frame_info, text=f'Time Running: ')
        self.lbl_time_running.place(relx=0.5, rely=0.5, relwidth=0.8, relheight=0.5, anchor='n')

        # ? Start/Stop buttons
        self.frame_start_stop = tk.Frame(self.root)
        self.frame_start_stop.place(relx=0.5, rely=0.75, relwidth=0.9, relheight=0.2, anchor='n')
        self.btn_start = tk.Button(self.frame_start_stop, text='start', command=self.btn_start_pressed)
        self.btn_start.place(relx=0, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')
        self.btn_stop = tk.Button(self.frame_start_stop, text='stop', state='disabled', command=self.btn_stop_pressed)
        self.btn_stop.place(relx=0.6, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')

        # ? End root
        self.root.mainloop()

    # ! BUSINESS LAYER !#
    def btn_folder_select_pressed(self):
        self.entry_folder_select.config(state='normal')
        file_path = filedialog.askdirectory()
        self.entry_folder_select.delete(0, 'end')
        self.entry_folder_select.insert(0, file_path)
        self.entry_folder_select.config(state='readonly')

    def btn_start_pressed(self):
        interval = int(self.entry_interval.get())
        self.running = True
        self.lbl_screenshots_taken.config(text='Screenshots taken: 0')
        # ? Enable stop button
        self.btn_stop.config(state='active')
        # ? Disable start button, browse button, interval entry, project name
        self.btn_start.config(state='disabled')
        self.btn_folder_select.config(state='disabled')
        self.entry_interval.config(state='readonly')
        self.entry_project_name.config(state='readonly')
        # TODO: Start timer
        # ? Take screenshot
        self.take_screenshot(interval)
        # ? Start updating screenshots taken
        self.update_lbl_screenshots_taken(interval)

    def btn_stop_pressed(self):
        # ? Disable stop button
        self.btn_stop.config(state='disabled')
        # ? Enable start button, browse button, interval entry, project name
        self.btn_start.config(state='active')
        self.btn_folder_select.config(state='active')
        self.entry_interval.config(state='normal')
        self.entry_project_name.config(state='normal')
        # TODO: open popup window prompting to open screenshot folder
        # ? Stop updating screenshots taken
        self.running = False
        self.root.after_cancel(self.callback)
        # ? Reset screenshot count back to 1
        self.screenshotCount = 1

    def update_lbl_screenshots_taken(self, interval):
        if self.running:
            screenshots_taken = int(self.lbl_screenshots_taken.cget('text').split(':')[1].strip())
            screenshots_taken = screenshots_taken + 1
            # ! change interval multiplication back to *60000
            self.lbl_screenshots_taken.config(text=f'Screenshots taken: {str(screenshots_taken)}')
            self.callback = self.root.after(interval * 6000,
                                            lambda: self.update_lbl_screenshots_taken(int(self.entry_interval.get())))

    def take_screenshot(self, interval):
        if self.running:
            screen = getRectAsImage(getDisplayRects()[1])
            file_path = self.entry_folder_select.get()
            file_name = self.entry_project_name.get() + '_' + str(self.screenshotCount) + '.png'
            screen.save(os.path.join(file_path, file_name), format='png')
            self.screenshotCount += 1
            # ! change interval multiplication back to *60000
            self.callback = self.root.after(interval * 6000,
                                            lambda: self.take_screenshot(int(self.entry_interval.get())))


if __name__ == '__main__':
    mainWindow = MainWindow()

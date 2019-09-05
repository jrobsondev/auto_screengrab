import tkinter as tk
from tkinter import filedialog
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage
import os
import glob


class MainWindow:
    # ? Variables
    HEIGHT = 300
    WIDTH = 400
    running = True
    callbacks = []
    screenshot_count = 0

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
        # ? Check folder for project files with the same name and set screenshots_taken variable
        # ! If this returns true it sets the screenshots taken to 1 more than there is - need to fix
        file_path = self.entry_folder_select.get()
        project_name = self.entry_project_name.get()
        tmp_screenshots_taken = self.check_folder_for_files(file_path, project_name)
        if tmp_screenshots_taken is not None:
            self.screenshot_count = tmp_screenshots_taken
            self.lbl_screenshots_taken.config(text=f'Screenshots taken: {str(self.screenshot_count)}')
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
        for callback in self.callbacks:
            self.root.after_cancel(callback)
        # ? Reset screenshot count back to 1
        self.screenshot_count = 1

    def update_lbl_screenshots_taken(self, interval):
        if self.running:
            screenshots_taken = int(self.lbl_screenshots_taken.cget('text').split(':')[1].strip())
            screenshots_taken = screenshots_taken + 1
            # ! change interval multiplication back to *60000
            self.lbl_screenshots_taken.config(text=f'Screenshots taken: {str(screenshots_taken)}')
            self.callbacks.append(self.root.after(interval * 6000,
                                                  lambda: self.update_lbl_screenshots_taken(
                                                      int(self.entry_interval.get()))))

    def take_screenshot(self, interval):
        if self.screenshot_count == 0:
            self.screenshot_count = 1
        if self.running:
            screen = getRectAsImage(getDisplayRects()[0])
            file_path = self.entry_folder_select.get()
            file_name = self.entry_project_name.get() + '_' + str(self.screenshot_count) + '.png'
            screen.save(os.path.join(file_path, file_name), format='png')
            self.screenshot_count += 1
            # ! change interval multiplication back to *60000
            self.callbacks.append(self.root.after(interval * 6000,
                                                  lambda: self.take_screenshot(int(self.entry_interval.get()))))

    @staticmethod
    def check_folder_for_files(folder_path, project_name):
        list_dir = os.listdir(folder_path)
        list_dir = [file.lower() for file in glob.glob(f'{os.path.join(folder_path, project_name)}*.png')]
        if len(list_dir) != 0:
            list_dir.sort(key=lambda x: os.path.getctime(x))
            last_file = list_dir[-1]
            last_file_number = last_file.split('_')[-1]
            last_file_number = int(last_file_number.split('.')[0]) + 1
            return last_file_number
        return None


if __name__ == '__main__':
    mainWindow = MainWindow()

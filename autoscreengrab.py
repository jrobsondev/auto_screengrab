import time
import tkinter as tk
from tkinter import filedialog
from desktopmagic.screengrab_win32 import getDisplayRects, getRectAsImage, getScreenAsImage, getDisplaysAsImages
import os
import glob


class MainWindow:
    def __init__(self):
        # ? Start root
        self.root = tk.Tk()
        self.root.wm_title('Auto Screengrab')
        self.root.iconbitmap('icons\\app_logo.ico')
        # ? Variables
        self.HEIGHT = 300
        self.WIDTH = 400
        self.running = True
        self.callbacks = []
        self.screenshot_count = 0
        self.is_resuming = False
        self.timestr = tk.StringVar()
        self.timer_start = 0.0
        self.timer_elapsedtime = 0.0
        # ? Constants
        self.MILLI_TO_MINS = 60000

        # ! PRESENTATION LAYER !#
        # ? Canvas
        self.canvas = tk.Canvas(self.root, height=self.HEIGHT, width=self.WIDTH)
        self.canvas.pack()

        # ? Folder select
        self.frame_folder_select = tk.Frame(self.root)
        self.frame_folder_select.place(relx=0.5, rely=0.1, relwidth=0.9, relheight=0.2, anchor='n')
        self.lbl_folder_select = tk.Label(self.frame_folder_select, text='Save Location')
        self.lbl_folder_select.place(relx=0, rely=0, relwidth=0.25, relheight=0.25, anchor='nw')
        self.entry_folder_select = tk.Entry(self.frame_folder_select, state='readonly')
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
        self.frame_info.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.2, anchor='n')
        self.lbl_screenshots_taken = tk.Label(self.frame_info, text='Screenshots taken: 0')
        self.lbl_screenshots_taken.place(relx=0, rely=0.2, relwidth=0.5, relheight=0.45, anchor='w')
        self.lbl_time_running = tk.Label(self.frame_info, textvariable=self.timestr)
        self.lbl_time_running.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5, anchor='w')
        self.timer_set_time(self.timer_elapsedtime)

        # ? Screen selection
        self.screen_dict = {3: 'All screens', 4: 'All screens (separate)'}
        self.screens = self.get_screens()
        self.selected_screen = tk.StringVar(self.root)
        self.selected_screen.set(self.screens.get(0))
        self.lbl_screens = tk.Label(self.frame_info, text='Select screen')
        self.lbl_screens.place(relx=0.6, rely=0.1, relwidth=0.4, relheight=0.3, anchor='w')
        self.dropdown_screens = tk.OptionMenu(self.frame_info, self.selected_screen, *self.screens.values())
        self.dropdown_screens.place(relx=0.6, rely=0.5, relwidth=0.4, relheight=0.5, anchor='w')
        caret = tk.PhotoImage(file='icons\\caret-down.png')
        self.dropdown_screens.config(indicatoron=0)
        self.lbl_caret = tk.Label(self.dropdown_screens, image=caret)
        self.lbl_caret.place(relx=0.8, rely=0, relwidth=0.2, relheight=1)

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
        self.validate()
        if self.running:
            interval = int(self.entry_interval.get())
            self.lbl_screenshots_taken.config(text='Screenshots taken: 0')
            # TODO: Start timer
            # ? Check folder for project files with the same name and set screenshots_taken variable
            file_path = self.entry_folder_select.get()
            project_name = self.entry_project_name.get()
            tmp_screenshots_taken = self.check_folder_for_files(file_path, project_name)
            if tmp_screenshots_taken is not None:
                warning_popup = Popup('Warning',
                                      'A Project already exists with this name.\n'
                                      'Would you like to carry on with this project?')
                warning_popup.yes_no()
                if warning_popup.result:
                    self.is_resuming = True
                    self.screenshot_count = tmp_screenshots_taken
                    self.lbl_screenshots_taken.config(text=f'Screenshots taken: {str(self.screenshot_count)}')
                else:
                    self.running = False
            if self.running:
                # ? Enable stop button
                self.btn_stop.config(state='active')
                # ? Disable start button, browse button, interval entry, project name
                self.btn_start.config(state='disabled')
                self.btn_folder_select.config(state='disabled')
                self.dropdown_screens.config(state='disabled')
                self.entry_interval.config(state='readonly')
                self.entry_project_name.config(state='readonly')
                for key, value in self.screen_dict.items():
                    if self.selected_screen.get() == value:
                        screen_index = key
                # ? Start timer
                self.timer_elapsedtime = 0.0
                self.timer_start = time.time() - self.timer_elapsedtime
                self.timer_update()
                # ? Take screenshot
                self.take_screenshot(interval, screen_index)
                # ? Start updating screenshots taken
                self.update_lbl_screenshots_taken(interval)

    def btn_stop_pressed(self):
        # ? Disable stop button
        self.btn_stop.config(state='disabled')
        # ? Enable start button, browse button, interval entry, project name
        self.btn_start.config(state='active')
        self.btn_folder_select.config(state='active')
        self.dropdown_screens.config(state='active')
        self.entry_interval.config(state='normal')
        self.entry_project_name.config(state='normal')
        # ? Stop updating screenshots taken
        self.running = False
        # ? Reset timer
        self.timer_elapsedtime = time.time() - self.timer_start
        self.timer_set_time(self.timer_elapsedtime)
        for callback in self.callbacks:
            self.root.after_cancel(callback)
        # ? Reset screenshot count back to 1
        self.screenshot_count = 1
        # ? open popup window prompting to open screenshot folder
        warning_popup = Popup('Warning', 'Would you like to to view the screenshots taken for this project?')
        warning_popup.yes_no()
        if warning_popup.result:
            path_to_open = os.path.realpath(self.entry_folder_select.get())
            os.startfile(path_to_open)

    def update_lbl_screenshots_taken(self, interval):
        if self.running:
            if not self.is_resuming:
                screenshots_taken = int(self.lbl_screenshots_taken.cget('text').split(':')[1].strip())
                screenshots_taken = screenshots_taken + 1
                # ! change interval multiplication back to *60000
                self.lbl_screenshots_taken.config(text=f'Screenshots taken: {str(screenshots_taken)}')
                self.callbacks.append(self.root.after(interval * self.MILLI_TO_MINS,
                                                      lambda: self.update_lbl_screenshots_taken(
                                                          int(self.entry_interval.get()))))
            else:
                self.is_resuming = False
                self.callbacks.append(self.root.after(interval * self.MILLI_TO_MINS,
                                                      lambda: self.update_lbl_screenshots_taken(
                                                          int(self.entry_interval.get()))))

    def take_screenshot(self, interval, screen_index):
        if self.screenshot_count == 0:
            self.screenshot_count = 1
        if self.running:
            file_path = self.entry_folder_select.get()
            file_name = self.entry_project_name.get() + '_' + str(self.screenshot_count) + '.png'
            if self.selected_screen.get() == 'Screen 1' or self.selected_screen.get() == 'Screen 2':
                screen = getRectAsImage(getDisplayRects()[screen_index])
                screen.save(os.path.join(file_path, file_name), format='png')
                self.screenshot_count += 1
                # ! change interval multiplication back to *60000
                self.callbacks.append(self.root.after(interval * self.MILLI_TO_MINS,
                                                      lambda: self.take_screenshot(int(self.entry_interval.get()),
                                                                                   screen_index)))
            elif self.selected_screen.get() == 'All screens':
                entire_screen = getScreenAsImage()
                entire_screen.save(os.path.join(file_path, file_name), format='png')
                self.screenshot_count += 1
                self.callbacks.append(self.root.after(interval * self.MILLI_TO_MINS,
                                                      lambda: self.take_screenshot(int(self.entry_interval.get()),
                                                                                   screen_index)))
            elif self.selected_screen.get() == 'All screens (separate)':
                for screen_number, image in enumerate(getDisplaysAsImages(), 1):
                    file_name = self.entry_project_name.get() + '_' + str(self.screenshot_count)\
                                + '_screen' + str(screen_number) + '.png'
                    image.save(os.path.join(file_path, file_name), format='png')
                self.screenshot_count += 1
                self.callbacks.append(self.root.after(interval * self.MILLI_TO_MINS,
                                                      lambda: self.take_screenshot(int(self.entry_interval.get()),
                                                                                   screen_index)))

    @staticmethod
    def check_folder_for_files(folder_path, project_name):
        list_dir = os.listdir(folder_path)
        list_dir = [file.lower() for file in glob.glob(f'{os.path.join(folder_path, project_name)}_*.png')]
        if len(list_dir) != 0:
            list_dir.sort(key=lambda x: os.path.getctime(x))
            last_file = list_dir[-1]
            last_file_number = last_file.split('_')[-1]
            last_file_number = int(last_file_number.split('.')[0]) + 1
            return last_file_number
        return None

    def validate(self):
        entries = { self.entry_folder_select: 'Folder Select',
                    self.entry_project_name: 'Project Name',
                    self.entry_interval: 'Interval'}
        for entry in entries:
            entry_text = entry.get()
            # ? Make sure that all entries have a value.
            if not entry_text:
                entry.config(bg='YELLOW')
                error_popup = Popup('Error!', f'You have forgotten to complete the {entries.get(entry)} field.')
                error_popup.okay()
                self.running = False
                return
            entry.config(bg='WHITE')
        # ? Make sure that interval is an integer, not a string.
        if not self.entry_interval.get().isdigit():
            self.entry_interval.config(bg='YELLOW')
            error_popup = Popup('Error!', 'Please enter a numeric value for interval')
            error_popup.okay()
            self.running = False
            return
        self.running = True

    def get_screens(self):
        for index, screen in enumerate(getDisplayRects()):
            self.screen_dict[index] = f'Screen {str(index + 1)}'
        return self.screen_dict

    def timer_set_time(self, elap):
        hours, rem = divmod(elap, 3600)
        minutes, seconds = divmod(rem, 60)
        self.timestr.set('Time Running: {:0>2}:{:0>2}:{:0>2}'.format(int(hours), int(minutes), int(seconds)))

    def timer_update(self):
        self.timer_elapsedtime = time.time() - self.timer_start
        self.timer_set_time(self.timer_elapsedtime)
        self.callbacks.append(self.root.after(50, self.timer_update))


class Popup:

    def __init__(self, title, msg):
        self.title = title
        self.msg = msg
        self.result = True

    def setup_window(self):
        self.popup.wm_title(self.title)
        self.popup_canvas = tk.Canvas(self.popup, height='110', width='250')
        self.popup_canvas.pack()
        self.popup_frame_msg = tk.Frame(self.popup)
        self.popup_frame_msg.place(relx=0.5, rely=0, relwidth=0.9, relheight=0.6, anchor='n')
        self.lbl_popup = tk.Label(self.popup_frame_msg, text=self.msg, wraplength=230)
        self.lbl_popup.place(relx=0.5, rely=0, relwidth=1, relheight=1, anchor='n')
        self.popup_frame_btns = tk.Frame(self.popup)
        self.popup_frame_btns.place(relx=0.5, rely=0.7, relwidth=0.9, relheight=0.3, anchor='n')

        # TODO: Disable all controls whilst popup is open

    def yes_no(self):
        # TODO: Add function parameters and pass them to the yes/no buttons
        self.popup = tk.Tk()
        self.setup_window()
        self.btn_popup_yes = tk.Button(self.popup_frame_btns, text='Yes', command=lambda: self.popup_result(1))
        self.btn_popup_yes.place(relx=0, rely=0.5, relwidth=0.4, relheight=0.8, anchor='w')
        self.btn_popup_no = tk.Button(self.popup_frame_btns, text='No', command=lambda: self.popup_result(0))
        self.btn_popup_no.place(relx=0.6, rely=0.5, relwidth=0.4, relheight=0.8, anchor='w')
        self.popup.wait_window()

    def popup_result(self, value):
        if value == 1:
            MainWindow.running = True
            self.result = True
            self.popup.destroy()
        elif value == 0:
            MainWindow.running = False
            self.result = False
            self.popup.destroy()

    def okay(self):
        self.popup = tk.Tk()
        self.setup_window()
        self.btn_popup_okay = tk.Button(self.popup_frame_btns, text='OK', command=self.popup.destroy)
        self.btn_popup_okay.place(relx=0.5, rely=0, relwidth=0.4, relheight=0.8, anchor='n')
        self.popup.wait_window()


if __name__ == '__main__':
    mainWindow = MainWindow()

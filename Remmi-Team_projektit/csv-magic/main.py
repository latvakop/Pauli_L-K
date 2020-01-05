import matplotlib.pyplot as plt
import numpy as np
import tkinter
from tkinter import messagebox
import re

class Ui():
    def __init__(self):
        self.mainwindow = tkinter.Tk()
        self.mainwindow.title("CSV-magic")
        self.stop_button = tkinter.Button(self.mainwindow, text="Stop", command=self.mainwindow.destroy)

        self.file_label = tkinter.Label(self.mainwindow, text="")
        self.file_label.grid(row=0)
        self.file_name = ""

        self.filename_button = tkinter.Button(self.mainwindow, text="Select filename", command =self.find_filename)
        self.filename_button.grid(row=0, column=1)

        tkinter.Label(self.mainwindow, text="Start reading data from row:").grid(row=3)
        self.start_row_entry = tkinter.Entry(self.mainwindow)
        self.start_row_entry.grid(row=3, column=1)

        tkinter.Label(self.mainwindow, text="Enter a word to be searched:").grid(row=2)
        self.y_axis_entry = tkinter.Entry(self.mainwindow)
        self.y_axis_entry.grid(row=2, column=1)

        tkinter.Label(self.mainwindow, text="Enter a row to search the word from:").grid(row=1)
        self.find_word_entry = tkinter.Entry(self.mainwindow)
        self.find_word_entry.grid(row=1, column=1)

        self.show_file_info_button = tkinter.Button(self.mainwindow, text="Show file info", command=self.show_file_info)
        self.show_file_info_button.grid(row=1, column=2)

        self.run_button = tkinter.Button(self.mainwindow, text="Plot", command=self.calculate)
        self.run_button.grid(row=4, column=1)


    def find_filename(self):
        """
        Lets the user open a desired file and updates the file name to a label.
        """
        self.file_name = tkinter.filedialog.askopenfilename(initialdir='./')
        self.file_label.configure(text=self.file_name)
        return self.file_name

    def __get_quantity(self):
        return '"' + self.y_axis_entry.get() + '"'

    def start_ui(self):
        self.mainwindow.mainloop()

    def __get_filename(self):
        return self.file_name

    def show_file_info(self):
        """
        Function for showing user all the possible quantities that are on the csv file with a pop up window.
        """
        if self.is_input_erroneous():
            return
        file_name = self.__get_filename()

        row_number = int(self.find_word_entry.get())
        with open(file_name) as f:
            line = f.readlines()[row_number - 1].rstrip().strip()

        line_list = line.split(",")
        for i in range(0, len(line_list)):
            line_list[i] = line_list[i].rstrip().strip()
            line_list[i] = line_list[i].lstrip()
            line_list[i] = line_list[i][1:-1]

        new_line = ""
        for i in range(0, len(line_list)):
            if i == len(line_list) - 1:
                new_line += line_list[i]
            else:
                new_line += line_list[i] + ", "


        filename_parts = []
        filename_parts = file_name.split("/")
        file_name_to_show = filename_parts[-1]
        popup_window = tkinter.Tk()
        popup_window.wm_title(f"{file_name_to_show} has the following data on line {row_number}:")
        info_label = tkinter.Label(popup_window, text=new_line)
        info_label.grid(row=0, column=0)


    def read_csv_file(self) :
        """
        Reads a csv file and returns the data values in two lists.

        Returns:
        y_axis_list: list
            List that has all the values of the quantity that the user wanted to search from the csv file.
        time_list: list
            List that has the time values from the csv file.
        """
        file_name = self.__get_filename()
        init_row = self.start_row_entry.get()
        quantity_index = self.read_y_axis_names()
        init_row = int(init_row)
        y_axis_list = []
        time_list = []
        i = 0
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip().rstrip()
                i += 1

                if i < init_row:
                    continue
                if not line:
                    continue
                else:
                    # This reqex splitting is for fixing a bug that was caused because motecs data has a different
                    # type of row for every 100 000 rows.
                    match = re.search(r'\"[0-9]+,[0-9]+\"', line)
                    if match:
                        parts = re.split('\", *\"', line)
                        new_parts = []
                        for part in parts:
                            part = re.sub(',', '.', part)
                            if part[-1] != '"':
                                part += '"'
                            if part[0] != '"':
                                part = '"' + part
                            new_parts.append(part)
                        s = ","
                        line = s.join(new_parts)

                    table = line.split(",")
                    if table[quantity_index] == '""':
                        table[quantity_index] = '"0"'
                    y_axis_list.append(float(table[quantity_index][1:-1]))
                    time_list.append(float(table[0][1:-1]))
        return y_axis_list, time_list

    def read_y_axis_names(self):
        """
        Reads from a line that the user inputs the index of the quantity that the user wants to search

        Returns
        -------
        ind: int
            The index of the quantity on the line
        """
        file_name = self.__get_filename()

        row_number = 0
        if self.find_word_entry.get():
            row_number = int(self.find_word_entry.get())

        quantity = self.__get_quantity()

        line = ""

        with open(file_name) as f:
            line = f.readlines()[row_number - 1].rstrip().strip()

        line =line.split(",")

        try:
            ind = line.index(quantity)
        except ValueError:
            tkinter.messagebox.showerror("Error!", f"Quantity {quantity} not found in data file {file_name}")
            raise ValueError
        return ind

    def is_input_erroneous(self):
        """
        Function for checking input errors and making the program less likely to crash.
        """
        if self.y_axis_entry.get() == "" or self.find_word_entry.get() == "" or self.start_row_entry.get() == "":
            tkinter.messagebox.showerror("Error!", "Empty input field!")
            return True
        try:
                open(self.__get_filename())
        except FileNotFoundError:
            tkinter.messagebox.showerror("Error!", "No file selected!")
            return True
        try:
            int(self.find_word_entry.get())
            int(self.start_row_entry.get())
        except ValueError:
            tkinter.messagebox.showerror("Error!", "Row number must be an integer!")
            return True
        if int(self.start_row_entry.get()) <= int(self.find_word_entry.get()):
            tkinter.messagebox.showerror("Error!", "CSV-format must be before CSV-data")
            return True
        return False

    def calculate(self):
        """
        Plots the y axis against time.
        """
        if self.is_input_erroneous():
            return
        try:
            y_list, time_list = self.read_csv_file()
        except ValueError:
            return
        y_list = np.array(y_list)
        time = np.array(time_list)
        plt.plot(time, y_list)
        plt.xlabel('Time')
        plt.ylabel(self.__get_quantity()[1:-1])
        plt.title(self.__get_quantity()[1:-1] + " graph")
        plt.show()


def main():
    
    ui = Ui()
    ui.start_ui()


if __name__ == '__main__':
    main()

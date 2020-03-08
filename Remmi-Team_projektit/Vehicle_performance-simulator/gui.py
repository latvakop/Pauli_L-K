# Made by: Pauli Latva-Kokko
# Graphical ui for the simulator.

import sys
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMainWindow, QFileDialog, QTextEdit
from PyQt5.QtGui import QFont
from gui_simulator import calculate_result
import configparser
from multiprocessing import Process
from gui_simulator import plt

class Ui():

    def __init__(self):
        """Initializes the GUI"""

        #Mainwindow
        self.window = QWidget()
        self.window.resize(1500, 1500)
        self.window.setWindowTitle("Vehicle simulator")
        self.window.setFont(QFont("Times", 24))
    
        self.track_label = QLabel(self.window)
        self.track_label.setText("Select track")
        self.track_label.move(10, 10)
        
        self.lap_count_label = QLabel(self.window)
        self.lap_count_label.setText("Lap count:")
        self.lap_count_label.move(10, 60)

        self.time_limit_label = QLabel(self.window)
        self.time_limit_label.setText("Time limit(min):")
        self.time_limit_label.move(10, 110)
        
        self.vehicle_parameters_button = QLabel(self.window)
        self.vehicle_parameters_button.setText("Change vehicle parameters:")
        self.vehicle_parameters_button.setGeometry(10, 160, 400, 40)

        self.text_edit = QTextEdit(self.window)
        self.text_edit.setGeometry(10, 210, 400, 280)
        self.text_edit.setFont(QFont("Times", 10))
        self.text_edit.textChanged.connect(self.text_edit_text_changed)

        self.result_label = QLabel(self.window)
        self.result_label.setText("Result:")
        self.result_label.setGeometry(10, 550, 500, 40)

        self.acceleration_start_label = QLabel(self.window)
        self.acceleration_start_label.setText("Acceleration start speed:")
        self.acceleration_start_label.setGeometry(10,600, 500, 40)

        self.acceleration_end_label = QLabel(self.window)
        self.acceleration_end_label.setText("Acceleration end speed:")
        self.acceleration_end_label.move(10, 650)
        self.acceleration_end_label.setGeometry(10,650, 500, 40)

        self.laps_label = QLabel(self.window)
        self.laps_label.setText("Laps driven:")
        self.laps_label.setGeometry(10, 700, 500, 40)

        # Track selection pushbutton
        self.track_push_button = QPushButton(self.window)
        self.track_push_button.setGeometry(250, 7, 300, 40)
        self.track_push_button.clicked.connect(self.open_file_dialog)

        # Lap counter line edit
        self.lap_line_edit = QLineEdit(self.window)
        self.lap_line_edit.setGeometry(250, 57, 300, 40)
        self.lap_line_edit_int = 10
        self.lap_line_edit.textChanged.connect(self.lap_line_edit_changed)
        self.lap_error_label = QLabel(self.window)
        self.lap_error_label.setGeometry(575, 57, 800, 40)

        # max time limit line edit
        self.time_line_edit = QLineEdit(self.window)
        self.time_line_edit.setGeometry(250, 107, 300, 40)
        self.time_line_edit_int = 15
        self.time_line_edit.textChanged.connect(self.time_line_edit_changed)
        self.time_error_label = QLabel(self.window)
        self.time_error_label.setGeometry(575, 107, 800, 40)

        # Simulation start button
        self.simulate_button = QPushButton(self.window)
        self.simulate_button.setText("SIMULATE")
        self.simulate_button.setGeometry(10, 500, 280, 40)
        self.simulate_button.clicked.connect(self.simulate_button_clicked)

        # configuration data
        self.config = configparser.ConfigParser()
        self.result_consumption = 0
        self.text = ""
        self.initialize_text_edit()

        # File name
        self.file_name = ""

        self.window.show()

    def initialize_text_edit(self):
        """
        Initializes the text edit when the program is first run or when the
        file data has been changed
        """
        filename = './constants.ini'
        if filename:
            f = open(filename, 'r')

            with f:
                data = f.read()
                self.text_edit.setText(data)
            f.close()

    def initialize_labels(self):
        """
        Initializes the result labels after the simulation is over.
        """
        self.result_label.setText("Result:")
        self.acceleration_start_label.setText("Acceleration start speed:")
        self.acceleration_end_label.setText("Acceleration end speed:")
        self.laps_label.setText("Laps diven:")

    def open_file_dialog(self):
        self.file_name, arg = QFileDialog.getOpenFileName(self.window, "Open file", "./")
        print(self.file_name)
        self.get_constants_data()
        self.config.set('ENVIRONMENT', 'FILE_NAME', str(self.file_name))
        self.change_constants_data()

    def text_edit_text_changed(self):
        self.text = self.text_edit.toPlainText()
        self.change_vehicle_parameters()

    def change_result(self, result):
        self.result_consumption = result

    def get_constants_data(self):
        self.config.read('./constants.ini')

    def change_constants_data(self):
        with open('./constants.ini', 'w') as file:
            self.config.write(file)

    def change_vehicle_parameters(self):
        """
        Changes the data in the ini file after the user has changed it.
        """
        filename = './constants.ini'
        f = open(filename, 'w')
        f.write(self.text)
        f.close()


    def time_line_edit_changed(self):
        """
        Changes the maximum time limit value in the simulation.
        """
        if self.time_line_edit.text() == "":
            self.time_error_label.setText("")
            return
        try:
            self.time_line_edit_int = int(self.time_line_edit.text())
        except ValueError:
            self.time_error_label.setText("Error! Time limit must be an integer")
            return
        if self.time_line_edit_int < 1:
            self.time_error_label.setText("Error! Time limit must be a positive number")
            return
        self.time_error_label.setText("")
        
    def lap_line_edit_changed(self):
        """
        Changes the maximum laps drived value in the simulation.
        """
        if self.lap_line_edit.text() == "":
            self.lap_error_label.setText("")
            return
        try:
            self.lap_line_edit_int = int(self.lap_line_edit.text())
        except ValueError:
            self.lap_error_label.setText("Error! Lap count must be an integer")
            return
        if self.lap_line_edit_int < 1:
            self.lap_error_label.setText("Error! Lap count must be a positive number")
            return
        self.lap_error_label.setText("")


    def simulate_button_clicked(self):
        """
        Runs the simulation function in gui_simulator.py, uses multiprocessing
        to show the plots and calculate the results at the same time.
        """

        self.get_constants_data()
        self.config.set('EVENT', 'TOTAL_LAPS', str(self.lap_line_edit_int))
        self.config.set('SIMULATION', 'END_TIME', str(self.time_line_edit_int *
                                                      60))

        # Change the values to the ini file and the text editor
        self.change_constants_data()
        self.initialize_text_edit()

        # Run the simulation
        p1 = Process(target=calculate_result, args=(12.97, 35.68, 35, 30, True,
                                                    self.file_name))
        p1.start()
        res, init_speed, end_speed, lap_counter = calculate_result(12.97, 35.68, 35, 30,
                                                      False, self.file_name)

        total_laps = self.config.getint('EVENT', 'TOTAL_LAPS')

        # Update the result labels.
        self.initialize_labels()
        self.result_label.setText(self.result_label.text() + " {0:.2f} km/l".format(res))
        self.acceleration_start_label.setText(self.acceleration_start_label.text() + " {:.2f} km/h".format(init_speed))
        self.acceleration_end_label.setText(self.acceleration_end_label.text() + " {:.2f} km/h".format(end_speed))
        self.laps_label.setText(self.laps_label.text() + str(lap_counter)+ "/" + str(total_laps))

    

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Ui()
    sys.exit(app.exec_())
    



# Made by: Pauli Latva-Kokko


import matplotlib.pyplot as plt

# A class for plotting the data calculated in the program.
class Plotter:
    def __init__(self, x_data, x_label):
        """
        Constructor for the plotting
        Parameters
        ----------
        x_data: list
            X-coordinates of the data
        x_label: string
            Name of the x-label
        """
        self.figure_number_ = 1
        self.x_data_ = x_data
        self.x_label_ = x_label

    def new_plot(self, y_data, y_label_, title, new_figure=True):
        """
        Draws a new plot based on the parameters
        Parameters
        ----------
        y_data: list
            Y-coordinates of the data
        y_label_: string
            The name of the y-label
        title: string
            Title of the plot
        new_figure: boolean
            True = new figure is drawn, False = no new figure is drawn
        Returns
        -------
        """
        if new_figure == True:
            plt.figure(self.figure_number_)
            self.figure_number_ += 1
        plt.plot(self.x_data_, y_data)
        plt.ylabel(y_label_)
        plt.xlabel(self.x_label_)
        plt.title(title)

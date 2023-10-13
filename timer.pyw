from stopwatch import Stopwatch
import tkinter as tk

class App:
    def __init__(self, master):
        self.master = master
        self.stopwatch = Stopwatch()

        self.time_label = tk.Label(self.master, text="0:00:00.00")
        self.time_label.pack()

        self.units_label = tk.Label(self.master, text="Units: 0.00")
        self.units_label.pack()

        self.cost_label = tk.Label(self.master, text="Cost: $0.00")
        self.cost_label.pack()

        self.start_button = tk.Button(self.master, text="Start", command=self.start_stopwatch)
        self.start_button.pack()

        self.reset_button = tk.Button(self.master, text="Reset", command=self.reset_stopwatch)
        self.reset_button.pack()

        self.reset_stopwatch()

        self.update_clock()

    def update_clock(self):
        if self.stopwatch.running:
            elapsed_time = self.format_time(self.stopwatch.duration)
            self.time_label.config(text=elapsed_time)
            units = self.calculate_units(self.stopwatch.duration)
            self.units_label.config(text=f"Units: {units:.2f}")
            cost = self.calculate_cost(units)
            self.cost_label.config(text=f"Cost: ${cost:.2f}")
        self.master.after(50, self.update_clock)

    def start_stopwatch(self):
        if not self.stopwatch.running:
            self.stopwatch.start()
            self.start_button.config(text="Stop")
        else:
            self.stopwatch.stop()
            self.start_button.config(text="Start")

    def reset_stopwatch(self):
        self.stopwatch.reset()
        self.time_label.config(text="0:00:00.00")
        self.units_label.config(text="Units: 0.00")
        self.cost_label.config(text="Cost: $0.00")
        self.start_button.config(text="Start")

    def format_time(self, time_in_seconds):
        minutes, seconds = divmod(time_in_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{int(hours)}:{int(minutes):02d}:{seconds:05.2f}"

    def calculate_units(self, time_in_seconds):
        units = time_in_seconds / (6 * 60)
        return units

    def calculate_cost(self, units):
        return units * 15.0


root = tk.Tk()
app = App(root)
root.mainloop()

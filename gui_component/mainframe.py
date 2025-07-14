from gui_component.components.input import InputComponent
from gui_component.components.process import ProcessComponent
from gui_component.components.output import OutputComponent
from shared import SharedData
import tkinter as tk
import matplotlib.pyplot as plt

class GUI:
    def __init__(self):
        self.root_gui = tk.Tk()
        self.root_gui.title("Solve TSP with CIH")
        self.root_gui.state("zoomed")
        self.output_component = OutputComponent()
        self.process_component = ProcessComponent(self.output_component)
        self.input_component = InputComponent(self.process_component)
        self.frame_utama = self.create_frame_utama()

    def create_frame_utama(self):
        frame = tk.Frame(self.root_gui)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        return frame
    
    def on_closing(self):
        plt.close(SharedData.figure_graf)
        self.root_gui.quit()
        self.root_gui.destroy()

    def run(self):
        self.input_component.create_frame_input(self.frame_utama)
        self.process_component.create_frame_process(self.frame_utama)
        self.output_component.create_frame_output(self.root_gui)

        self.root_gui.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root_gui.mainloop()
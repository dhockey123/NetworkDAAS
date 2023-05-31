from ui_networkdesign import *

class App(Tk):
    def __init__(self):
        super().__init__()
        self.config = {
            'SCREEN_HEIGHT': 900,
            'SCREEN_WIDTH': 1200,
            'BLOCKSIZE': 30
        }
        self.title("Network Dimensioning and Allocation Solver")
        self.geometry("1200x900")
        self.sidedashboard = SideDashBoard(self)
        self.networkdesigntool = NetworkDesignTool(self, self.config)
        self.pack_propagate(0)

if __name__ == "__main__":
    app = App()
    app.mainloop()

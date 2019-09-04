import math
import tkinter as tk

g = 9.81

class app(tk.Frame):
    def __init__(self, master=None, WH = 400):
        super().__init__(master)
        self.master = master
        self.WH = WH
        self.pack()
        self.scale = 800
        self.create_widgets()

    def create_widgets(self):
        self.ok_button = tk.Button(self)
        self.ok_button["text"] = "draw" 
        self.ok_button["command"] = self.draw
        self.ok_button.grid(row = 6, column = 2)

        self.v_slider = tk.Scale(self, from_ = 1, to = 75, orient = tk.HORIZONTAL, length = 300)
        self.v_slider.grid(row = 5, column = 2)
        self.v_label = tk.Label(self, text = "velocity m/s")
        self.v_label.grid(row = 4, column = 2)

        self.d_slider = tk.Scale(self, from_ = 1, to = 89, orient = tk.HORIZONTAL, length = 300)
        self.d_slider.grid(row = 3, column = 2)
        self.d_label = tk.Label(self, text = "degrees from ground")
        self.d_label.grid(row = 2, column = 2)

        self.graph = tk.Canvas(self, width = self.WH+200, height = self.WH)
        self.graph.grid(row = 1, column = 0, columnspan = 3)
        
        self.scaleList = tk.Listbox(self)
        for i in range(200,1000,100):
            self.scaleList.insert(tk.END, str(i))
        self.scaleList.grid(row = 2, column = 1, rowspan = 5)

    def putLines(self):
        pixelDim = self.scale/self.WH
        scaleLineDistance = 10/pixelDim

        i = 0 
        tenCounter = 0
        while i<self.WH+200:
            i += scaleLineDistance
            tenCounter += 1
            if tenCounter==10:
                self.graph.create_line([(i,self.WH), (i,self.WH-20)])
                tenCounter = 0
            else:
                self.graph.create_line([(i,self.WH), (i,self.WH-10)])

        i = 0 
        tenCounter = 0
        while i<self.WH:
            i += scaleLineDistance
            tenCounter += 1
            if tenCounter==10:
                self.graph.create_line([(0, self.WH - i), (20, self.WH - i)])
                tenCounter = 0
            else:
                self.graph.create_line([(0, self.WH - i), (10, self.WH - i)])


    def draw(self):
        self.scale = int(self.scaleList.get(tk.ACTIVE))
        locations = self.calculate(self.v_slider.get(), self.d_slider.get(), self.WH)
        if locations:
            self.graph.delete("all")
            self.putLines()
            self.graph.create_line(locations, smooth = 1, width = 2)

    def calculate(self, v, d, H):

        if d >= 90 or d <= 0 or v <= 0 or v > 100:
            print("bad argument")
            return False

        rad = (d/180)*math.pi
        vy = math.sin(rad)*v
        vx = math.cos(rad)*v
        y = 0
        x = 0
                
        pixelDim = self.scale/self.WH
        locations = []

        while y >= 0:
            y += 0.1*vy
            vy -= 0.1*g
            x += 0.1*vx
            
            locations.append((x/pixelDim,H-(y/pixelDim)))

        return locations

root = tk.Tk()
root.minsize(600,580)
root.maxsize(600,580)
win = app(master=root)
win.mainloop()

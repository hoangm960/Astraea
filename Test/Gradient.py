from tkinter import Canvas

class GradientFrame(Canvas):
    __tag = "GradientFrame"

    hex_format = "#%04x%04x%04x"
    top2bottom = 1
    left2right = 2


    def __init__(self,parent,geometry,colors=("red","black"),direction=top2bottom,**kw):
        
        Canvas.__init__(self,parent,width=geometry[0],height=geometry[1],**kw)

        self.__geometry = geometry
        self.__colors = colors
        self.__direction = direction

        self.__drawGradient()

        
    def __drawGradient(self):

        self.delete(self.__tag)

        limit = self.__geometry[0] if self.__direction == self.left2right else self.__geometry[1]
       
        red1,green1,blue1 = self.winfo_rgb(self.__colors[0])
        red2,green2,blue2 = self.winfo_rgb(self.__colors[1])

        r_ratio = float(red2 - red1) / limit
        g_ratio = float(green2 - green1) / limit
        b_ratio = float(blue2 - blue1) / limit

        for pixel in range(limit):
            
            red = int( red1 + ( r_ratio * pixel ) )
            green = int( green1 + ( g_ratio * pixel ) )
            blue = int( blue1 + ( b_ratio * pixel ) )

            color = self.hex_format % (red,green,blue)

            x1 = pixel if self.__direction == self.left2right else 0
            y1 = 0 if self.__direction == self.left2right else pixel
            x2 = pixel if self.__direction == self.left2right else self.__geometry[0]
            y2 = self.__geometry[1] if self.__direction == self.left2right else pixel

            self.create_line(x1,y1,x2,y2 , tag=self.__tag , fill=color)


    def setColors(self,colors):

        self.__colors = colors
        self.__drawGradient()


    def setDirection(self,direction):

        if direction in (self.left2right,self.top2bottom):
            self.__direction = direction
            self.__drawGradient()
        else:
            raise ValueError('The "direction" parameter must be self.left2right or self.top2bottom')
        

    def setGeometry(self,geometry):

        self.config(width=geometry[0],height=geometry[1])
        self.__geometry = geometry
        self.__drawGradient()

from tkinter import Tk

root = Tk()
gf = GradientFrame(root,[400,400],colors = ("#0d4dff","#00ffa9"))
gf.pack()
root.mainloop()
# Imports
import math 
from PIL import Image, ImageDraw 
import colorsys
import random
import inspect
import pickle
import os
import time
import logging
try:
    from . import patternTemplates
except ImportError: 
    import patternTemplates
# End Imports

# Globals
NoneType = type(None)
logging.basicConfig(filename='app.log',level=logging.DEBUG,format='%(asctime)s %(levelname)-8s < %(funcName)s > %(message)s')
logger = logging.getLogger(__name__)
# End Globals

#Classes
class PatternBase():
    params = {}
    def __init__(self,w=1000,h=1000,path=None,params={}):
        self.initialize(w,h)
        self.params.update(params)
        self.path = path
        logger.debug(str(self.params))

    def initialize(self,width=800,height=800,x_inc = 0,y_inc = 0,
    rand_x_s= 0,rand_x_e = 0,rand_y_s = 0,
    rand_y_e = 0,step_x = 1,step_y = 1,s_degree = 0,e_degree = 360,point_method = '',fill_method = 'fill',color = '#000000'
    ,shape='line'):
        """
        Initialise parameters for pattern. It uses a new Image and canvas.
        Args:
            width: width of Image. Default=800
            height: height of Image. Default=800
            x_inc:  width of shape used. Default=1
            y_inc: height of shape used. Default=1
            rand_x_s: min randomization of shape width. Default=0
            rand_x_e: max randomization of shape width. Default=0
            rand_y_s: min randomization of shape height. Default=0
            rand_y_e: max randomization of shape height. Default=0
            step_x: step size in x direction. Determines next x coordinate. Default=1
            step_y: step size in y direction. Determines next y coordinate. Default=1
            s_degree: Starting degree of arc. Default=0. Applicable only with Outline draw with arcs
            e_degree: End degree of arc. Default=360. Applicable only with Outline draw with arcs
            point_method: convolution method. Determines how shapes are populated in canvas
            fill_method: fill or outline. Determines shape colouring
            color: shape color
        """
         
        self.getNewImage(width,height)
        self.visited = []
        self.methods = [self.forward,self.backward,self.left,self.right]

        #Params Initialization
        self.params['canvas'] = self.getNewCanvas(width,height)
        self.params['width'] = width
        self.params['height'] = height
        self.params['x_inc'] = x_inc   
        self.params['y_inc'] = y_inc
        self.params['step_x'] = step_x  
        self.params['step_y'] = step_y 
        self.params['rand_x_s'] = rand_x_s   
        self.params['rand_x_e'] = rand_x_e
        self.params['rand_y_s'] = rand_y_s   
        self.params['rand_y_e'] = rand_y_e
        self.params['s_degree'] = s_degree
        self.params['e_degree'] = e_degree
        self.params['point_method'] = point_method
        self.params['fill_method'] = fill_method
        self.params['color'] = color
        self.params['shape'] = shape

    def updateParams(self,params):
        self.params.update(params)
        
    def getParam(self,key,default=None):
        if key in ['width','height','x_inc','y_inc','step_x','step_y','rand_x_s','rand_x_e','rand_y_s','rand_y_e','s_degree','e_degree']:
            return int(self.params.get(key,default))
        else:
            return self.params.get(key,default)

    def getNewCanvas(self,width=1000,height=1000):
        canvas = ImageDraw.Draw(self.image)
        self.canvas = canvas
        return canvas

    def getNewImage(self,width,height,mode="RGB"):
        image = Image.new(mode, (width, height)) 
        print(image)
        self.image = image

    def getCanvas(self):
        return self.canvas

    def WriteText(self,text):
        self.textFilePointer = open(self.path+'/details.jst','a')
        self.textFilePointer.write(text+'\n')
        self.textFilePointer.close()

    def saveText(self,filename):
        self.WriteText('\n\n**************************')
        self.WriteText('Filename: '+str(filename))
        for key,value in self.params.items():
            self.WriteText(str(key)+': '+str(value))

    def saveImage(self,filename,text=True):
        filename = self.path+'/'+filename
        self.image.save(filename)
        if text == True:
            self.saveText(filename)
    def showImage(self):
        self.image.show()

    def getRandomColour(self):
        self.current_color = '#{}{}{}'.format(self.getColourHex(self.randRGB()),self.getColourHex(self.randRGB()),self.getColourHex(self.randRGB()))
        return self.current_color

    def getColourHex(self,code):
        return '{:0<2}'.format(str(hex(code))[2:])
    
    def randRGB(self):
        return random.randint(0,255)
    def edge_check(self,*args):
        return True

    def forward(self,current):
        x = current[0]
        y = current[1] + self.getParam('step_y')
        if (y) >= self.getParam('width') or (x,y) in self.visited or not self.edge_check(current):
            return None
        else:
            return (x,y)

    def backward(self,current):
        x = current[0]
        y = current[1] - self.getParam('step_y')
        if (y) < 0 or (x,y) in self.visited or not self.edge_check(current):
            return None
        else:
            return (x,y)

    def left(self,current):
        x = current[0] - self.getParam('step_x')
        y = current[1]
        if (x) < 0 or (x,y) in self.visited or not self.edge_check(current):
            return None
        else:
            return (x,y)

    def right(self,current):
        x = current[0] + self.getParam('step_x')
        y = current[1] 
        if (x) >= self.getParam('width') or (x,y) in self.visited or not self.edge_check(current):
            return None
        else:
            return (x,y)


    def choose(self,choices):
        if len(choices) == 0:
            return None
        return random.choice(choices)
    def getShapeX(self,x):
        return x+self.getParam('x_inc')+random.randint(self.getParam('rand_x_s'),self.getParam('rand_x_e'))
    def getShapeY(self,y):
        return y+self.getParam('y_inc')+random.randint(self.getParam('rand_y_s'),self.getParam('rand_y_e'))

    def getNextPosition(self,current,shape='rectangle'):
        """
        Determines and conforms shape and next position
        Args:
            current: current pointer
            shape: main shape
        """
        available_choices = [func(current) for func in self.methods]
        available_choices = list(filter(lambda x: type(x)!= NoneType,available_choices))
        choice = self.choose(available_choices)
        if choice == None:      #No points available
            return None,None
        else:
            if self.getParam('point_method') == 'true_new':           #True shape as defined in parameters in new position
                choice_end = (self.getShapeX(choice[0]),self.getShapeY(choice[1]))
                return [choice,choice_end],choice           

            elif self.getParam('point_method') == 'ref_x_new':    #Reflective x shape in new position
                choice_end = (self.getShapeX(choice[0]),self.getShapeY(choice[0]))
                return [choice,choice_end],choice   

            elif self.getParam('point_method') == 'ref_x_curr':   #Reflective x shape in current position
                choice_end = (self.getShapeX(choice[0]),self.getShapeY(choice[0]))
                return [current,choice_end],choice_end

            elif self.getParam('point_method') == 'ref_y_new':    #Reflective y shape in new position
                choice_end = (self.getShapeX(choice[1]),self.getShapeY(choice[1]))
                return [choice,choice_end],choice   

            elif self.getParam('point_method') == 'ref_y_curr':   #Reflective y shape in current position
                choice_end = (self.getShapeX(choice[1]),self.getShapeY(choice[1]))
                return [current,choice_end],choice_end

            elif self.getParam('point_method') == 'true_curr': #True shape as defined in parameters in current position with next position as defined
                choice_end = (self.getShapeX(choice[0]),self.getShapeY(choice[1]))
                return [current,choice_end],choice

            else:                                                   #True shape as defined in parameters in current position with next position reconformed
                choice_end = (self.getShapeX(choice[0]),self.getShapeY(choice[1]))                  
                return [current,choice_end],choice_end                  #Default choice

    def close(self):
        self.textFilePointer.close()
    def setInfo(self,param,value):
        self.params[param]=value
    def saveCoordinates(self,coordinates,suffix=0):
        fp = open(self.path+'/coordinates_{}.pkl'.format(suffix),'wb')
        pickle.dump(coordinates,fp)
        fp.close()
    def canvasDraw(self,shape,colour,method='line'):
        self.setInfo('Polygon',method)
        methods = {
            'line': self.canvas.line,
            'rectangle': self.canvas.rectangle,
            'arc': self.canvas.arc,
            'polygon': self.canvas.polygon,
            'ellipse':self.canvas.ellipse
        }
        poly = methods.get(method)
        names = inspect.getfullargspec(poly)
        if method != 'arc':
            
            if self.getParam('fill_method') == 'outline':
                if 'outline' in names[0]:
                    poly(shape,outline=colour)
            else:
                poly(shape,fill=colour)
        else:
            
            if self.getParam('fill_method') == 'outline':
                if 'outline' in names[0]:
                    poly(shape,self.getParam('s_degree'),self.getParam('e_degree'),outline=colour)
            else:
                poly(shape,self.getParam('s_degree'),self.getParam('e_degree'),fill=colour)
    
    def drawPattern(self,length,initial_pointer,colour,canvas=None,method='line',save=False):
        print('Drawing for length:',length)
        current_pointer = initial_pointer
        self.setInfo('Length',length)
        self.setInfo('Origin',initial_pointer)
        self.current_color = colour
        coordinates = []
        for i in range(0,length):
            shape,current_pointer = self.getNextPosition(current_pointer,shape='line')
            if current_pointer == None:
                print('No further positions available, exiting')
                break
            self.canvasDraw(shape,colour,method=method)
            if save == True:
                coordinates.append(shape)
        if save == True:
            self.saveCoordinates(coordinates,str(length) +'_'+ str(initial_pointer))


class Pattern():
    """
    Wrapper class
    """
    def __init__(self,w=1000,h=1000,path='.',params={}):
        """
        Initialise a pattern object with Image size and path
        """
        self.pattern = PatternBase(w,h,path,params)
        self.params = params

    def updateParams(self,params):
        """
        Updates current pattern parameter
        """
        return self.pattern.updateParams(params)

    def saveImage(self,filename,text=True):
        """
        Save pattern as Image to filename in the path defined in params
        Args:
            filename: filename of the image
            text: boolean True or False. Determines if current parameters needs to be saved 
        """
        return self.pattern.saveImage(filename,text)

    def showImage(self):
        """
        Show the pattern so drawn as Image
        """
        return self.pattern.showImage()
    
    def drawPattern(self,length,initial_pointer,colour='#ffffff',shape=None):
        """
        Draws a pattern in canvas
        Args:
            length: no of continuous shapes drawn
            initial_pointer: a tuple in form of (x,y) coordinate
            colour: colour of the shape to be drawn
            shape: shape to be drawn. Default: as set in params
        """
        if shape == None:
            shape = self.pattern.getParam('shape','line')
        return self.pattern.drawPattern(length=length,initial_pointer=initial_pointer,colour=colour,method=shape)
    def drawTemplate(self,templateName,colour='#ffffff',location='Templates'):
        """
        Draws pattern based on template
        Args:
            templateName: Name of existing template
            colour: Optional colour for the pattern
            location: Default Templates folder
        """
        templateObject = patternTemplates.Templates(location=location)
        p = templateObject.getTemplate(templateName)
        self.updateParams(p)
        length = 100
        self.drawPattern(length=p.get('length',length),
        initial_pointer=(random.randint(0,self.pattern.getParam('width')), random.randint(0,self.pattern.getParam('height'))),
        colour=p.get('colour',colour)
        )
    def getRandomInitalPointer(self):
        """
        Generates a random tuple as initial pointer
        """
        initial_pointer=(random.randint(0,self.pattern.getParam('width')), random.randint(0,self.pattern.getParam('height')))
        return initial_pointer
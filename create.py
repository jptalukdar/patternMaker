import patternMaker


params = {}
params['width'] = 1000
params['height'] = 1000
params['x_inc'] = 5   
params['y_inc'] = 5
params['step_x'] = 10  
params['step_y'] = 20

pattern = patternMaker.Pattern(path='save',params=params)
pattern.drawPattern(length=20,initial_pointer=(500,600),colour='#2ec4b6',save=True)
pattern.showImage()
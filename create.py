import patternMaker
import patternTemplates
params = {}
params['width'] = 1000
params['height'] = 1000
params['x_inc'] = 50   
params['y_inc'] = 50
params['step_x'] = 50  
params['step_y'] = 20
params['rand_x_e'] = 10
params['point_method'] = 'true_new'
params['fill_method']= 'outline'
params['shape'] = 'rectangle'
pattern = patternMaker.Pattern(path='save',params=params)
pattern.drawPattern(length=100,initial_pointer=(0,100),colour='#2ec4b6')

params['x_inc'] = 100   
params['y_inc'] = 100
params['shape'] = 'ellipse'
pattern.updateParams(params)
pattern.drawPattern(length=100,initial_pointer=(100,100),colour='#e71d36')

pattern.drawTemplate(templateName='cloud_t1',colour='#ff9f1c')
pattern.showImage()

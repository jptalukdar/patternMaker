# patternMaker

Pattern maker helps you to create patterns and shapes effortlessly. You can get different pattern each time you run.

## Usage

```python
import patternMaker
params = {}
pattern = patternMaker.pattern(path='save',params=params)
pattern.drawPattern(length,initial_pointer,colour='#ffffff',shape=None)
pattern.showImage()
```
params is a dictionary of predefined parameters
parameters can include the following. If params is not passed, it creates pattern based on defaults

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

One can also create patterns based on templates

```python
pattern.drawTemplate(templateName='cloud_t1',colour='#ff9f1c')
```

patterns provided are:
1. cloud_t1
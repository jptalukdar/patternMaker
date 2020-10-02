import yaml
class Templates():
    def __init__(self,location='Templates'):
        self.location=location
    
    def _readTemplate(self,name):
        path= self.location+'/'+name+'.yml'
        with open(path) as stream:
            data = yaml.safe_load(stream)
        return dict(data)

    def getTemplate(self,name):
        data = self._readTemplate(name)
        return data

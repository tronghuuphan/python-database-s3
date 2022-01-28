from configparser import ConfigParser

class BaseConfig:
    def __init__(self, filename, section):
        self.filename = filename
        self.section = section
        self.parser = ConfigParser()
        self.parser.read(self.filename)
    
class DatabaseConfig(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self, filename='config.ini', section='mysql')

    def parse(self):
        db = {}
        if self.parser.has_section(self.section):
            items = self.parser.items(self.section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file.'.format(self.section, self.filename))
        return db
        

class S3Config(BaseConfig):
    def __init__(self):
        BaseConfig.__init__(self, filename='config.ini', section='aws')

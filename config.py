from configparser import ConfigParser

class Config:
    def __init__(self, filename: str, section:str)->None:
        self.filename = filename
        self.section = section
        self.parser = ConfigParser()
        self.parser.read(self.filename)
    
    def parse(self) -> dict:
        arg = {}
        if self.parser.has_section(self.section):
            items = self.parser.items(self.section)
            for item in items:
                arg[item[0]] = item[1]
        else:
            raise Exception('{0} not found in the {1} file.'.format(self.section, self.filename))
        return arg

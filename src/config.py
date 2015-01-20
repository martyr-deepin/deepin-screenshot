import ConfigParser
#from xdg import BaseDirectory
#from os.path import exists
#from os import mkdir

#config_dir = BaseDirectory.xdg_config_home


APPNAME = 'my_python_program'
OPERATE_CONFIG = "%s/%s/%s" % ('/home/ph', APPNAME, 'deepin-screenshot-v3/src/share_service/config.ini')
class WeiboConfig():
    def __init__(self):
        print("weibo")
        return 1
class OperateConfig(object):
    def __init__(self, config_file=OPERATE_CONFIG):
        self.config = ConfigParser.ConfigParser()
        self.config_file = config_file
        self.config.read(config_file)

    def get(self, section, opt=None):
        '''
        get section info
        @param section: the section name
        @param opt: the options name
        @return: the opt value if the opt in the section, else None
        '''
        if not self.config.has_section(section):
            return None
        if opt:
            return self.config.get(section, opt) if self.config.has_option(section, opt) else None
        back = {}
        for option in self.config.options(section):
            back[option] = self.config.get(section, option)
        return back

    def set(self, section, **kw):
        '''
        set section info
        @param section: the section name
        @param kw: some option and value
        '''
        if not self.config.has_section(section):
            self.config.add_section(section)
        for option in kw:
            self.config.set(section, option, kw[option])
        self.config.write(open(self.config_file, 'wb'))

    def __getattr__(self, kw):
        ''' __getattr__'''
        try:
            section, opt = kw.split('_')[0:2]
            return self.get(section, opt)
        except:
            return None

if __name__ == '__main__':
    c = WeiboConfig()
    print c

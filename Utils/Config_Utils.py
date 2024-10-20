# This Utils for test config demo
import os
import configparser
from typing import AnyStr, DefaultDict


class Config_Manager:
    def __init__(self):
        self.conf = configparser.ConfigParser()

    def creat(self, section_list: DefaultDict, ini_file: AnyStr):
        for key, value in section_list.items():
            self.conf[key] = value
        self.save(ini_file)

    def open(self, inifile: AnyStr) -> bool:
        self.ini_file = self.conf.read(inifile)
        if self.ini_file:
            return True
        else:
            return False

    def save(self, ini_file: AnyStr):
        with open(ini_file, 'w') as configfile:
            self.conf.write(configfile)

    def get_section(self):
        sections = self.conf.sections()
        return sections

    def get_section_value(self, section, key):
        value = ''
        try:
            value = self.conf.get(section, key)
        except configparser.NoSectionError as e:
            print(e)
        return value

    def add_section(self, section):
        self.conf.add_section(section)    

    def remove_section(self, section):
        self.conf.remove_section(section)

    def set_section_key_value(self, section, key, value):
        try:
            self.conf.set(section, key, value)
        except configparser.NoSectionError as e:
            print(e)


def test_creat():
    config_dict = {
        "logoninfo": {
            'addr': "zhangsan",
            'passwd': "lisi",
            'popserver': "emain"
        },
        'logging': {
            "level": '2',
            "path": "/root",
            "server": "login",
            'User': 'Atlan'
        }
    }
    cm = Config_Manager()
    cm.creat(config_dict, 'create_test.ini')


def test_open():
    inifile = 'create_test.ini'
    # if inifile in os.listdir('./'):
    #     os.remove(inifile)
    cm = Config_Manager()
    cm.open(inifile)
    s = cm.get_section()
    print(s)
    cm.set_section_key_value('logging', 'testkey', 'testvalue')
    cm.remove_section('xyz')
    res = cm.get_section_value('logging', 'testkey')
    print(res)
    cm.save('create_test.ini')


if __name__ == '__main__':
    test_creat()
    test_open()

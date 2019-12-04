from pylogic.logged_object import LoggedObject
from pylogic.controller import Controller
from pylogic.tagsrv.tagsrv import TagSrv
from pylogic.channel import Channel
from pylogic.saver import FileParameterSaver

import logging


class Factory(LoggedObject):
    def __init__(self):
        super().__init__('Factory')
        self.controller = None
        self.tag_srv = None
        self.top_object = None
        self.saver = None

    def get_controller(self):
        if self.controller is None:
            self.logger.info('Create controller')
            self.controller = Controller()
        return self.controller

    def get_tag_srv(self, tagsrv_config, channels, simulators):
        if self.tag_srv is None:
            self.logger.info('Create tag server')
            self.tag_srv = TagSrv()
            self.tag_srv.init(tagsrv_config, channels, simulators)
        return self.tag_srv

    def get_top_object(self, config):
        if self.top_object is None:
            self.logger.info('Create io objects')
            if len(config) != 1:
                raise Exception('Required 1 root io_object')
            for name, cfg in config.items():
                self.top_object = self.io_object_config_parse(name, cfg, None)
        return self.top_object

    def io_object_config_parse(self, name, config, parent):
        current = config['class'](name, parent)
        current.set_logger(parent.logger if parent is not None else logging.getLogger(name))
        for key, value in config.items():
            if key in ('class', 'children'):
                pass
            elif hasattr(current, key):
                if isinstance(current.__dict__[key], Channel):
                    current.__dict__[key].set_name(value)
                else:
                    current.__dict__[key] = value
        if 'children' in config:
            for child_name, child_cfg in config['children'].items():
                child = self.io_object_config_parse(child_name, child_cfg, current)
                #current.add_child(child)
        return current

    def get_saver(self):
        if self.saver is None:
            self.saver = FileParameterSaver()
            self.saver.set_logger(logging.getLogger('file_saver'))
        return self.saver

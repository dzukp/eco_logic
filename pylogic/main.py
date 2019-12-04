from .logged_object import DEFAULT_LOGGER
from .pyshell.rpcserver import start_shell_server
from .factory import Factory

import logging
import logging.config


def main(config):
    logging.basicConfig()
    app_config = {
        'objects': {},
        'tagsrv_settings': {
            'tags': {},
            'sources': {},
            'dispatchers': {}}
    }
    app_config.update(config)

    if 'logging_conf' in app_config:
        logging.config.dictConfig(app_config['logging_conf'])

    if 'factory' in app_config:
        factory_ = config['factory']
    else:
        factory_ = Factory()

    top_object = factory_.get_top_object(config['objects'])
    tag_srv = factory_.get_tag_srv(config['tagsrv_settings'], top_object.get_all_channels(), {})
    saver = factory_.get_saver()

    controller = factory_.get_controller()
    controller.set_tag_server(tag_srv)
    controller.set_top_object(top_object)
    controller.set_saver(saver)

    if 'pyshell' not in config or config['pyshell']:
        start_shell_server(namespace=locals())

    controller.init()
    controller.start_loop()


if __name__ == '__main__':
    main({})

import yaml

__author__ = 'Conan Dooley'


class Config(object):
    def __init__(self, source, destination, options=None):
        """

        :param source: source config file path
        :type source: str
        :param destination: installed location
        :type source: str
        :param options: optional configuration options
        :type source: dict
        :return:
        """
        super(Config, self).__init__()
        self.source = source
        self.destination = destination
        self.options = {}
        if options is not None:
            self.options = options


class Task(object):
    def __init__(self, name, configs=None, commands=None):
        """
        :param name: name of task
        :type source: str
        :param config: configuration files and associated options
        :type source: list of Config
        :param commands: list of commands to be executed
         :type source: list of str
        :return:
        """
        super(Task, self).__init__()
        self._configs = []
        self._commands = []
        self.name = name
        if configs is not None:
            self.configs = configs
        if commands is not None:
            self.commands = commands

    @property
    def configs(self):
        """
        :return:
        :rtype: Config
        """
        return self._configs

    @configs.setter
    def configs(self, config):
        """

        :param config: configuration parameters
        :type config: Config
        :return:
        """
        self._configs = config

    @property
    def commands(self):
        """

        :return:
        :rtype list
        """
        return self._commands

    @commands.setter
    def commands(self, commands):
        """

        :param commands: command line arguments to execute
        :return: list
        """
        self._commands = commands


class YmlParser(object):
    def __init__(self):
        super(YmlParser, self).__init__()

    def parse(self, config_file):
        """
        :param config_file:
        :return:
        :rtype: list of Task
        """
        config_dict = yaml.load(open(config_file, "r").read())
        """:type config_dict: dict"""
        options = {}
        if 'options' in config_dict:
            options = config_dict['options']
        tasks = []
        for name, task in config_dict.iteritems():
            if name != 'options':
                configs = []
                if 'configs' in task:
                    for config in task['configs']:
                        if 'source' not in config or 'destination' not in config:
                            raise Exception("Invalid Configuration in section %s. 'source' and 'destination' are mandatory." % name)
                        config_options = {}
                        if 'options' in config:
                            config_options = config['options']
                        # This is here to persist the global options if you need to override an option for a single template
                        global_options = options
                        global_options.update(config_options)
                        config_options = global_options
                        configs.append(Config(config['source'], config['destination'], config_options))
                commands = None
                if 'commands' in task:
                    commands = task['commands']
                tasks.append(Task(name, configs, commands))
        return tasks

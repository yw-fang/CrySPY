try:
    import ConfigParser
except ImportError:
    print('ConfigParser has been renamed to configparser')
else:
    import configparser

try:
    print('ConfigParser: ', ConfigParser)
except ImportError:
    pass
else:
    print('configparser: ', configparser)

try:
    config = ConfigParser.ConfigParser()
except ImportError:
    pass
else:
    config = configparser.ConfigParser()

print(config)

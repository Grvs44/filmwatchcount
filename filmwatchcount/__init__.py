from importlib.metadata import version

try:
    VERSION = version('filmwatchcount')
except:
    VERSION = '(dev)'

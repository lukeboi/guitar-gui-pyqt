import importlib
module = importlib.import_module('fbs_runtime._frozen')
module.BUILD_SETTINGS = {'app_name': 'GuitarController', 'author': 'Luke Farritor', 'version': '0.2', 'environment': 'production'}
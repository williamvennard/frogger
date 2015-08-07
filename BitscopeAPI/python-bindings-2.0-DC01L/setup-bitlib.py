import os
from distutils.core import setup, Extension

os.environ['LDFLAGS'] = "-framework bitscope-library"

module = Extension ( 'bitlib', sources = ['bitlibmodule.c'], include_dirs=['/Library/Frameworks/bitscope-library.framework/Versions/A/Headers'] )

setup ( name = "bitlib", version = "2.0", 
        maintainer = "BitScope Designs", maintainer_email = "support@bitscope.com",
        description = "BitScope Library Python Extension module", ext_modules = [module] )
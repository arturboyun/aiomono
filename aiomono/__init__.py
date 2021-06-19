import sys

if sys.version_info < (3, 7):
    raise ImportError(
        'Your Python version {0} is not supported by aiomono, '
        'please install Python 3.7+'.format('.'.join(map(str, sys.version_info[:3])))
    )

from aiomono.client import MonoClient
from aiomono.client import PersonalMonoClient
from aiomono.client import CorporateMonoClient
from aiomono.exceptions import MonoException
from aiomono.exceptions import ToManyRequests

__all__ = (
    'MonoClient',
    'PersonalMonoClient',
    'CorporateMonoClient',

    'MonoException',
    'ToManyRequests',
)

__version__ = '1.1.3'
__api_version__ = '1.0'

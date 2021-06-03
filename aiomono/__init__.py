import sys

if sys.version_info < (3, 7):
    raise ImportError('Your Python version {0} is not supported by aiogram, please install '
                      'Python 3.7+'.format('.'.join(map(str, sys.version_info[:3]))))

from aiomono.client import MonoClient
from aiomono.client import PersonalMonoClient
# from aiomono.client import CorporateMonoClient

__all__ = (
    'MonoClient',
    'PersonalMonoClient',
    # 'CorporateMonoClient',
)

__version__ = '0.1'
__api_version__ = '5.2'

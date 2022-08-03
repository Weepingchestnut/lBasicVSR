import time
import warnings
from getpass import getuser
from socket import gethostname


def get_host_info():
    """Get hostname and username.

    Return empty string if exception raised, e.g. ``getpass.getuser()`` will
    lead to error in docker container
    """
    host = ''
    try:
        host = f'{getuser()}@{gethostname()}'
    except Exception as e:
        warnings.warn(f'Host or user not found: {str(e)}')
    finally:
        return host


def get_time_str():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())

import os
try:
    from offline_guard import install
    install()
except BaseException:
    os._exit(97)

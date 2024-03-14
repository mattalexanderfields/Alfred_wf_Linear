import re
import types

def patched_global_enum(*args, **kwargs):
    return lambda obj: obj

re.enum.global_enum = types.MethodType(patched_global_enum, re.enum)

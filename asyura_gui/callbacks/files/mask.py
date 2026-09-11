from ...callback_runtime import *

def maskclear(env):
    check_vars = env.get('check_vars')
    var = env.get('var')
    for var in check_vars:
        var.set(0)

def maskall(env):
    check_vars = env.get('check_vars')
    var = env.get('var')
    for var in check_vars:
        var.set(1)

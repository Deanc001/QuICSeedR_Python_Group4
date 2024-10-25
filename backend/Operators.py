#No custom operator (%) in python so function def used instead. Function takes x and y checks if x is None, returns y, otherwise it returns x
def null_coal(x,y):
    return y if x is None else x

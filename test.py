import pmodel

def myfunc(**kwargs):
    a = kwargs.get('a')
    b = kwargs.get('b')
    c = kwargs.get('c')
    if len(kwargs) < 1 or kwargs.get('a') == 'None':
        print "Amora"
    if len(kwargs) < 2 or kwargs.get('b') == 'None':
        print "Luna"
    if len(kwargs) < 3:
        print "Amoluna"

# myfunc()

x, y = pmodel(4096, 0.52, -1.66)

myfunc(a=1)

import math
integer = 7
string = "simple string"
c = 42
boolean = True

list_temp = ['one', 2, 'three']
set_temp = set(list_temp)
frozenset_temp = frozenset(list_temp)
tuple_temp = tuple(list_temp)


dict_test = {'first': 1, 'second': 2}


class TestClassA:
    def __init__(self):
        self.el1 = 't'
        self.el2 = 2


class TestClassB:
    pass


class ClassA(TestClassA, TestClassB):
    pass


obj_temp = TestClassA()
GLOBAL_VALUE = 'Hello world'


def simple_func():
    global GLOBAL_VALUE
    return f'Global value is {GLOBAL_VALUE}'


def arguments_func(arg1: int, arg2: int, arg3: int):
    s = arg1 + arg2 + arg3
    return s


def butoma_func(x: int):
    a = 123
    return math.sin(a*x*c)

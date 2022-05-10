import inspect
from types import CodeType, FunctionType

primitives = (int, str, bool, float)


class Converter:

    func_found = {}

    @staticmethod
    def convert(obj) -> object:
        if isinstance(obj, primitives):
            return obj
        elif inspect.isfunction(obj):
            return Converter.convert_function(obj)
        elif inspect.iscode(obj):
            return Converter.convert_code(obj)
        elif inspect.isclass(obj):
            return Converter.convert_class(obj)
        elif inspect.ismodule(obj):
            return Converter.convert_module(obj)
        else:
            return obj

    @staticmethod
    def convert_globals(obj, obj_code):
        Converter.func_found[obj.__name__] = True
        gls = {}
        for i in obj_code.co_names:
            try:
                if inspect.isclass(obj.__globals__[i]):
                    gls[i] = Converter.convert_class(obj.__globals__[i])
                elif inspect.isfunction(obj.__globals__[i]):
                    if obj.__globals__[i].__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_function(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], staticmethod):
                    if obj.__globals__[i].__func__.__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_static_method(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], classmethod):
                    if obj.__globals__[i].__func__.__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_class_method(obj.__globals__[i])
                elif inspect.ismodule(obj.__globals__[i]):
                    gls[i] = Converter.convert_module(obj.__globals__[i])
                elif Converter.is_instance(obj.__globals__[i]):
                    gls[i] = Converter.convert_object(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], (set, dict, list, int, float, bool, type(None), tuple, str)):
                    gls[i] = obj.__globals__[i]
            except KeyError:
                pass
        for i in obj_code.co_consts:
            if isinstance(i, CodeType):
                gls.update(Converter.collect_globals(obj, i))
        return gls

    @staticmethod
    def convert_class(cls):
        bases = ()
        if len(cls.__bases__) != 0:
            for i in cls.__bases__:
                if i.__name__ != "object":
                    bases += (Converter.convert_class(i),)
        args = {}
        st_args = dict(cls.__dict__)
        if len(st_args) != 0:
            for i in st_args:
                if inspect.isclass(st_args[i]):
                    args[i] = Converter.convert_class(st_args[i])
                elif inspect.isfunction(st_args[i]):
                    if st_args[i].__name__ not in Converter.func_found:
                        args[i] = Converter.convert_function(st_args[i])
                elif isinstance(st_args[i], staticmethod):
                    if st_args[i].__func__.__name__ not in Converter.func_found:
                        args[i] = Converter.convert_static_method(st_args[i])
                elif isinstance(st_args[i], classmethod):
                    if st_args[i].__func__.__name__ not in Converter.func_found:
                        args[i] = Converter.convert_class_method(st_args[i])
                elif inspect.ismodule(st_args[i]):
                    args[i] = Converter.convert_module(st_args[i])
                elif Converter.is_instance(st_args[i]):
                    args[i] = Converter.convert_object(st_args[i])
                elif isinstance(st_args[i],
                                (set, dict, list, int, float, type(True), type(False), type(None), tuple)):
                    args[i] = st_args[i]
        return {"##class_type##": {"name": cls.__name__, "bases": bases, "dict": args}}

    @staticmethod
    def convert_object(obj):
        return {"##instance_type##": {"class": Converter.convert_class(obj.__class__), "vars": obj.__dict__}}

    @staticmethod
    def convert_module(obj):
        return {"##module_type##": obj.__name__}

    @staticmethod
    def collect_globals(obj, obj_code):
        Converter.func_found[obj.__name__] = True
        gls = {}
        for i in obj_code.co_names:
            try:
                if inspect.isclass(obj.__globals__[i]):
                    gls[i] = Converter.convert_class(obj.__globals__[i])
                elif inspect.isfunction(obj.__globals__[i]):
                    if obj.__globals__[i].__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_function(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], staticmethod):
                    if obj.__globals__[i].__func__.__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_static_method(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], classmethod):
                    if obj.__globals__[i].__func__.__name__ not in Converter.func_found:
                        gls[i] = Converter.convert_class_method(obj.__globals__[i])
                elif inspect.ismodule(obj.__globals__[i]):
                    gls[i] = Converter.convert_module(obj.__globals__[i])
                elif Converter.is_instance(obj.__globals__[i]):
                    gls[i] = Converter.convert_object(obj.__globals__[i])
                elif isinstance(obj.__globals__[i], (set, dict, list, int, float, bool, type(None), tuple, str)):
                    gls[i] = obj.__globals__[i]
            except KeyError:
                pass
        for i in obj_code.co_consts:
            if isinstance(i, CodeType):
                gls.update(Converter.collect_globals(obj, i))
        return gls

    @staticmethod
    def convert_static_method(obj):
        return {"##static_method_type##": Converter.convert_function(obj.__func__)}

    @staticmethod
    def convert_class_method(obj):
        return {"##class_method_type##": Converter.convert_function(obj.__func__)}

    @staticmethod
    def convert_function(obj):
        gls = Converter.collect_globals(obj, obj.__code__)

        return {"##function_type##": {"__globals__": gls,
                                      "__name__": obj.__name__,
                                      "__code__":
                                          Converter.convert_code(obj.__code__)
                                      }}

    @staticmethod
    def convert_code(obj):
        return {"##code_type##":
            {
                "co_argcount": obj.co_argcount,
                "co_posonlyargcount": obj.co_posonlyargcount,
                "co_kwonlyargcount": obj.co_kwonlyargcount,
                "co_nlocals": obj.co_nlocals,
                "co_stacksize": obj.co_stacksize,
                "co_flags": obj.co_flags,
                "co_code": Converter.convert_byte_array(obj.co_code),
                "co_consts": obj.co_consts,
                "co_names": obj.co_names,
                "co_varnames": obj.co_varnames,
                "co_filename": obj.co_filename,
                "co_name": obj.co_name,
                "co_firstlineno": obj.co_firstlineno,
                "co_lnotab": Converter.convert_byte_array(obj.co_lnotab),
                "co_freevars": obj.co_freevars,
                "co_cellvars": obj.co_cellvars
            }
        }

    @staticmethod
    def convert_byte_array(obj):
        array = [byte for byte in obj]
        s = "[ "
        for el in array:
            s += str(el) + " ,"
        s = s[:-1]
        s += " ]"
        return s

    @staticmethod
    def is_instance(obj):
        if not hasattr(obj, '__dict__'):
            return False
        if inspect.isroutine(obj):
            return False
        if inspect.isclass(obj):
            return False
        else:
            return True

    @staticmethod
    def load(obj):
        if type(obj) is dict:
            for key, value in obj.items():
                if key == "##function_type##":
                    return Converter.load_func(value)
                elif key == "##code_type##":
                    return Converter.load_code(value)
                elif key == "##module_type##":
                    return Converter.load_module(value)
                elif key == "##static_method_type##":
                    return staticmethod(Converter.load_func(value))
                elif key == "##class_method_type##":
                    return classmethod(Converter.load_func(value))
                elif key == "##instance_type##":
                    return Converter.load_obj(value)
        return obj

    @staticmethod
    def load_code(obj: dict) -> CodeType:
        obj = obj["##code_type##"]
        return CodeType(obj["co_argcount"],
                        obj["co_posonlyargcount"],
                        obj["co_kwonlyargcount"],
                        obj["co_nlocals"],
                        obj["co_stacksize"],
                        obj["co_flags"],
                        bytes(bytearray(Converter.load_bytearray(obj["co_code"]))),
                        tuple(obj["co_consts"]),
                        tuple(obj["co_names"]),
                        tuple(obj["co_varnames"]),
                        obj["co_filename"],
                        obj["co_name"],
                        obj["co_firstlineno"],
                        bytes(bytearray(Converter.load_bytearray(obj["co_code"]))),
                        tuple(obj["co_freevars"]),
                        tuple(obj["co_cellvars"]))

    @staticmethod
    def load_func(obj):
        res = FunctionType(globals=Converter.load_globals(obj["__globals__"]),
                           code=Converter.load_code(obj["__code__"]),
                           name=obj['__name__'])
        funcs = Converter.collect_funcs(res, {})
        funcs.update({res.__name__: res})
        Converter.set_funcs(res, {res.__name__: True}, funcs)
        res.__globals__.update(funcs)
        res.__globals__['__builtins__'] = __import__('builtins')
        return res

    @staticmethod
    def load_class(cls):
        try:
            return type(cls["name"], tuple(cls["bases"]), cls["dict"])
        except IndexError:
            raise StopIteration("Incorrect class")

    @staticmethod
    def load_obj(obj):
        try:
            def __init__(self):
                pass
            cls = obj["class"]
            temp = cls.__init__
            cls.__init__ = __init__
            res = obj["class"]()
            res.__dict__ = obj["vars"]
            res.__init__ = temp
            res.__class__.__init__ = temp
            return res
        except IndexError:
            raise StopIteration("Incorrect object")

    @staticmethod
    def load_module(module: str):
        try:
            return __import__(module)
        except ModuleNotFoundError:
            raise ImportError(str(module) + ' not found')

    @staticmethod
    def set_funcs(obj, is_visited, gls):
        for i in obj.__globals__:
            attr = obj.__globals__[i]
            if inspect.isfunction(attr) and attr.__name__ not in is_visited:
                is_visited[attr.__name__] = True
                attr.__globals__.update(gls)
                is_visited = Converter.set_funcs(attr, is_visited, gls)
        return is_visited

    @staticmethod
    def collect_funcs(obj, is_visited):
        for i in obj.__globals__:
            attr = obj.__globals__[i]
            if inspect.isfunction(attr) and attr.__name__ not in is_visited:
                is_visited[attr.__name__] = attr
                is_visited = Converter.collect_funcs(attr, is_visited)
        return is_visited

    @staticmethod
    def load_bytearray(s: str):
        array = bytearray()
        s = s.replace("[", "")
        s = s.replace("]", "")
        s = s.replace(" ", "")
        a = s.split(",")
        for el in a:
            array.append(int(el))
        return array

    @staticmethod
    def load_globals(g: dict):
        globs = dict()
        for key, value in g.items():
            globs[key] = Converter.load(value)
        return globs

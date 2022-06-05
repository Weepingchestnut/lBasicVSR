"""
    (1) 最简实现
"""
# # 方便起见，此处并未使用类方式构建，而是直接采用全局变量
# _module_dict = dict()
#
#
# # 定义装饰器函数
# def register_module(name):
#     def _register(cls):
#         _module_dict[name] = cls
#         return cls
#
#     return _register
#
#
# # 装饰器用法
# @register_module('one_class')
# class OneTest(object):
#     pass
#
#
# @register_module('two_class')
# class TwoTest(object):
#     pass


"""
    (2) 实现无需传入参数，自动根据类名初始化类
"""

_module_dict = dict()


def register_module(module_name=None):
    def _register(cls):
        name = module_name
        # 如果 module_name 没有给，则自动获取
        if module_name is None:
            name = cls.__name__
        _module_dict[name] = cls
        return cls

    return _register


@register_module('one_class')
class OneTest(object):
    pass


@register_module()
class TwoTest(object):
    pass


if __name__ == '__main__':
    # 通过注册类名实现自动实例化功能
    # one_test = _module_dict['one_class']()
    # print(one_test)

    one_test = _module_dict['one_class']
    # 方便起见，此处仅仅打印了类对象，而没有实例化。如果要实例化，只需要 one_test() 即可
    print(one_test)
    two_test = _module_dict['TwoTest']
    print(two_test)

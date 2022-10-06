# -*- coding: utf-8 -*-
import re


def register_params_check(content):
    """
    TODO: 进行参数检查
    """

    try:
        if not re.match("[a-zA-Z]+\d+$", content["username"]):  # 检测username
            return "username", False
        if len(content['username']) not in range(5, 13):
            return "username", False

        if not re.match("[\w\-_*^]+$", content['password']):  # 检测password
            return "password", False
        if len(content['password']) not in range(8, 16):
            return "password", False

        content['nickname']  # 检测nickname

        protocol, domain_name = content['url'].split('//')  # 检测url
        if protocol not in ['https:', 'http:']:
            return "url", False
        if len(domain_name) > 48:
            return "url", False
        labels = domain_name.split('.')
        if len(labels) <= 1:
            return "url", False
        if re.match("\d+$", labels[-1]):
            return "url", False
        for label in labels:
            if not re.match("[\w-]+$", label):
                return "url", False
            if re.match("(-.*)|(.*-)$", label):
                return "url", False

        if not re.match("\+\d\d\.\d{12}$", content['mobile']):  # 检测mobile
            return "mobile", False

        if 'magic_number' not in content:  # 检测magic_number
            content['magic_number'] = 0
        else:
            if not isinstance(content['magic_number'], int):
                return "magic_number", False
            if content['magic_number'] < 0:
                return "magic_number", False
    except KeyError as e:
        return str(e)[1:-1], False  # 专门用来处理字段缺失情况。
    except ValueError:
        return "url", False
    except TypeError:
        return 'username', False
    return "ok", True

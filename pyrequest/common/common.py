# -*- coding:utf-8 -*-
import os,sys
BASE_PATH = os.path.split(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))[0]
sys.path.append(BASE_PATH)

"""
   根据key值遍历获取dict中对应的value值
   :param search_dict: Dict类型，传入需要的响应结果
   :param key_name: Str类型，传入Key值
   :return: 返回Value值，根据对应的类型进行返回（字符串类型、Dict类型、列表类型等）
"""
def get_value_byKey(search_dict, key_name):
    search_value = ""
    for key, value in search_dict.items():
        if key == key_name:
            search_value = value
        elif isinstance(value, dict):
            results = get_value_byKey(value, key_name)
            for result in results:
                search_value = result
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    more_results = get_value_byKey(item, key_name)
                    for another_result in more_results:
                        search_value = another_result
    return search_value
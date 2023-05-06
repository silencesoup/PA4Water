"""
Author: Wenyu Ouyang
Date: 2023-05-06 10:37:28
LastEditTime: 2023-05-06 10:56:51
LastEditors: Wenyu Ouyang
Description: 
FilePath: \PA4Water\toolbox.py
Copyright (c) 2023-2024 Wenyu Ouyang. All rights reserved.
"""
from functools import lru_cache
import importlib
import os
import re

def is_openai_api_key(key):
    API_MATCH_ORIGINAL = re.match(r"sk-[a-zA-Z0-9]{48}$", key)
    API_MATCH_AZURE = re.match(r"[a-zA-Z0-9]{32}$", key)
    return bool(API_MATCH_ORIGINAL) or bool(API_MATCH_AZURE)

def read_env_variable(arg, default_value):
    """
    环境变量可以是 `PA_CONFIG`(优先)，也可以直接是`CONFIG`
    例如在windows cmd中，既可以写：
        set USE_PROXY=True
        set API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    也可以写：
        set PA_USE_PROXY=True
        set PA_API_KEY=sk-j7caBpkRoxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        set PA_proxies={"http":"http://127.0.0.1:10085", "https":"http://127.0.0.1:10085",}
        set PA_AVAIL_LLM_MODELS=["gpt-3.5-turbo", "chatglm"]
        set PA_AUTHENTICATION=[("username", "password"), ("username2", "password2")]
    """
    arg_with_prefix = f"PA_{arg}"
    if arg_with_prefix in os.environ: 
        env_arg = os.environ[arg_with_prefix]
    elif arg in os.environ: 
        env_arg = os.environ[arg]
    else:
        raise KeyError
    print(f"[ENV_VAR] 尝试加载{arg}，默认值：{default_value} --> 修正值：{env_arg}")
    try:
        if isinstance(default_value, bool):
            r = bool(env_arg)
        elif isinstance(default_value, int):
            r = int(env_arg)
        elif isinstance(default_value, float):
            r = float(env_arg)
        elif isinstance(default_value, str):
            r = env_arg.strip()
        elif isinstance(default_value, dict):
            r = eval(env_arg)
        elif isinstance(default_value, list):
            r = eval(env_arg)
        elif default_value is None:
            assert arg == "proxies"
            r = eval(env_arg)
        else:
            print(f"[ENV_VAR] 环境变量{arg}不支持通过环境变量设置! ")
            raise KeyError
    except:
        print(f"[ENV_VAR] 环境变量{arg}加载失败! ")
        raise KeyError(f"[ENV_VAR] 环境变量{arg}加载失败! ")

    print(f"[ENV_VAR] 成功读取环境变量{arg}")
    return r

@lru_cache(maxsize=128)
def read_single_conf_with_lru_cache(arg):
    try:
        # 优先级1. 获取环境变量作为配置
        default_ref = getattr(importlib.import_module('config'), arg)   # 读取默认值作为数据类型转换的参考
        r = read_env_variable(arg, default_ref)
    except Exception:
        try:
            # 优先级2. 获取config_private中的配置
            r = getattr(importlib.import_module('config_private'), arg)
        except Exception:
            # 优先级3. 获取config中的配置
            r = getattr(importlib.import_module('config'), arg)

    # 在读取API_KEY时，检查一下是不是忘了改config
    if arg == 'API_KEY':
        print("[API_KEY] 本项目现已支持OpenAI的api-key")
        if is_openai_api_key(r):
            print(f"[API_KEY] 您的 API_KEY 是: {r[:15]}*** API_KEY 导入成功")
        else:
            print( "[API_KEY] 正确的 API_KEY 是'sk'开头的51位密钥（OpenAI），或者 'fk'开头的41位密钥，请在config文件中修改API密钥之后再运行。")
    return r


def get_conf(*args):
    # 建议您复制一个config_private.py放自己的秘密, 如API和代理网址, 避免不小心传github被别人看到
    res = []
    for arg in args:
        r = read_single_conf_with_lru_cache(arg)
        res.append(r)
    return res

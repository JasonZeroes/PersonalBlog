# 创建一个函数, 实现对ajax请求的返回响应
def json_msg(code, msg=None, data=None):
    return {"code": code, "errmsg": msg, "data": data}

from django.test import TestCase

# Create your tests here.
import hashlib
print( dir(hashlib) )

a=b'123456'  # 原文&明文

obj = hashlib.sha1(a)
obj2 = hashlib.md5(a)  # 将明文以字节码（字符串）形式加到对象中
obj3 = hashlib.sha256(a)
obj4 = hashlib.sha512(a)
obj5 = hashlib.sha384(a)

print( obj.hexdigest() )  # 加密输出
print( obj2.hexdigest() )
print( obj3.hexdigest() )
print( obj4.hexdigest() )
print( obj5.hexdigest() )

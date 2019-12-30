from syldb.core import SerializedInterface
from syldb.core.field import Field

# 数据表对象
class Table(SerializedInterface):
    def __init__(self,**options):
        self._field_names = []  # 数据表的所有字段名
        self._field_objs = {}  #数据表字段名与字段对象映射
        self._rows = 0  # 数据条目数

        # 获取所有字段名和字段对象为数据表初始化字段
        for field_name,field_obj in options.items():
            # 进行字段添加
            self.add_field(field_name,field_obj)

    # 添加新字段
    def add_field(self,field_name,field_obj,value=None):

        # 如果新添加的字段名已存在，抛出字段已经在异常
        if field_name in self._field_names:
            raise Exception('Field Exists')
        #如果field_obj不为Field对象，抛出类型错误异常
        if not isinstance(field_obj,Field):
            raise TypeError('type error, value must be %s' %Field)

        # 添加字段名
        self._field_names.append(field_name)

        #绑定字段名与字段
        self._field_objs[field_name] = field_obj

        #如果已存在其它字段，同步该新增字段的数据长度与原先字段数据长度等长，反之初始化数据长度为第一个字段的数据长度
        if len(self._field_names)>1:

            #获取已存在字段的长度
            length = self._rows

            # 获取该字段新增字段的长度
            field_obj_length = field_obj.length()
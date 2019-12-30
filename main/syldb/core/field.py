from syldb.core import  FieldKey, FieldType, TYPE_MAP

from main.syldb.core import SerializedInterface

# 数据字段类
class Field(SerializedInterface):
    def __init__(self, data_type, keys=FieldKey.NULL, default=None):
        self._Type = data_type   # 字段的数据类型
        self._keys = keys        # 字段的数据约束
        self._default = default   #默认值
        self._values = []       #字段数据
        self._rows = 0          #字段数据长度
        # 要求字段类型在定义类型中
        if not isinstance(self._Type, FieldType):
            raise TypeError('data-Type require type of "FieldType"')
        # 如果约束只有一个，并且非 list 类型，则转换为 list (为什么非要list？)
        if  not isinstance(self._keys, keys):
            self._keys = [self._keys]
        # 要求约束在定义类型中
        for key in self._keys:
            if not isinstance(key, FieldKey):
                raise TypeError('data-key require type of "FieldKey"')

        if FieldKey.INCREMENT in self._keys:
            if self._Type !=FieldType.INT:
                raise TypeError("Increment key require Data-type is integer")
            if FieldKey.PRIMARY not in self._keys:
                raise Exception("Increment key require primary key")

    def _check_type(self,value):
        # 如果该值不符合定义好的类型，配出类型错误异常
        if value is not None and not isinstance(value, self._type.value):
            raise TypeError('data type error, value must be %s' %self._type)

    def _check_index(self,index):
        # 如果指定位置不存在，抛出不存在该元素异常
        if not isinstance(index, int) or not -index < self._rows >index:
            raise Exception('Not this element')
        return True

    # 键值约束
    def _check_keys(self,value):
        # 如果字段包含自增键，则选择合适的值自动自增
        if FieldType.INCREMENT in self._keys:
            # 如果值为空，则用字段数据长度作为基值自增
            if value is None:
                value = self._rows + 1

            if value in self._values:
                raise Exception('value %s exists' % value)
        # 如果字段包含主键约束或者唯一约束，判断值是否存在
        if FieldKey.PRIMARY in self._keys or FieldKey.UNIQUE in self._keys:
            # 如果值存在，抛出存在异常
            if value in self._values:
                raise Exception('value % exists' % value)

        #如果该字段包含主键或者非空键，并且添加的值为空值，则抛出值不能为空异常
        if(FieldKey.INCREMENT in self._keys or FieldKey.NOT_NULL in self._keys) and value is None:
            raise Exception('Field Not null')

        return True

    #获取有多少条数据
    def length(self):
        return self._rows

    #获取数据
    def get_data(self,index=NOne):
        # 如果index参数为整型，则返回指定位置数据，反之返回所有数据
        if index is not None and self._check_index(index):
            return self._values[index]

        # 返回所有数据
        return self._values

    # 添加数据
    def add(self,value):
        # 如果插入数据为空，则赋值为默认值
        if value is None:
            value = self._default

        #判断数据是否符合约束要求
        value = self._check_keys(value)

        # 检查插入数据得类型是否符合
        self._check_type(value)

        #追加数据
        self._values.append(value)

        self._rows += 1

    # 删除指定位置数据
    def delete(self,index):

        # 如果删除的位置不存在，抛出不存在该元素异常
        self._check_index(index)

        self._values.pop(index)

        self._rows -= 1

    # 修改指定位置数据

    def modify(self,index,value):

        # 如果修改的位置小于0或者大于数据总长度,抛出不存在该元素异常
        self._check_index(index)

        # 判断数据是否符合约束要求
        value = self._check_keys(value)

        # 如果修改的值类型不符合定义好的类型,抛出类型错误异常

        self._check_type(value)

        # 修改shuju
        self._values[index] = value

    # 获取字段数据约束
    def get_keys(self):
        return self._keys
    # 获取字段类型
    def get_type(self):
        return self._Type
    # 获取数据长度
    def length(self):
        return self._rows

    # 序列化对象
    def serialized(self):
        return SerializedInterface.json.dumps({
            'key':[key.value for key in self._keys],
            'type':self._type.value,
            'values':self._values,
            'default':self._default
        })
    # 反序列化对象
    @staticmethod
    def deserialized(data):
        # 将数据转化为Json对象
        json_data = SerializedInterface.json.loads(data)

        # 转换Json对象中key的值为枚举类 FieldKey 中的属性
        keys = [FieldKey(key) for key in json_data['key']]

        # 传入解析出来的数据类型和字段健并实例化一个Field对象
        obj = Field(FieldType(json_data['type']),keys,default=json_data['default'])

        #为Field对象绑定数据
        for value in json_data['value']:
            obj.add(value)

        #
        返回该Field对象
        return obj
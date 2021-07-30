import xmltocd
from xmltocd import TextType
xml_data = """
    <root>
        <a name="name_a">I am A.</a>
        <b name="name_b">
            <c name="name_c"  flag="1">I am C.</c>
            <c name="name_$c" flag="1">I am CC.</c>
            <c>666</c>
            <c>hello</c>
            <c>
                <d name="d">world</d>
                123
                <e name="e"></e>
            </c>
        </b>
    </root>
"""
# xmlManager = xmltocd.parse('output.xml')
xmlManager = xmltocd.parse_string(xml_data)
xml = xmlManager.xml # 获取整个XML对象

# 输出查看整个结构
# import json
# print(json.dumps(xml, indent=4))

# 取根节点
root = xml.root

# 取属性值
print(root.a.name) # name_a
print(root.a['name']) # name_a

# 取文本
print(root.a.text_) # I am A.
print(root.a['text_']) # I am A.
print(root.b.c[0].text_) # I am C.
print(root.b.c[3].text_) # hello
xmlManager.add_attrs(root.b.c[3], flag="123456")
print(root.b.c[-1].d.text_) # world
print(root.b.c[-1].text_) # 123
print(xmlManager.find_text(root.b.c[-2])) # hello
'''
text_type可选值：TextType.STR、TextType.FLOAT、TextType.INT。默认 STR 类型。
'''
print(xmlManager.find_text_by_attrs(text_type=TextType.STR, name="d")) # world

# 更新属性/文本值
root['a'].age = 12 # 不可取，必须使用本工具提供的方法新增节点，否则程序不会认为 age 是属性值（因为保存操作有反转数据操作）
xmlManager.register_attr(root['a'], 'age', 12) # 如果一定要用上面的新增属性方式，则必须注册，以让程序了解到属性地更新（后期考虑自动感知）
root['a'].age = 12
xmlManager.register_attr(root['a'], 'age', 12) # 无效注册，仅需手动注册一次
# 建议使用如下方式新增属性
xmlManager.add_attrs(root['a'], ('age', 12))
xmlManager.add_attrs(root['a'], ('age', 14)) # 重复添加，仅第一个有效
node_a = xmlManager.find_node_by_attrs(name="name_a")
xmlManager.update_attr(node_a, 'age', 45)
xmlManager.batch_update_attrs(node_a, ('age', 100), age=123) # 接收位置参数和关键字参数，重复时后者覆盖前者
xmlManager.update_text(node_a, 'I am A2.') # 默认存在，若是新增节点请使用 first = True
xmlManager.update_text(root.b.c[4].e, 'I am e.')
print(node_a) # ChainDict([('name', 'name_a'), ('text_', 'I am A2.'), ('age', 123)])


# 推荐使用下面的方式创建并插入一个 f 节点
xmlManager.insert(root.b.c[4].e, tag='f', attrs={'name': "name_f"}, text='I am f.')


### 通过属性获取节点对象
# 取唯一的节点（必须只有一个，否则报 MoreNodesFound 和 NotNodeFound 异常）
name_c = xmlManager.find_node_by_attrs(name='name_$c', flag="1")
print(name_c.text_) # I am CC.
# 取满足条件的多个节点，当节点一个也不存在时报 NotNodeFound 异常
cs = xmlManager.find_nodes_by_attrs(flag="1")
print(cs) # [ChainDict([('name', 'name_c'), ('flag', '1'), ('text_', 'I am C.')]), ChainDict([('name', 'name_$c'), ('flag', '1'), ('text_', 'I am CC.')])]
# 取满足条件的且为指定索引位置的几个节点，如果索引不存在，则返回空迭代器
c = xmlManager.find_nodes_by_indexs([0, 18, 3], flag="1") # 取第一个
print(list(c)) # [ChainDict([('name', 'name_c'), ('flag', '1'), ('text_', 'I am C.')])]
print(xmlManager.find_node_by_attrs(name='name_c').text_)

objs = xmlManager.find_nodes_by_tag_and_attrs(tag="c", name='name_$c')
print(objs)

# 删除
obj = xmlManager.pop_node_by_attrs(name="e")
print(obj)


# 保存修改
xmlManager.save('output.xml')

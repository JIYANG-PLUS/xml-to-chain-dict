依赖安装：pip install -r requirements.txt
安装本工具：pip install xmltocd

在线教程链接（tutorial）：http://101.34.219.31:8001/
教程参考正在逐步整理中，更多高级用法，请阅读源码获取。

### 举个简单的例子
```python
import xmltocd
import json

s = """\
<root id='root'>
    78946546
    <a id="a1">123</a>
    <a>1234</a>
    <a>1235</a>
    <b name='bb'>
        <c id='c1' okk='yiu'>okk</c>
        <d json='{"x": 888}' e='eee'>{"x": 666}
            <e>789789789</e>
        </d>
    </b>
    <e2></e2>
    6789
</root>
"""

'''读
'''
xmlManager = xmltocd.parse_string(s, real_cdata_key='string')

'''输出原始字典和ChainDict字典
'''
# print(json.dumps(xmlManager.objects.doc, indent=4))
# print(json.dumps(xmlManager.xml, indent=4))

'''通过标签查找
'''
print(xmlManager.find_nodes_by_tag('e2', one_=True).string) # one_ 用于限制结果集有且只有一个节点返回

'''通过子孙节点确定唯一的目标节点
'''
node = xmlManager.find_nodes_with_descendants(
    constraint={
        'args': []
        ,'kwargs': {'tag': "e"}
    }
    , tag='d'
    , one_=True
)
print(node.json) # 输出：{"x": 888}

```
事实上它的功能远比上面这个例子要强大的多。
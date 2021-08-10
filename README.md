教程链接（tutorial）：http://101.34.219.31:8001/

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

xmlManager = xmltocd.parse_string(s, real_cdata_key='string')

# print(json.dumps(xmlManager.objects.doc, indent=4))
# print(json.dumps(xmlManager.xml, indent=4))

print(xmlManager.find_nodes_by_tag('e2', one_=True).string)

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
事实上它的功能远比下面这个例子强大的多
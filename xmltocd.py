from collections import OrderedDict
from typing import Any, List, OrderedDict as Type_OrderedDict
from functools import reduce

try:
    import xmltodict
except:
    raise ImportError('Unable to import xmltodict, please pip install xmltodict.')

''' 2021-07-23 ~ '''
__author__ = 'jiyang'
__version__ = '0.0.1'
__license__ = 'MIT'

ATTR_PREFIX = '@'
CDATA_KEY = '#text'
REAL_CDATA_KEY = 'text_'

class DocTypeError(Exception): ...
class KeywordAttrsError(Exception): ...
class MoreNodesFound(Exception): ...
class NotNodeFound(Exception): ...
class TextNotFound(Exception): ...
class UpdateError(Exception): ...
class AddNodeError(Exception): ...

class TextType:
    STR = 0
    INT = 1
    FLOAT = 2
    DECIMAL = 3


class ChainDict(OrderedDict):

    def __init__(self):
        super(ChainDict, self).__init__()

    def __getattr__(self, name):
        if not name.startswith('_'):
            return self[name]
        return super(ChainDict, self).__getattr__(name)

    def __setattr__(self, name, value):
        if not name.startswith('_'):
            self[name] = value
        else:
            super(ChainDict, self).__setattr__(name, value)


class ChainXML:

    xml = None

    def __init__(self
                 , doc: Type_OrderedDict
                 , attr_prefix: str = ATTR_PREFIX # default attribute prefix
                 , cdata_key: str = CDATA_KEY # default original text-flag
                 , real_cdata_key = REAL_CDATA_KEY # obj's default text-flag
                 ) -> None:

        if not isinstance(doc, OrderedDict) or 1 != len(doc):
            raise DocTypeError('`doc` type error.')

        self.doc = doc
        self.attr_prefix = attr_prefix
        self.cdata_key = cdata_key
        self.real_cdata_key = real_cdata_key

        self._attr_searcher = {}
        '''self._reverse_attr_name
            {
                ("name", "#name"): node,
                ...
            }
        '''
        self._reverse_attr_name = {}
        '''self._attr_searcher:

            {
                'name="ok"': {
                    'count': 0,
                    'nodes': [

                    ]
                }
            }
        '''
        self._reverse_text_node = []
        self.xml = self._build_chain_by_recursion(self.doc)

    
    def _build_chain_by_BFS(self, doc_obj: Type_OrderedDict) -> dict:
        '''generate chained struct by BFS. (future)
        '''

    def _build_chain_by_DFS(self, doc_obj: Type_OrderedDict) -> dict:
        '''generate chained struct by DFS. (future)
        '''

    def _build_chain_by_recursion(self, doc_obj: Any) -> dict:
        '''generate chained struct by recursion.
        '''
        if not isinstance(doc_obj, dict):
            if isinstance(doc_obj, (list, tuple, )): # safely change to BFS. (future)
                temp_list = []
                for line in doc_obj:
                    temp_list.append(self._build_chain_by_recursion(line))
                return temp_list
            if doc_obj is None:
                return ChainDict() # None is not allowed
            return doc_obj

        temp_xml = ChainDict()
        
        for k, v in doc_obj.items():
            _attr_name_new_old = None
            _text_ = False
            if self.attr_prefix == k[0]: # attribute
                _attr_name_new_old = (k[1:], k)
                k = k[1:]
            if self.cdata_key == k: # text
                k = self.real_cdata_key
                _text_ = True
            temp_xml[k] = self._build_chain_by_recursion(v)

            if _attr_name_new_old is not None:
                if _attr_name_new_old not in self._reverse_attr_name:
                    self._reverse_attr_name[_attr_name_new_old] = [temp_xml] # deal with attr specially(due to save).
                else:
                    self._reverse_attr_name[_attr_name_new_old].append(temp_xml)

            if _text_:
                self._reverse_text_node.append(temp_xml)
            
            if isinstance(temp_xml[k], str):
                # if self.real_cdata_key not in temp_xml:
                #     t_d = ChainDict()
                #     t_d[self.real_cdata_key] = temp_xml[k]
                #     temp_xml[k] = t_d

                search_key = f'{k}={temp_xml[k]}'
                if search_key in self._attr_searcher:
                    self._attr_searcher[search_key]['nodes'].append(temp_xml)
                    self._attr_searcher[search_key]['count'] += 1
                else:
                    self._attr_searcher[search_key] = {
                        'count': 1,
                        'nodes': [temp_xml, ]
                    }

        return temp_xml

class ChainManager:

    def __init__(self, xml_data: str, *args, **kwargs) -> None:

        self.attr_prefix = kwargs['attr_prefix'] if 'attr_prefix' in kwargs else ATTR_PREFIX
        self.cdata_key = kwargs['cdata_key'] if 'cdata_key' in kwargs else CDATA_KEY
        self.real_cdata_key = kwargs['real_cdata_key'] if 'real_cdata_key' in kwargs else REAL_CDATA_KEY
        
        self.chainXML = ChainXML(
            xmltodict.parse(xml_data, attr_prefix=self.attr_prefix, cdata_key=self.cdata_key)
            , attr_prefix = self.attr_prefix
            , cdata_key = self.cdata_key
            , real_cdata_key = self.real_cdata_key
        )
        self.xml = self.chainXML.xml
        self._attr_searcher = self.chainXML._attr_searcher
        self._searcher_keys = list(self._attr_searcher.keys())

        # add operations must update `_reverse_attr_name` and `_reverse_text_node`
        self._reverse_attr_name = self.chainXML._reverse_attr_name
        self._reverse_text_node = self.chainXML._reverse_text_node

    @classmethod
    def new_node(self):
        return ChainDict()

    def _intersection(self, obj1, obj2):
        result = []
        for _1 in obj1:
            for _2 in obj2:
                if _1 == _2:
                    result.append(_1)
                    break
        return result
    
    def find_node_by_attrs(self, *args, **kwargs) -> ChainDict:

        if len(kwargs) < 1:
            raise KeywordAttrsError('Keyword parameters must be passed in.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in self._searcher_keys:
            if sk in conditions:
                match_cons.append(sk)

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            raise NotNodeFound('Not found.')
        elif 1 == len_match_cons:
            obj = self._attr_searcher[match_cons[0]]
            if obj['count'] > 1:
                raise MoreNodesFound('Match to more than one result.')
            else:
                return obj['nodes'][0]
        else:
            objs = list(reduce(self._intersection, [self._attr_searcher[t]['nodes'] for t in match_cons]))
            if 0 == len(objs):
                raise NotNodeFound('Not found.')
            elif 1 == len(objs):
                return objs[0]
            else:
                raise MoreNodesFound('Match to more than one result.')

    def find_nodes_by_attrs(self, *args, **kwargs) -> List[ChainDict]:

        if len(kwargs) < 1:
            raise KeywordAttrsError('Keyword parameters must be passed in.')

        conditions = set([f'{k}={v}' for k, v in kwargs.items()])
        match_cons = []
        for sk in self._searcher_keys:
            if sk in conditions:
                match_cons.append(sk)

        len_match_cons = len(match_cons)
        if 0 == len_match_cons:
            raise NotNodeFound('Not found.')
        elif 1 == len_match_cons:
            obj = self._attr_searcher[match_cons[0]]
            if obj['count'] > 1:
                return obj['nodes']
            else:
                return obj['nodes'][0]
        else:
            objs = list(reduce(self._intersection, [self._attr_searcher[t]['nodes'] for t in match_cons]))
            if 0 == len(objs):
                raise NotNodeFound('Not found.')
            elif 1 == len(objs):
                return objs[0]
            else:
                return objs


    def find_nodes_by_indexs(self, indexs: List[int], *args, **kwargs) -> ChainDict:
        nodes = self.find_nodes_by_attrs(*args, **kwargs)
        len_nodes = len(nodes)
        for index in indexs:
            if 0 <= index < len_nodes:
                yield nodes[index]


    def find_text(self, node):
        
        if self.real_cdata_key in node:
            return node[self.real_cdata_key]
        elif isinstance(node, str):
            return node
        else:
            raise TextNotFound('Text not found.')


    def find_node_by_tag(self):
        '''(future)
        '''

    def find_text_by_attrs(self, *args, text_type: int=TextType.STR, **kwargs) -> str:
        node = self.find_node_by_attrs(*args, **kwargs)
        text = self.find_text(node)
        if TextType.STR == text_type:
            return str(text)
        elif TextType.FLOAT == text_type:
            return float(text)
        elif TextType.INT == text_type:
            return int(text)
        else:
            return text
        
    def insert(self, obj, tag, attrs={}, text=''):
        if isinstance(obj, ChainDict):
            new_node = ChainDict()
            self.add_attrs(new_node, **attrs)
            self.update_text(new_node, text, first=True)
            insert_node = ChainDict()
            insert_node[tag] = new_node
            obj.update(insert_node)
        else:
            raise AddNodeError('Add node error, obj must be `ChainDict` type.')

    def delete(self, obj: ChainDict) -> ChainDict:
        '''(future)
        '''
        return obj

    def _register_attr(self, node, attr_name):
        temp_key = (attr_name, f'{self.attr_prefix}{attr_name}')
        if temp_key in self._reverse_attr_name:
            if node not in self._reverse_attr_name[temp_key]:
                self._reverse_attr_name[temp_key].append(node)
        else:
            self._reverse_attr_name[temp_key] = [node]

    def _register_text(self, node):
        self._reverse_text_node.append(node)

    def add_attrs(self, node, *args, **kwargs):
        for attr_name, value in args+tuple(kwargs.items()):
            if attr_name not in node:
                node[attr_name] = value
                self._register_attr(node, attr_name)

    def update_attr(self, obj: ChainDict, attr_name: str, new_value: Any):
        if obj is None:
            obj = ChainDict()
        if attr_name in obj:
            obj[attr_name] = new_value
        else:
            raise UpdateError('Unable to update this node, check whether the attribute exists.')

    def batch_update_attrs(self, obj, *args, **kwargs):
        if len(args) < 1 and len(kwargs) < 1:
            raise KeywordAttrsError('Parameters or keyword parameters must be passed in.')
        for attr_name, value in args+tuple(kwargs.items()):
            self.update_attr(obj, attr_name, value)
        

    def update_text(self, obj: ChainDict, new_text: Any, first=False):
        if obj is not None and self.real_cdata_key in obj:
            obj[self.real_cdata_key] = new_text
        else:
            if obj is None:
                raise UpdateError('Unable to update this node, None is found.')
            if first:
                obj[self.real_cdata_key] = new_text
                self._register_text(obj)
            else:
                raise UpdateError('Unable to update this node, check whether text exists.')

    def __reverse_data(self):
        for no, objs in self._reverse_attr_name.items():
            new_name, old_name = no
            for obj in objs:
                obj[old_name] = obj[new_name]
                del obj[new_name]

        for node in self._reverse_text_node:
            node[self.cdata_key] = node[self.real_cdata_key]
            del node[self.real_cdata_key]

    def __revert_data(self):
        for no, objs in self._reverse_attr_name.items():
            new_name, old_name = no
            for obj in objs:
                obj[new_name] = obj[old_name]
                del obj[old_name]

        for node in self._reverse_text_node:
            node[self.real_cdata_key] = node[self.cdata_key]
            del node[self.cdata_key]


    def save(self, path: str = 'output.xml') -> None:
        self.__reverse_data()
        with open(path, 'w', encoding='utf-8') as fp:
            xmltodict.unparse(self.xml, fp)
        self.__revert_data()

if __name__ == '__main__':
    ...

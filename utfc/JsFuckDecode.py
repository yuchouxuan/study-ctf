# 该工具能够通解六字符和八字符的 jsfuck 混肴
# 主要的函数为 unjsfuck

import re
import urllib.parse

# 这里使用了几个中文字符作为重要的分割器
# 所以解析的代码里面解出来一定不要包含这几个中文字符
_plus_sign_rep = '￥'  # +
_single_quotes_rep = '‘'  # '
uleft, uright = '【', '】'  # []
pleft, pright = '（', '）'  # ()


def cuter(string, force=True):
    # 正确的分割算数单元，结果返回一个列表
    # eg.  '+!+[]+[0]+[][[]]+![true]+!+[]+!+[false]'
    #  => ['+!+[]', '+', '[0]', '+', '[][[]]', '+', '![true]', '+', '!+[]', '+', '!+[false]']
    def combine(p):
        # 合并相连的中括号， [?] 将拼接的列表连接在一起。因为是一个计算单元
        # eg. []      [[]]  => [][[]]
        # eg. 'asdf'  [3]   => 'asdf'[3]
        pr = None
        ci = 0
        cb = {}
        for cr in sorted(p):
            if pr:
                if pr[1] == cr[0]:
                    if ci not in cb: cb[ci] = []
                    if pr not in cb[ci]: cb[ci].append(pr)
                    if cr not in cb[ci]: cb[ci].append(cr)
                else:
                    ci += 1
                    if ci not in cb: cb[ci] = []
                    if cr not in cb[ci]: cb[ci].append(cr)
            else:
                if ci not in cb: cb[ci] = []
                if cr not in cb[ci]: cb[ci].append(cr)
            pr = cr
        d = {}
        for pi in sorted(cb):
            v = cb[pi]
            l, r = v[0][0], v[-1][1]
            d[(l, r)] = ''.join([p[i] for i in v])
        return d

    list_left, list_right = '[]'
    tupl_left, tupl_right = '()'
    dict_left, dict_right = '{}'
    s = string
    p = {}
    l, r = 0, 0
    _list = 0
    _name = 1
    _int = 2
    _str = 3
    _tuple = 4
    _dict = 5

    def find(string, r):
        '''
        在查找时，同时获取下一个结构的类型，虽然jsfuck只用很少的字符
        不过在层层解析的过程中，还是会生成其他类型的数据，所以需要考虑到这类型的数据分割
        并且在一定情况下，原始的脚本就是混合 jsfuck 的。一开始就有其他类型的数据，所以还是需要考虑。
        _list , _int , _str, _name, _tuple, _dict
        '''
        _ints = list(map(str, range(10)))
        te = re.findall(r"[a-zA-Z0-9$_\[\(\{']", s[r:])
        if te:
            if te[0] == list_left:
                ft = _list
            elif te[0] == tupl_left:
                ft = _tuple
            elif te[0] == dict_left:
                ft = _dict
            elif te[0] == "'":
                ft = _str
            elif te[0] in _ints:
                ft = _int
            else:
                ft = _name
            return string.find(te[0], r), ft
        else:
            return -1, None

    q, ft = find(s, 0)
    t = True
    while t:
        c = []
        if q == -1: break
        for idx, i in enumerate(s[q:]):
            if ft == _list:
                if i == list_left:  c.append(list_left)
                if i == list_right: c.pop()
                if len(c) == 0:
                    l, r = q, q + idx + 1
                    p[(l, r)] = s[l:r]
                    q, ft = find(s, r)
                    break
            elif ft == _tuple:
                if i == tupl_left:  c.append(tupl_left)
                if i == tupl_right: c.pop()
                if len(c) == 0:
                    l, r = q, q + idx + 1
                    p[(l, r)] = s[l:r]
                    q, ft = find(s, r)
                    break
            elif ft == _dict:
                if i == dict_left:  c.append(dict_left)
                if i == dict_right: c.pop()
                if len(c) == 0:
                    l, r = q, q + idx + 1
                    p[(l, r)] = s[l:r]
                    q, ft = find(s, r)
                    break
            else:
                if ft == _name:
                    v = re.findall(r'[a-zA-Z0-9$_]+', s[r:])[0]
                elif ft == _int:
                    v = re.findall(r'[0-9]+', s[r:])[0]
                elif ft == _str:
                    v = re.findall(r"'[^']*'", s[r:])[0]
                l, r = q, q + len(v)
                p[(l, r)] = s[l:r]
                q, ft = find(s, r)
                break
        if len(c) > 0: t = False
    s = string
    d = combine(p)
    k = sorted(d)
    ll, rr = 0, len(s) + 1
    if k:
        q = [ll]
        for l, r in k:
            q.append(l);
            q.append(r)
        q.append(rr)
        e = {}
        w = {}
        pr = ''
        for i in range(len(q) - 1):
            k, v = (q[i], q[i + 1]), s[q[i]:q[i + 1]]
            if i % 2 == 0:
                # c = re.findall(r'\+!+\+$|\+$', v)
                c = re.findall(r'\+((?:!+\+)?)$', v)
                c.extend(re.findall(r'\+((?:!+)?)$', v))
                pr = c[0] if c else ''
                e[k] = v[:len(v) - len(pr)]
            if i % 2 == 1:
                w[k] = pr + v
        e.update(w)
        k = sorted(e)
        r = [e[i] for i in k]
        if len(r) >= 2 and (r[0].endswith('+') or r[0].endswith('!') or not r[0]):
            r = [r[0] + r[1]] + [i for i in r[2:] if i]
        return r
    else:
        # import traceback; traceback.print_exc()
        print('error:', string)
        return ['[{}]'.format(string)]


def safe_pack(string):
    v = string.replace("'", _single_quotes_rep)
    v = v.replace('+', _plus_sign_rep)
    v = repr(v).replace('\\\\', '\\')
    return v


def safe_unpack(string):
    v = re.sub(r"'[^']+'", lambda g: "{}".format(g.group(0).replace('\\', '\\\\')), string)
    v = v.replace(_single_quotes_rep, "\\'")
    v = v.replace(_plus_sign_rep, '+')
    return v


def allplus(ls):
    '''
    通过将列表内的表达式进行比较初级的元映射后，进行运算变换
    这里的运算变换会考虑到不同类型的 js 隐式转换，虽然不一定能完全覆盖
    但是从原运算的角度来考虑的话，会更加贴近真实的解析状态
    原始函数经过切分函数后生成切分单元列表，然后再经过本函数后即可处理元映射计算处理
    eg. jsfk_str = '+!+[]+[0]+[][[]]+![true]+!+[]+!+[false]+!+[123]+!+[undefined]+[123123]+['asdfasdf']'
        ls =    cuter(jsfk_str)
        ls ==   ['+!+[]', '+', '[0]', '+', '[][[]]', '+', '![true]', '+', '!+[]', '+', '!+[false]', '+', '!+[123]', '+', '!+[undefined]', '+', '[123123]', '+', "['asdfasdf']"]
        allplus(jsfk_str) == '10undefinedfalsetruetruefalsetrue123123asdfasdf'
    '''
    _unfind = -1
    _int = 0
    _str = 1
    _undefined = 2
    _boolen = 3
    _null = 4
    _NaN = 5
    _list = 6
    _dict = 7
    _func = 8
    q = [
        ["NaN", "NaN", _NaN],
        ["false", "false", _boolen],
        ["true", "true", _boolen],
        ["undefined", "undefined", _undefined],
        ["[]", "[]", _list],
        ["[][[]]", "undefined", _undefined],
        ["[]['']", "undefined", _undefined],
        ["['']", "[]", _list],
    ]
    e = [
        [r'^\+(!*)\[\]$', "_bint_", _int],  # 下面几个注释中的映射关系的通解
        [r'^\+(!+)\+\[\]$', "_binti_", _int],  # 下面几个注释中的映射关系的通解
        [r'^(!+)\[\]$', "_bool_", _boolen],  # 下面几个注释中的映射关系的通解
        [r'^(!+)\+\[\]$', "_booli_", _boolen],  # 下面几个注释中的映射关系的通解
        # ["+![]",                      "0",        _int],
        # ["+!![]",                     "1",        _int],
        # ["+[]",                       "0",        _int],
        # ["+!+[]",                     "1",        _int],
        # ["+!!+[]",                    "0",        _int],
        # ["!+[]",                      "true",     _boolen],
        # ["!!+[]",                     "false",    _boolen],
        # ["![]",                       "false",    _boolen],
        # ["!![]",                      "true",     _boolen],
        # [r'^\{(\d+)\}$',              None,       _int],      # 这种情况不会出现，这里写明是为区分
        # [r"^\{'[^']'\}$",             None,       _str],      # 这种情况不会出现，这里写明是为区分
        [r"^\{\}$", None, _dict],  # 常用的 dict 类型
        [r"^\{NaN\}$", None, _dict],
        [r"^\{undefined\}$", None, _dict],
        [r"^\+\{\}$", "NaN", _NaN],  # 后续几条{}相关的、 以 !或+ 符号开始的只能在计算块的起始才能存在
        [r"^\+\{NaN\}$", "NaN", _NaN],
        [r"^\+\{undefined\}$", "NaN", _NaN],
        [r"^(!+)\{[^{]*\}$", "_bool_", _boolen],
        [r"^(!+)\+\{[^{]*\}$", "_booli_", _boolen],
        [r"^\+(!+)\{[^{]*\}$", "_bint_", _int],
        [r"^\+(!+)\+\{[^{]*\}$", "_binti_", _int],
        [r'^\+?(\d+)$', None, _int],
        [r"^\+'(\d+)'$", None, _int],
        [r"^'(\d+)'$", None, _str],
        [r"^\+?(\d+)e(\d+)$", "_sint", _int],  # 科学计数法，我TM惊呆了
        [r"^\+?'(\d+)e(\d+)'$", "_sint", _int],  # py与js自动变化的位数不同，py:16, js:21
        [r"^\+'(\.\d+)'$", "_sfloat", _int],  # 这里需要负指数的科学计数法
        [r"^'([^']*)'$", None, _str],
        [r"^'([^']*)'\[(\d+)\]$", "_eval_", _str],
        [r"^'([^']*)'\['(\d+)'\]$", "_evalr_", _str],
        [r"^\['([^']+)'\]$", None, _str],
        [r'^\[([^\[\]]*)\]$', None, _list],
        [r"^\+?\d+\['([^'\[\]]+)'\]$", "_numfunc", _func],  # typeobj[?]
        [r"^\+?'[^']*'\['([^']+)'\]$", "_strfunc", _func],  # eg. []["filter"]
        [r"^\+?\[\]\['([^'\[\]]+)'\]$", "_arrfunc", _func],
        [r"^\+?true\['([^'\[\]]+)'\]$", "_boofunc", _func],
        [r"^\+?false\['([^'\[\]]+)'\]$", "_boofunc", _func],
        [r"^\[\]\[[^'\[\]]+\]$", "undefined", _undefined],
        # 这里考虑放弃对方法字符串的判断 [1][2] 这种结构中的 2 部分将不接受字符串匹配
        # 因为这里可能会获取到函数，我这里的功能不包括实现 js 内部函数块
        [r'^!\[.+\]$', "false", _boolen],
        [r'^!(\d+)$', "_int_", _boolen],
        [r'^\+\[null\]$', "0", _int],
        [r'^\+\[undefined\]$', "0", _int],
        [r'^\+\[(\d+)\]$', None, _int],
        [r'^\+\[true\]$', "NaN", _NaN],
        [r'^\+\[false\]$', "NaN", _NaN],
        [r'^\+\[NaN\]$', "NaN", _NaN],
        [r"^\+\['([^']+)'\]$", "NaN", _NaN],
        [r"^!\+\['([^']+)'\]$", "true", _boolen],
        [r'^!\+\[(\d+)\]$', "_int_", _boolen],
        [r'^!\+\[\w+\]$', "true", _boolen],
        [r"^(\d+)\['toString'\]\('?(\d+)'?\)\[('?\d+'?)\]$", "_base_n", _str],  # 101['toString'](21)[1]
        [r"^(\d+)\['toString'\]\('?(\d+)'?\)$", "_base_n2", _str],
        [r"^'([^']*)'\['italics'\]\(\)\[('?\d+'?)\]$", "_itafunc", _str],  # 'false0'['italics']()['10']
        [r"^'([^']*)'\['fontcolor'\]\(\)\[('?\d+'?)\]$", "_fontfunc", _str],  # ''['fontcolor']()['12']
        [r"^\['([^']*)'\]\['concat'\]\('([^']*)'\)$", "_concat", _str],
        [r"^\+?\d+\['([^'\[\]]+)'\]\['([^'\[\]]+)'\]$", "_numfunc2", _func],  # []['filter']['constructor']
        [r"^\+?'[^']*'\['([^']+)'\]\['([^'\[\]]+)'\]$", "_strfunc2", _func],
        [r"^\+?\[\]\['([^'\[\]]+)'\]\['([^'\[\]]+)'\]$", "_arrfunc2", _func],
        [r"^\+?true\['([^'\[\]]+)'\]\['([^'\[\]]+)'\]$", "_boofunc2", _func],
        [r"^\+?false\['([^'\[\]]+)'\]\['([^'\[\]]+)'\]$", "_boofunc2", _func],
        # 下面这些应该是目前为止最TM硬的硬编码了
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return escape'\)\(\)\('(.)'\)\['?(\d+)'?\]$", '_escape', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return unescape'\)\(\)\('([^']+)'\)$", '_unescape', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return/0/'\)\(\)\['constructor'\]$", '_regexp', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return/0/'\)\(\)\['constructor'\]\(\)$", '_regexp2', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return new Date\(200000000\)'\)\(\)$", '_date', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return new Date\(24000000000\)'\)\(\)$", '_date2', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return Date'\)\(\)\(\)$", '_date3', _str],
        # []['filter']['constructor']('return Date')()()
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return this'\)\(\)$", '_window', _str],
        [r"^\[\]\['[a-zA-Z0-9]+'\]\['constructor'\]\('return location'\)\(\)$", '_http', _str],
    ]
    arrf = [
        "concat", "copyWithin", "entries", "every", "fill",
        "filter", "find", "findIndex", "forEach", "from",
        "includes", "indexOf", "isArray", "join", "keys",
        "lastIndexOf", "map", "pop", "push", "reduce",
        "reduceRight", "reverse", "shift", "slice", "some",
        "sort", "splice", "toString", "unshift", "valueOf",
    ]
    srtf = [
        "anchor", "big", "blink", "bold", "charAt",
        "charCodeAt", "concat", "fixed", "fontcolor", "fontsize",
        "fromCharCode", "indexOf", "italics", "lastIndexOf", "link",
        "localeCompare", "match", "replace", "search", "slice",
        "small", "split", "strike", "sub", "substr",
        "substring", "sup", "toString", "valueOf", "toLowerCase",
        "toUpperCase", "toSource", "toLocaleLowerCase", "toLocaleUpperCase",
    ]
    numf = [
        "toString", "toLocaleString", "toFixed", "toExponential", "toPrecision",
        "valueOf",
    ]
    boof = [
        "toSource", "toString", "valueOf"
    ]
    funf = [
        "prototype", "apply", "arguments", "bind", "call",
        "toString", "hasOwnProperty", "isPrototypeOf", "valueOf",
        "propertyIsEnumerable", "toLocaleString",
    ]

    def _get_func(v, obj):
        val = v[0]
        if obj == 'arr':
            if val in arrf:
                return "function " + val + "() { [native code] }"
            elif val == 'constructor':
                return "function Array() { [native code] }"
        if obj == 'str':
            if val in srtf:
                return "function " + val + "() { [native code] }"
            elif val == 'constructor':
                return "function String() { [native code] }"
        if obj == 'num':
            if val in numf:
                return "function " + val + "() { [native code] }"
            elif val == 'constructor':
                return "function Number() { [native code] }"
        if obj == 'boo':
            if val in boof:
                return "function " + val + "() { [native code] }"
            elif val == 'constructor':
                return "function Boolean() { [native code] }"

    def _get_func2(v, obj):
        # 解析 [1][2][3] 这种结构时，结构2一定会存在，否则会变成 undefined[3] 直接报错
        val, val2 = v[0]

        def raise_err(type, tval, val, val2):
            raise TypeError('{} error. {}["{}"]["{}"]'.format(type, tval, val, val2))

        if obj == 'arr':
            tval = '[]'
            if val not in arrf: raise_err('undefined', tval, val, val2)
        if obj == 'str':
            tval = '""'
            if val not in srtf: raise_err('undefined', tval, val, val2)
        if obj == 'num':
            tval = '123'
            if val not in numf: raise_err('undefined', tval, val, val2)
        if obj == 'boo':
            tval = 'true'
            if val not in boof: raise_err('undefined', tval, val, val2)
        if val2 in funf:
            return "function " + val + "() { [native code] }"
        elif val2 == 'constructor':
            return "function Function() { [native code] }"
        else:
            raise_err('unknow', tval, val, val2)

    def get_fit(s):
        if isinstance(s, (list, tuple)):
            return s
        for i in q:
            i.copy()
            if s == i[0]:
                return i
        for i in e:
            i = i.copy()
            v = re.findall(i[0], s)
            if v:
                def base_n(s, n, i=0):
                    m = '0123456789abcdefghijklmnopqrstuvwxyz'
                    q = []
                    e = True
                    while e:
                        e = s // n
                        y = s % n
                        s = e
                        q.append(m[y])
                    v = q[::-1][i]
                    return v

                def _parse_get_func(func, type, i, v):
                    f2string = func(v, type)
                    if f2string:
                        if not s.startswith('+'):
                            i[1] = f2string
                        else:
                            i[1], i[2] = 'NaN', _NaN
                    else:
                        i[1], i[2] = 'undefined', _undefined

                if i[1] is None:
                    i[1] = v[0]
                elif i[1] == '_int_':
                    i[1] = 'false' if int(v[0]) else 'true'
                elif i[1] == '_eval_':
                    s, idx = v[0];
                    i[1], i[2] = (s[int(idx)], i[2]) if len(s) > int(idx) else ("undefined", _undefined)
                elif i[1] == '_evalr_':
                    s, idx = v[0];
                    i[1], i[2] = (s[int(idx)], i[2]) if len(s) > int(idx) else ("undefined", _undefined)
                elif i[1] == '_bint_':
                    i[1] = '0' if v[0].count('!') % 2 == 1 or v[0].count('!') == 0 else '1'
                elif i[1] == '_binti_':
                    i[1] = '1' if v[0].count('!') % 2 == 1 else '0'
                elif i[1] == '_bool_':
                    i[1] = 'false' if v[0].count('!') % 2 == 1 else 'true'
                elif i[1] == '_booli_':
                    i[1] = 'true' if v[0].count('!') % 2 == 1 else 'false'
                elif i[1] == '_sfloat':
                    i[1] = str(float(v[0]))
                elif i[1] == '_sint':
                    v = str(eval('{}e{}'.format(*v[0])));
                    i[1] = v if v != 'inf' else "Infinity"
                elif i[1] == '_strfunc':
                    _parse_get_func(_get_func, 'str', i, v)
                elif i[1] == '_arrfunc':
                    _parse_get_func(_get_func, 'arr', i, v)
                elif i[1] == '_numfunc':
                    _parse_get_func(_get_func, 'num', i, v)
                elif i[1] == '_boofunc':
                    _parse_get_func(_get_func, 'boo', i, v)
                elif i[1] == '_strfunc2':
                    _parse_get_func(_get_func2, 'str', i, v)
                elif i[1] == '_arrfunc2':
                    _parse_get_func(_get_func2, 'arr', i, v)
                elif i[1] == '_numfunc2':
                    _parse_get_func(_get_func2, 'num', i, v)
                elif i[1] == '_boofunc2':
                    _parse_get_func(_get_func2, 'boo', i, v)
                elif i[1] == '_itafunc':
                    i[1] = "<i>{}</i>".format(v[0][0])[int(v[0][1].strip("'"))]
                elif i[1] == '_fontfunc':
                    i[1] = '<font color="undefined">{}</font>'.format(v[0][0])[int(v[0][1].strip("'"))]
                elif i[1] == '_concat':
                    i[1] = ','.join(v[0])
                elif i[1] == '_base_n':
                    i[1] = base_n(*map(int, v[0]))
                elif i[1] == '_base_n2':
                    i[1] = base_n(*map(int, v[0]))
                elif i[1] == '_escape':
                    i[1] = urllib.parse.quote(v[0][0].encode())[int(v[0][1])]
                elif i[1] == '_unescape':
                    i[1] = urllib.parse.unquote(v[0])
                elif i[1] == '_regexp':
                    i[1] = "function RegExp() { [native code] }"
                elif i[1] == '_regexp2':
                    i[1] = "/(?:)/"
                elif i[1] == '_date':
                    i[1] = "Sat Jan 03 1970 15:33:20 GMT+0800"
                elif i[1] == '_date2':
                    i[1] = "Tue Oct 06 1970 02:40:00 GMT+0800"
                elif i[1] == '_date3':
                    i[1] = "Sat Jan 03 1970 15:33:20 GMT+0800"
                elif i[1] == '_window':
                    i[1] = "[object Window]"
                elif i[1] == '_http':
                    i[1] = "http://vvvv.vvv"  # 在某些情况下这里的字符串只会被取走第4个字母 p
                return i
        return ['', s, _unfind]

    def parse_type(xv, xt, tp):
        if tp == _NaN:
            return 'NaN'
        if tp == _int:
            if xt != _int:
                if xt == _dict:     return '0'
                if xv == 'true':    return '1'
                if xv == 'false':   return '0'
                if xv == 'null':    return '0'
            else:
                return xv
        if tp == _str:
            if xt != _str:
                if xv == '[]':
                    return ''
                else:
                    return xv
            else:
                return xv
        if tp == _unfind:
            return xv

    def _plus(a, b):
        '''
        这里还需要增加一些无法计算类型的处理
        比如一些变量名字的计算暂时不需要考虑，过早的加入那个会使得问题复杂化。
        k:key
        v:value
        t:targettype
        '''
        ak, av, at = a
        bk, bv, bt = b
        types = [at, bt]
        if _dict in types:
            if at == _dict and bt == _dict:
                av = bv = "[object Object]"
                rt = _str
            elif at == _dict:
                if bt == _NaN or bt == _undefined or bt == _func:
                    rt = _NaN
                else:
                    rt = _int
            elif bt == _dict:
                bv = "[object Object]"
                rt = _str
            else:
                rt = _str
        elif _list in types or _str in types or _func in types:
            rt = _str
        elif _NaN in types or _undefined in types:
            rt = _NaN
        elif _int in types:
            if types.count(_int) == 2:
                rt = _int
            elif _boolen in types or _null in types:
                rt = _int
        elif _boolen in types:
            if types.count(_boolen) == 2:
                rt = _int
            elif _null in types:
                rt = _int
        elif _null in types:
            if types.count(_boolen) == 2:
                rt = _int
        else:
            rt = _unfind
        _a = parse_type(av, at, rt)
        _b = parse_type(bv, bt, rt)
        if rt == _NaN: val = 'NaN'
        if rt == _str: val = _a + _b
        if rt == _int: val = int(_a) + int(_b)
        if rt == _unfind: val = _a + '+' + _b
        return None, str(val), rt

    l = [i for idx, i in enumerate(ls[::-1]) if idx % 2 == 0]
    t = True
    p = []
    if len(l) < 2:
        v = get_fit(l.pop())
        if v[2] == _str:
            return safe_pack(v[1])
        v = parse_type(v[1], v[2], _str)
        if v:
            return v
        else:
            return repr(v)
    while t and len(l):
        p.append(l.pop())
        if len(p) == 2:
            left = get_fit(p[0])
            right = get_fit(p[1])
            p = [_plus(left, right)]
    return safe_pack(p[0][1]) if p[0][2] == _str else p[0][1]


def unjsfuck(s, dlevel=10, debuglevel=0):
    '''
    应对常规的jsfuck应该是没有问题
    暂时还没有解决 ''['length'] 的问题，不过实际上 jsfuck 本身生成就已经很重了
    一般也很少用复杂函数混肴生成比原本还要更加大几倍的超大字符串，会影响性能。
    '''
    unique, unit = uleft + uright, '[]'
    _unique, _unit = pleft + pright, '()'
    x = r'(^|\+|\[|\(|\)|\]|%s|%s|%s|%s)' % (uright, pright, uleft, pleft)
    expa = x + r'(\([^\(\)\[\]]+\))' + x  # 找到计算块
    expb = r'\[[^\(\)\[\]]+\]'
    expc = r"'[^']*'"
    elef = erit = r"([\)|\]|{}|{}|\(|\[|{}|{}])".format(uright, pright, uleft, pleft)
    expd = elef + r"\(('[^']*')\)"  # + erit
    expf = r"\[([a-zA-Z0-9$_']+)\]"
    expe = r"\(([a-zA-Z0-9$_']+)\)"

    def _repa(string):
        return string.replace('[', uleft).replace(']', uright).replace('(', pleft).replace(')', pright)

    def _repb(string):
        return string.replace(uleft, '[').replace(uright, ']').replace(pleft, '(').replace(pright, ')')

    def _repc(string):
        if debuglevel >= 2:
            print('  == prcut:', _repb(string[1:-1]))
            print('  -- cuter:', cuter(_repb(string[1:-1])))
        return allplus(cuter(_repb(string[1:-1])))

    def parse_idxstr(string):
        '''
        将解析差不多干净的字符串下标单字部分清理成单个字符串
        并且将所有连接在一起的部分进行合并
        '''
        a = r"(^|\+)'([^']*)'\[(\d+)\]"
        b = r"(^|\+)'([^']*)'\['(\d+)'\]"
        c = r"([^\)\]])'([^']*)'\[(\d+)\]($|\+)"
        d = r"([^\)\]])'([^']*)'\['(\d+)'\]($|\+)"
        x = r"(?:(?:^|\+)?'[^'\[\]\(\)\+]+')+([^\[])"

        def _inindex(g, left=True):
            s = g.group(2)
            i = int(g.group(3))
            if i > len(s):
                r = 'undefined'
            else:
                r = s[i]
            return g.group(1) + repr(r) if left else g.group(1) + repr(r) + g.group(4)

        _inindex_left = lambda g: _inindex(g)
        _inindex_right = lambda g: _inindex(g, left=False)

        def _combine_single(g):
            v = g.group(0)
            t = v[-1]
            if t != '+': v = v[:-1]
            r = "'{}'".format(v.replace('+', '').replace("'", '').replace('+', ''))
            if v.startswith('+'): r = '+' + r
            if v.endswith('+'):   r = r + '+'
            if t != '+': r = r + t
            return r

        v = re.sub(a, _inindex, string)
        v = re.sub(b, _inindex, v)
        v = re.sub(c, _inindex_right, v)
        v = re.sub(d, _inindex_right, v)
        v = re.sub(x, _combine_single, v)
        return v

    v = '[{}]'.format(s.replace(' ', '').replace('"', "'"))
    if debuglevel >= 1:
        print('======= start =======')
        print('[ level: {} ] {}'.format(0, v))

    def e(g):
        return _repa(g.group(0))  # 规避函数

    def h(g):
        return uleft + g.group(1) + uright  # 规避函数

    def i(g):
        return pleft + g.group(1) + pright  # 规避函数

    def j(g):
        return g.group(1) + pleft + g.group(2) + pright  # + g.group(3)

    def n(g):
        return '[{}]'.format(_repc(g.group(0)))  # 处理抽取中括号中的计算体

    def m(g):
        l, c, r = _repb(g.group(1)), _repc(g.group(2)), _repb(g.group(3))
        return (l + '({})'.format(c) + r) if l in (')', ']', uright, pright, _unit) or r in ('(', pleft) else (
                l + c + r)

    for _ in range(dlevel):
        v = v.replace(unit, unique).replace(_unit, _unique)
        v = re.sub(expc, e, v)  # 规避字符串内的中小括号
        v = re.sub(expf, h, v)
        v = re.sub(expe, i, v)
        v = re.sub(expd, j, v)
        v = re.sub(expa, m, v)  # 从小括号中的内容获取解析式，并计算
        v = _repb(v)
        v = v.replace(unit, unique).replace(_unit, _unique)
        v = re.sub(expc, e, v)
        v = re.sub(expf, h, v)
        v = re.sub(expe, i, v)
        v = re.sub(expd, j, v)
        v = re.sub(expb, n, v)  # 从中括号中的内容获取解析式，并计算
        v = _repb(v)
        v = parse_idxstr(v)
        if v != s:
            s = v
        else:
            break
        if debuglevel >= 1:
            print('[ level: {} ] {}'.format(_ + 1, safe_unpack(v[1:-1])))

    v = safe_unpack(v)[1:-1]
    return v

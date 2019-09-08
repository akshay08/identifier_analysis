import ast
import sys
import tokenize

def _read(filename):
    if (2, 5) < sys.version_info < (3, 0):
        with open(filename, 'rU') as f:
            return f.read()
    elif (3, 0) <= sys.version_info < (4, 0):
        """Read the source code."""
        try:
            with open(filename, 'rb') as f:
                (encoding, _) = tokenize.detect_encoding(f.readline)
        except (LookupError, SyntaxError, UnicodeError):
            # Fall back if file encoding is improperly declared
            with open(filename, encoding='latin-1') as f:
                return f.read()
        with open(filename, 'r', encoding=encoding) as f:
            return f.read()

code = _read(sys.argv[1])
tree = compile(code, sys.argv[1], "exec", ast.PyCF_ONLY_AST)

linewise_contents = dict()
with open(sys.argv[1], 'r') as f:
    for lineno, linecode in enumerate(f):
        linewise_contents[lineno+1] = linecode

root = ast.parse(code)

defined_functions = list()
function_arguments = list()
all_local_variables = list()

names = list()

ast_types = list()

for el in ast.walk(root):
    ast_types.append(type(el))
    if isinstance(el, ast.FunctionDef):
        defined_functions.append({el.name:el.lineno})
    # elif isinstance(el, ast.arg):
    #     function_arguments.append({el.arg:el.lineno})
    # elif isinstance(el, ast.Assign):
    #     for x in el.targets:
    #         if isinstance(x, ast.Name):
    #             all_local_variables.append({[x.id][0]:el.lineno})
    #         elif isinstance(x, ast.Tuple):
    #             all_local_variables += [{y.id:x.lineno} for y in x.elts]
    #         elif isinstance(x, ast.Attribute):
    #             all_local_variables.append({x.attr:el.lineno})
    #         else:
    #             print(linewise_contents[x.lineno])
    #             print(type(x))
    #             print(x.__dict__)
    #             print('------------------')
    # elif isinstance(el, ast.Return):
    #     print(linewise_contents[el.lineno])
    #     print(type(el), el.__dict__)
    #     print('------------------')
    elif isinstance(el, ast.Name):
        names.append({el.id:el.lineno})
        print(linewise_contents[el.lineno])
        print(type(el), el.__dict__)
        print('------------------')
       # print(el.__dict__)

# names = [name for name in names if ((name in defined_functions) or (name in all_local_variables))]

ast_types = set(ast_types)
print(f'Unique types: {ast_types}')

print(f"Defined Functions: {defined_functions}")
print(f"Variables: {all_local_variables}")
print(f"Function Arguments: {function_arguments}")
print(f"Names: {names}")


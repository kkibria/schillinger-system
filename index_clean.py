import yaml

def convert(spec, node:dict):
    cur = None
    for item in spec['b']:
        if isinstance(item, dict):
            if cur is not None:
                convert(item, cur)
            else:
                convert(item, node)
        else:
            cur = {NAME: item, CONTENT: []}
            node[CONTENT].append(cur)

def remove_content(node:dict):
    content = node[CONTENT]
    if len(content) < 1:
        node.pop(CONTENT, None)
    else:
        for i in content:
            remove_content(i)

with open("bookindex_original.yaml") as stream:
    try:
        b_i=yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

NAME = "n"
CONTENT = "c"
root = {NAME: "root", CONTENT: []}
convert(b_i, root)
remove_content(root)
clean = yaml.safe_dump(root[CONTENT], sort_keys=False, width=300)
with open("bookindex.yaml", "w") as f:
    f.write(clean)


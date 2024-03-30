from pathlib import Path
import pypdf
import re
import yaml


# def toc2pdf(pgtoc):
#     if pgtoc < 879:
#         return pgtoc+28
#     return pgtoc+32

def pdf2toc(pgpdf):
    if pgpdf < 879+28:
        return pgpdf-28
    else:
        return pgpdf-32

pfigidx = Path("figindex.yaml")

if pfigidx.exists():
    with open(pfigidx) as stream:
        try:
            fig_list = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

else:    
    reader = pypdf.PdfReader("schillinger-system.pdf")
    pat = r"(Figure([0-9]+(\(.*?\))?)\.)"
    fig_list = []
    for page in reader.pages:
        print(".", end="", flush=True)
        text = page.extract_text()
        pg = page.page_number+1
        result = re.findall(pat, text)
        if len(result) > 0:
            for i in result:
                fig_list.append({"fig":i[1], "page":pdf2toc(pg)})

    figyaml = yaml.safe_dump(fig_list, sort_keys=False, width=300)

    with open(pfigidx, "w") as f:
        f.write(figyaml)

NAME = "n"
CONTENT = "c"
BOOKMARK = None
with open("bookindex.yaml") as stream:
    try:
        BOOKMARK={NAME:'root', CONTENT:yaml.safe_load(stream)}
    except yaml.YAMLError as exc:
        print(exc)
        exit(1)

# insert figures in bookindex
print()
print("##### inserting figures in bookindex")

fig_list_len = len(fig_list)
curfig = 0
if CONTENT in BOOKMARK:
    last = None
    lasti = None 

    for i in BOOKMARK[CONTENT]:
        item = i[NAME]
        a = item.split()
        l = len(a)
        desc = " ".join(a[0:l-1])
        try:
            page = int(a[l-1])
        except ValueError as exc:
            print(exc)
            print("******* item is ", item)
        if last is not None:
            # search all figures between last and this page
            first = 0
            bkfigs = []
            while True:
                if curfig < fig_list_len:
                    figpg = fig_list[curfig]['page']
                    if figpg >= last and figpg < page:
                        if len(bkfigs) == 0:
                            first = figpg
                        fignode = f"FIGURE {fig_list[curfig]['fig']}. {figpg}"
                        bkfigs.append({NAME: fignode})
                        curfig += 1
                        print(".", end="", flush=True)
                    else:
                        if len(bkfigs) > 0:
                            node = {NAME:f'FIGURES {first}', CONTENT:bkfigs}
                            lasti[CONTENT] = [node] + lasti[CONTENT]
                        break
                else:
                    break
        last = page
        lasti = i


newindex = yaml.safe_dump(BOOKMARK[CONTENT], sort_keys=False, width=300)
with open("bookindex-fig.yaml", "w") as f:
    f.write(newindex)

figyaml = yaml.safe_dump(fig_list, sort_keys=False, width=300)

with open("figindex.yaml", "w") as f:
    f.write(figyaml)

print()
print("done")
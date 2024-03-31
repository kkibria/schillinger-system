from pathlib import Path
import pypdf
import re
import yaml

# def toc2pdf(pgtoc):
#     if pgtoc < 879:
#         return pgtoc+28
#     return pgtoc+32
NAME = "n"
CONTENT = "c"

def pdf2toc(pgpdf):
    if pgpdf < 879+28:
        return pgpdf-28
    else:
        return pgpdf-32

def get_fig_list(pfigidx):
    if pfigidx.exists():
        with open(pfigidx) as stream:
            fig_list = yaml.safe_load(stream)

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

        print()
    return fig_list

def get_desc_page(item):
    a = item.split()
    l = len(a)
    desc = " ".join(a[0:l-1])
    try:
        page = int(a[l-1])
    except ValueError as exc:
        print("******* item is ", item)
        raise
    return desc, page

def insert_fig(fig_list, idx_node):
    fig_list_len = len(fig_list)
    curfig = 0

    if CONTENT in idx_node:
        last = None
        lasti = None

        for i in idx_node[CONTENT]:
            item = i[NAME]
            _, page = get_desc_page(item)
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
                            fig_node_name = f"FIGURE {fig_list[curfig]['fig']}. {figpg}"
                            bkfigs.append({NAME: fig_node_name})
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
    print()

if __name__ == '__main__':

    pfigidx = Path("figindex.yaml")
    old_idx = "bookindex.yaml"
    new_idx = "bookindex-fig.yaml"

    try:
        fig_list = get_fig_list(pfigidx)

        idx_root_node = None
        with open(old_idx) as stream:
            idx_root_node={NAME:'root', CONTENT:yaml.safe_load(stream)}

        # insert figures in bookindex
        print("##### inserting figures in bookindex")
        insert_fig(fig_list, idx_root_node)

        newindex = yaml.safe_dump(idx_root_node[CONTENT], sort_keys=False, width=300)
        with open(new_idx, "w") as f:
            f.write(newindex)

    except (yaml.YAMLError, ValueError) as exc:
        print(exc)
        exit(1)

    print("done")
import argparse
from pprint import pprint
from pypdf import PdfWriter, PdfReader, PageRange
import yaml

YAML_CHECK = False
OUTLINE = False

def set_opt(yc, ol):
    global YAML_CHECK, OUTLINE
    YAML_CHECK, OUTLINE = yc, ol

def toc2pdf(pgtoc):
    if pgtoc < 879:
        return pgtoc+28
    return pgtoc+32

def add2pages(page):
    pg = RDR_ALT.pages[page]
    h = pg.mediabox.height
    h_adj = (h- H_REF)/2
    pg.mediabox.bottom = h_adj
    pg.mediabox.top = h_adj+H_REF

    l = pg.mediabox.left
    r = pg.mediabox.right
    mid = (l+r)/2

    pg.mediabox.right = W_REF
    WRTR.add_page(pg)

    pg.mediabox.right = mid+W_REF
    pg.mediabox.left = mid
    WRTR.add_page(pg)

def insert_missing(insert_alt_page, goodpart):
    goodbgn, goodend = goodpart
    add2pages(insert_alt_page)
    prng = PageRange(slice(goodbgn, goodend))
    WRTR.append(RDR2, pages=prng)

def bookmark(spec, node=None, level=0):
    cur = None
    for item in spec['b']:
        if isinstance(item, dict):
            if cur is not None:
                bookmark(item, cur, level+1)
            else:
                bookmark(item, node, level+1)
        else:
            a = item.split()
            l = len(a)
            # WRTR.add_outline_item_dict
            desc = " ".join(a[0:l-1])
            try:
                page = int(a[l-1])
            except ValueError as exc:
                print(exc)
                print("******* item is ", item)

            if YAML_CHECK or OUTLINE:
                if OUTLINE:
                    fmt = "{0}{1}"
                else:
                    fmt = "{0}{1}......{2} => {3}"
                print(fmt.format(" "*level*2, desc, page, toc2pdf(page)))
            else:
                cur = WRTR.add_outline_item(desc, toc2pdf(page)-1, node)

def handle_args():
    parser = argparse.ArgumentParser(
        prog="process_pdfs",
        description='Processes Schillinger pdfs',
        epilog=f'(c) Khan Kibria')

    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument('-y', '--yaml-check', default=False,
                    action='store_true')
    action.add_argument('-l', '--outline', default=False,
                    action='store_true')
    action.add_argument('-p', '--pdf', default=False,
                    action='store_true')
    
    args = parser.parse_args()
    set_opt(args.yaml_check, args.outline)

if __name__ == '__main__':

    handle_args()

    BOOKMARK=None
    with open("bookindex.yaml") as stream:
        try:
            BOOKMARK=yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            exit(1)

    if YAML_CHECK:
        bookmark(BOOKMARK)

    else:
        RDR1 = PdfReader("sch-vol1.pdf")
        RDR2 = PdfReader("sch-vol2.pdf")
        RDR_ALT = PdfReader("sch-alt.pdf")
        WRTR = PdfWriter()

        pr1 = PageRange(slice(8, 914))
        WRTR.append(RDR1, pages=pr1)
        pr2_1 = PageRange(slice(5, 82))
        WRTR.append(RDR2, pages=pr2_1)

        pg_ref = RDR2.pages[82]
        W_REF = pg_ref.mediabox.width
        H_REF = pg_ref.mediabox.height

        # page 952-953
        insert_missing(508, (82, 92))
        # page 964-965
        insert_missing(514, (92, 122))
        # page 996-997
        insert_missing(530, (122, 765))

        OL_ROOT = WRTR.get_outline_root()
        bookmark(BOOKMARK, OL_ROOT)
        
        fn = "schillinger-system.pdf"
        with open(fn, "wb") as fp:
            WRTR.write(fp)

        print(f'Pdf file "{fn}" has been written')
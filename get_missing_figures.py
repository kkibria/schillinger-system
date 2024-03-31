from pathlib import Path
import sys
from extract_fig_pages import get_fig_list

def check_missing(fig, page):
    global last, lastpage
    try:
        fig = int(fig)
    except:
        print (f'# check non number {fig} {page}')
        return 

    if last is not None:
        delta = fig - last
        if delta < 0:
            print(f"#### backward??? last = {last}, cur = {fig}")
        if delta > 1:
            print(f"#### last = {last}, cur = {fig}")
            print(f"#### missing figures between page {lastpage} {page}")
            for m in range(last+1, fig):
                print(f"- fig: '{m}'")
                print("  page: -9999")
    last = fig
    lastpage = page


pfigidx = Path("figindex.yaml")
fig_list = get_fig_list(pfigidx)

last = None
lastpage = None

with open("missing_figures.yaml", "w") as sys.stdout:
    for i in fig_list:
        check_missing(**i)
sys.stdout = sys.__stdout__

print("done")
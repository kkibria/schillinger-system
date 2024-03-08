# Schillinger System of Musical Composition

I got interested in Schillinger's System some time back. It consists of 12 books
published in 2 large volumes. Total is about 1500 pages.

Originally, I downloaded a large pdf from
somewhere, but this large pdf was hard to navigate.
It was quite inconvenient due to its size scrolling back and forth
between cross referencing contents. As such, reading this was put
to back burner.

Later, I was inspired to dig into it more, but also decided to create
bookmarks for the pdf so it is easier to navigate between parts of the books.
As a result, I did this python project.

I am assuming you know python already. If not, there are plenty of places in the net
including youtube that will provide many free learning resources. Python is a very *easy
to learn and use* language.

## What and How?
This python project is used to generate TOC for existing PDFs using `pypdf` package.

For this project, 
- A virtual environment was used. 
- I located two out of print pdfs that was scanned by some academic library in internet archive.
- I downloaded those, volume 1 and volume 2.

## Code
The `process_pdfs.py` file contains the code I wrote.

It performed, 
- Concatenation of volume 1 and volume 2.
- There were some missing pages in volume 2. A third alternate pdf was also downloaded from internet archive that has the missing pages.
- Missing pages were copied and inserted from the alternate pdf.
- TOCs were copy-pasted from scanned pdfs and manually edited to construct `bookindex.yaml`
- To yaml was checked without processing the pdfs by setting `YAML_CHECK = True` in `process_pdfs.py` to fix all the yaml problems first.
- Finally, the yaml TOC was processed and inserted as bookmarks in the newly constructed pdf and saved.

### Source Pdf Download Links
- [Volume 1](https://archive.org/download/in.ernet.dli.2015.167764/2015.167764.The-Schillinger-System-Of-Musical-Composition-Volume-I-Books-I-Vii-Volume-Ii-Books-Viii-Xii_text.pdf) which was renamed as `sch-vol1.pdf`.
- [Volume 2](https://archive.org/download/in.ernet.dli.2015.89483/2015.89483.The-Schillinger-System-Of-Musical-Composition-Volume-Ii-Books-Viii-Xii_text.pdf) which was renamed as `sch-vol2.pdf`.
- [Alternate](https://ia801008.us.archive.org/30/items/SchillingerSystem/Schillinger%20System%20of%20Musical%20Composition_text.pdf) which was renamed as `sch-alt.pdf`.

## Steps

* Clone this repo.
* Download the pdf files from the links and save in the cloned folder.
* Rename the pdf files as mentioned.
* Create a virtual environment if you want.
* Install libraries needed by running `pip install -r requirements.txt`
* Run python file `python process_pdfs.py` which will create the new pdf file.
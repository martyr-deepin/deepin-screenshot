# build documents
EPYDOC=epydoc
DSTDOC=docs
INPUT=src/*.py src/_share/*.py

all:
	$(EPYDOC) --html --graph=all -v -o $(DSTDOC) --name Deepin-Screenshot $(INPUT)
	$(EPYDOC) --pdf --graph=all -v -o $(DSTDOC) --name Deepin-Screenshot $(INPUT)

html:
	$(EPYDOC) --html --graph=all -v -o $(DSTDOC) --name Deepin-Screenshot $(INPUT)

pdf:
	$(EPYDOC) --pdf --graph=all -v -o $(DSTDOC) --name Deepin-Screenshot $(INPUT)

clean:
	rm -rf $(DSTDOC)

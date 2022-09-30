# fackel-to-tei
Python (and XSLT) based workflow to convert Fackel-XML into text based XML/TEIs

* `fetch_data.sh` copies original FACKEL XMLs into `./data`

* run `make_text_files.py` to create XML/(TEI) files per Fackel Text. Original fackel mark up is saved into `data/fackel_out`, the TEIs are saved into `data/editions`. The files are converted with `totei.xsl`


* to add `@ref` into `rs type person` elements, (maybe) run https://github.com/csae8092/fackel-texte-data/blob/main/person_lookup.py
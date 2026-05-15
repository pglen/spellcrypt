import os

doclist = []; droot = "docs/"
doclistx = os.listdir(droot)
for aa in doclistx:
    doclist.append(droot + aa)

print("doclist:", doclist)

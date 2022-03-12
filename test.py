import notenliste

file1 = open("notenliste.html.example", "r")
content = file1.read()
file1.close()

[noten, studiengang] = notenliste.parseFromHTML(content)
print(noten)

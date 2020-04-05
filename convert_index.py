import re

with open(r"templates/index.html", "r") as file:
    html = file.read()

scripts = re.compile(r"/static/js/\S*\.js")
css = re.compile(r"/static/css/\S*\.css")

scripts = scripts.findall(html)
mapper = {k: "{% static '" + k[8:] + "' %}" for k in scripts}

for k, v in mapper.items():
    html = html.replace(k, v)

css = css.findall(html)
mapper = {k: "{% static '" + k[8:] + "' %}" for k in css}

for k, v in mapper.items():
    html = html.replace(k, v)

html = "{% load static %}\n" + html

with open(r"templates/index.html", "w") as file:
    file.write(html)

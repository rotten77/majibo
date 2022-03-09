# Majibo - Python static stice generator

Majibo is a simple static site generator. It uses Markdown for writing content including some extra tags, Jinja2 and Bootstrap 5 for templates.


## Shortcodes

### Include

	{{include my_file}}

Includes `my_file.md` from `content/include` folder. 

### Image

{{image image-01.jpg "Title of an image"}}

### Gallery

{{gallery image-01.jpg image-02.jpg image-03.jpg}}

### YouTube video

{{youtube aSK8_Kdsnjka}}

### Iframe

{{iframe 21x9 https://server.com/...}}

### Gist

{{gist https://gist.github.com/...}}
# Majibo - Python static stice generator

Majibo is a simple static site generator. It uses Markdown for writing content including some extra tags, Jinja2 and Bootstrap 5 for templates.


## Shortcodes

### Include

	{{include my_file}}

Includes `my_file.md` from `content/include` folder.

### Image

	{{image file.png "Title of an image"}}

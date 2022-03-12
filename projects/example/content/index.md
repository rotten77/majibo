Title: Majibo - Static site generator written in Python

# Majibo

----

* Static site generator written in Python
* Designed for my personal purposes
* No database, content is based on markdown files
* Powerful shortcodes for images, YouTube videos and other stuff
* Fast and secure! Of course, because it produces only static HTML sites :-)

Majibo is a japan world for... just kidding. The name is just an acronym from used components:

* **ma** = [markdown](./content.html)
* **ji** = [jinja templates](./templates.html)
* **bo** = [bootstrap](./templates.html)

## How to use

**[Download or clone](https://github.com/rotten77/majibo)** Majibo repository and explore the `example` project!

You can find various files and folders so maybe some basic description is needed:

* `/assets/` - folder for your stylesheet, javascripts, etc.
	* `style.scss` - Sass stylesheet file, it includes Bootstrap, you can define colors and other stuff (see [Templates](./templates.html))
* `/content/` - content of your website, one Markdown file = one HTML file, you can find more details on [Content](./content.html))
* `/img/` - place your images here
* `/template/` - folder with Jinja templates (see [Templates](./templates.html))
* `config.py` - project configuration file (see [Configuration](./configuration.html))

## Build and publish

In Majibo's root folder you can find building script `build.py`. Run it from command line and then you can find your website in the `/dist/` folder. These arguments are available:

* `-p project_name` - build project from `project_name` folder
* `-d` - build project in [development mode](./templates.html#development-mode)
* `-v` - show Majibo version

Examples:

{{gist https://gist.github.com/rotten77/03bb86d0a64a7e6bdcb564be28c26002}}

## Components

Majibo uses these essential components:

* [Python-Markdown](https://python-markdown.github.io/)
* [Jinja Templates](https://jinja.palletsprojects.com/en/3.0.x/)
* [Bootstrap 5](https://getbootstrap.com/)
* [BS5-Lightbox](https://trvswgnr.github.io/bs5-lightbox/)

...and some other Python modules that you can find in [requirements.txt](https://github.com/rotten77/majibo/blob/main/requirements.txt) file.
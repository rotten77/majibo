Title: Templates
Description: Majibo static site generator template documentation.

# Templates

----

Majibo uses Jinja as a templating engine. 

## Template

Default template is `template.html` but you can specify particular template for page by `Template` meta tag.

## Variables

* `site.name` - site (project) name
* `site.url` - site URL
* `site.author` - site author
* `site.navigation` - navigation object
* `site.description` - site description
* `site.generator.name` - Majibo name
* `site.generator.url` - Majibo URL
* `site.generator.version` - Majibo version
* `page.url` - page URL
* `page.id` - page id (`info.md` = `info`)
* `page.is_index` - true/false if page is index.md
* `page.type` - open graph page type
* `page.language` - page language
* `page.title` - page title
* `page.description` - page description
* `page.image` - page image
* `page.author` - page author
* `page.content` - page content (HTML)
* `link_base` - link base folder (`./`)
* `assets.base` - assets base folder (`./assets/`)
* `assets.stylesheet` - site CSS file
* `assets.jquery.js` - jQuery JS file
* `assets.bootstrap.js` - Bootstrap JS
* `assets.bootstrap.lightbox.js` - BS5-lightbox JS

## Bootstrap

Majibo uses [Bootstrap](https://getbootstrap.com/) CSS framework. Main Sass file is `/assets/style.scss`. This file includes Bootstrap files. You have to use Sass compiler to compile it to CSS file.

I am using [Live Sass Compiler](https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass) extension for VS Code.

{{image live-sass-compiler.png "How to use Live Sass Compiler in VS Code editor"}}

## Development mode

You can build project in development mode with this command: `python build.py -p project_name -d`

* Project `/dist/` folder is not removed and re-builded (files are just updated) so you can use [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension for VS Code
* Stylesheet is included directly from project's `/asset/` folder do you can use *Live Sass Compiler* for live preview of CSS changes

{{image live-server.png "How to use Live Server in VS Code editor"}}
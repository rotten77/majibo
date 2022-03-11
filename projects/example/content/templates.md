# Templates

Majibo uses Jinja as a templating engine. 

## Template

Default template is `template.html` but you can specify particular template for page by `Template` meta tag.

## Variables

* `site_name` - site (project) name
* `site_url` - site URL
* `site_author` - site author
* `page_url` - page URL
* `page_id` - page id (`info.md` = `info`)
* `page_is_index` - true/false if page is index.md
* `page_type` - open graph page type
* `page_language` - page language
* `page_title` - page title (contains also site project name)
* `link_base` - link base folder (`./`)
* `stylesheet` - link to stylesheet
* `navigation` - navigation object
* `meta` - meta tags
	* `title` - page title
	* `image` - page image
	* `description` - page description
	* `author` - page author
* `content` - page content (HTML)

## Bootstrap

Majibo uses [Bootstrap](https://getbootstrap.com/) CSS framework. Main Sass file is placed in `/assets/style.scss` file. This files includes Bootstrap file. You have to use Sass compiler to compile it to CSS file.

I am using [Live Sass Compiler](https://marketplace.visualstudio.com/items?itemName=ritwickdey.live-sass) extension for VS Code.

{{image live-sass-compiler.png "How to use Live Sass Compiler in VS Code editor"}}

## Development mode

You can build project in development mode with this command: `python build.py -p project_name -d`

* Project `/dist/` folder is not removed and re-builded (files are just updated) so you can use [Live Server](https://marketplace.visualstudio.com/items?itemName=ritwickdey.LiveServer) extension for VS Code
* Stylesheet is included directly from project's `/asset/` folder do you can use *Live Sass Compiler* for live preview of CSS changes

{{image live-server.png "How to use Live Server in VS Code editor"}}
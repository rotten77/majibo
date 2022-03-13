Title: Content
Description: Majibo static site generator content documentation.

# Content

----

Create Markdown files in `/content/` folder, one Markdown file = one HTML file. There is no support for sub-folders, categories or tags. Majibo is just for flat-structured projects.

Place images in `/img/` folder.

## Meta data

Majibo supports these Markdown meta data tags

* `Title` - page title
* `Description` - page description
* `Image` - page image
* `Type` - open graph page type (default is `website`)
* `Lang` - page language
* `Template` - [template](./templates.html) that is used for rendering
* `Author` - page author
* `Date` - page publication date

## Shortcodes

Majibo extends Markdown syntax with some powerful shortcodes. See [example page](./example.html) for results.

### Include

{{gist https://gist.github.com/rotten77/df4a2b57502282e6e970ba28951cc3a1}}

Include an markdown file from `content/include` folder.

### Image

{{gist https://gist.github.com/rotten77/3057bdd3bb08f89eb3570d49950f44ae}}

Shows image with modal viewer (lightbox). Works only with images in `img` folder. It is possible to add an caption (figure).

### Gallery

{{gist https://gist.github.com/rotten77/275c51110c00f04a6e29ac56afb93e56}}

Shows image with modal viewer (lightbox). Works only with images in `img` folder.

### YouTube

{{gist https://gist.github.com/rotten77/d7ee25d5418dae5aa26465f21e099251}}

Shows YouTube video. You can use video or playlist ID as an argument.

### Embed content

{{gist https://gist.github.com/rotten77/4fc4dfa9691371893f87815d33a3ec30}}

Shows external (embed) content, you can specify ratio (see Bootstrap documentation for other info).

### Gists

{{gist https://gist.github.com/rotten77/a467387ef368e0414e879eb16531f8db}}

Shows GitHub's gist.

### Div

{{gist https://gist.github.com/rotten77/5905f25915622815e9cc399f923c74cb}}

Add div `<div>` to your page.
Title: Configuration
Description: Majibo static site generator configuration documentation.

# Configuration

----

Project configuration is placed in `config.py` file:

* `SITE_***` - your site parameters
* `IMAGE_MAX_WIDTH` - max width of image inserted by [image shortcode](./content.html#shortcodes), if image is wider than this value, image is resized and could be displayed in modal lightbox
* `IMAGE_GALLERY_THUMBNAIL_SIZE` - size of image thumbnail in [gallery](./content.html#shortcodes)
* `SITE_NAVIGATION` - navigation that can be used in templates
* `PAGE_DEFAULT_IMAGE` - default page image that is used if there is no image in page's [meta data](./content.html#meta-data)
* `PAGE_DEFAULT_DESCRIPTION` - default page description that is used if there is no description in page's [meta data](./content.html#meta-data)
* `DATETIME_FORMAT` - date and time format (Python syntax)
* `DATE_FORMAT` - date format (Python syntax)
* `TIME_FORMAT` - time format (Python syntax)

See [example project's config](https://github.com/rotten77/majibo/blob/main/projects/example/config.py) for more details.
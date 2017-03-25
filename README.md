# Blended
Blended is a static website generator written in Python and licensed under the GPL 3.0 open-source license. It supports a HTML-based templating system, content written in HTML, Markdown, Textile, reStructuredText, Jade, Docx, and Plain Text. It also supports the compiliation of Sass, Less, Stylus, and CoffeeScript. Blended makes it easy to deply your websites by incuding a built-in FTP uploader. In addition, Blended is powerfully upgradeable because it has support for a Python plugin system.

There is a full step-by-step *Getting Started* tutorial on [the website](http://jmroper.com/blended/getting-started.html).

## Installing

To install Blended from PyPi (recommended) run:

`pip install blended`

To build and install Blended from source run:

`git clone https://github.com/johnroper100/Blended.git`

`cd Blended`

`pip install .`

## Running

To use Blended after you have installed it, run:

`blended init`

This will help you start up a new website. If you need help, run:

`blended --help`

and you will see all of the commands that are available.

## Building Your Site

To build the site you have created with Blended run

`blended build`

or

`blended interactive` (for on file change building)

For any command that you run, you can specify an alternative `--outdir` to build or view from. For example, to build to the `soutput` folder, run `blended build --outdir soutput`.

## Working with templates

Each Blended website uses four template files:

* header.html (Required)
* footer.html (Required)
* home_page.html (Not required but the site looks better)
* content_page.html (Not required but the site looks better)
* nav(1-6).html (You can have up to 6 different nav templates. For example, `nav2.html`)

In these files you place the markup for each section to be generated.

When working with pages, you can optionally specifiy which template you want (other than `content_page.html`) by adding the name of the template file without the extension to the first line of the page, and then at least five `-`s to the second line. For example, if I wanted to use a template called `blog_page.html` for a certain page, I would put

```
blog_page
-----
```

at the **top** of the page. Make sure you put it at the top or else it will not work!

You have some variables that you can use in your templates to pull in values while building:

* `{website_name}`
* `{website_description}`
* `{website_description_long}` (Use for long descriptions like an author bio)
* `{author_name}`
* `{website_language}`
* `{website_license}`
* `{page_content}` (Can only be used in the content_page.html template file)
* `{page_time}` (Time the page was modified)
* `{relative_root}` (Returns a relative path for the current file)
* `{random_number}`
* `{build_date}`
* `{build_time}`
* `{build_datetime}`
* `{`(page_filename)`_active}` (When building, if the active page equals the filename in the tag, the tag is replaced by `active` ex. `{getting-started.html_active}`)
* `{nav(1-6)}` (Use to place navbars. You can have up to 6 different templates. For example, `{nav2}`)
* `{page_list}` (Lists all the pages in `<ul><li><a href="page-name.html">page-name</a></li></ul>` format)
* `{page_file}` (The full filename of the page. ex. `getting-started.html`)
* `{page_filename}` (the filename of the page without the .html extension. ex. `getting-started`)
* `{page_name}` (Gives the name of the current page. Makes the page name look more pretty. For example, `getting-started.html` is converted to `Getting Started`)
* `{page_folder}` (Gives the name of the current page's folder. Makes the folder name look more pretty. For example, `getting-started` is converted to `Getting Started`)
* `{page_folder_orig}` (Gives the name of the current page's folder)
* `{blended_version}` (Gives Blended's current version)
* `{blended_version_message}` (Gives Blended's current version with a nice message: `Built with Blended v4.4`)

Wherever you put these variables in the templates, they will be replaced by the values in your config.py file. The variables must stay within the curley brackets. You can even put variables inside the content of other variables!

## Working with Plugins

To use plugins, include them in the `plugins` list in `config.py`.

If the plugin is meant to be called in your templates, ex. `{html_comment_box}` then insert it into the plugins list like `plugins = [["html_comment_box"]]`.

If the plugin is meant to be run on build, ex. `{minify_images}` then insert it into the plugins list like `plugins = [["RUN", "minify_images"]]`.

You can use multiple plugins at once, ex. `plugins = [["html_comment_box"], ["RUN", "minify_images"]]`

## Pre-Made Templates

* Simple starter template for Blended called blended-simple ([GitHub page](https://github.com/johnroper100/blended-simple))

* Blog template called blended-blog ([GitHub page](https://github.com/johnroper100/blended-blog))

* Software showcase ([Github page](https://github.com/johnroper100/blended-software))

## Plugins

* Google Analytics ([GitHub page](https://github.com/johnroper100/blended_google_analytics))

* HTML Comment Box ([GitHub page](https://github.com/johnroper100/blended_html_comment_box))

## Projects That Use Blended

* The [Blended website](http://jmroper.com/blended)

* A full render managment dashboard ([GitHub page](https://github.com/johnroper100/RenderManagementDashboard))

* DVDStyler website redesign ([Github page](https://github.com/johnroper100/dvdstyler-web))

* MakeHuman website redesign ([Github page](https://github.com/johnroper100/makehuman-web))

* LilyPond website redesign ([Github page](https://github.com/johnroper100/LilyPond-Web-Redesign))

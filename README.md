# Blended
Blended is a static website generator written in Python and licensed under the GPL 3.0 open-source license. It supports a HTML-based templating system, content written in HTML, Markdown, Textile, reStructuredText, Jade, Docx, and Plain Text. It also supports the compilation of SASS, Less, Stylus, and CoffeeScript. Blended makes it easy to deploy your websites by including a built-in FTP uploader. In addition, Blended is powerfully upgradeable because it has support for a Python plugin system.

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

For any command that you run, you can specify an alternative `--outdir` to build or view from. For example, to build to the `source_output` folder, run `blended build --outdir source_output`.

Inside the `config.py` file, you can set `minify_css` and `minify_js` to true to optimize your CSS and JS files after building.

## Working With templates

You can install templates from GitHub using `blended install-template`.

Each Blended website uses four template files:

* header.html (Required)
* footer.html (Required)
* home_page.html (Not required but the site looks better)
* content_page.html (Not required but the site looks better)
* nav(name).html (You can have up to 6 different nav templates. For example, `navTest.html` or `nav_test.html`)
* page_list_item.html (Not required, if used, this will replace each page list item content. Can have the variables `{name}`, `{content}`, `{content_short}`, `{date}`, `{day}`, `{month}`, `{year}`, `{path}`)

In these files you place the markup for each section to be generated.

When working with pages, you can optionally specify which template you want (other than `content_page.html`) by adding the name of the template file without the extension to the first line of the page, and then at least five `+`s to the second line. For example, if I wanted to use a template called `blog_page.html` for a certain page, I would put

```
blog_page
+++++
```

at the **top** of the page. Make sure you put it at the top or else it will not work!

You have some variables that you can use in your templates to pull in values while building:

* `{website_name}`
* `{website_description}`
* `{website_description_long}` (Use for long descriptions like an author bio)
* `{author_name}`
* `{author_bio}`
* `{website_language}`
* `{website_license}`
* `{page_content}` (Can only be used in the content_page.html template file)
* `{page_date}` (Date/Time the page was written/modified)
* `{page_day}` (Day the page was written/modified)
* `{page_month}` (Month the page was written/modified)
* `{page_year}` (Year the page was written/modified)
* `{relative_root}` (Returns a relative path for the current file)
* `{random_number}`
* `{build_date}`
* `{build_time}`
* `{build_datetime}`
* `{`(page_filename)`_active}` (When building, if the active page equals the filename in the tag, the tag is replaced by `active` ex. `{getting-started.html_active}`)
* `{nav`(name)`}` (Use to place navbars. To add a navbar, write `nav` plus something else. For example, `{nav2}` or `{nav_test}`)
* `{page_list}` (Lists all the pages in `<ul><li><a href="page-name.html">page-name</a></li></ul>` format)
* `{page_file}` (The full filename of the page. ex. `getting-started.html`)
* `{page_filename}` (the filename of the page without the .html extension. ex. `getting-started`)
* `{page_name}` (Gives the name of the current page. Makes the page name look more pretty. For example, `getting-started.html` is converted to `Getting Started`)
* `{page_folder}` (Gives the name of the current page's folder. Makes the folder name look more pretty. For example, `getting-started` is converted to `Getting Started`)
* `{page_folder_orig}` (Gives the name of the current page's folder)
* `{blended_version}` (Gives Blended's current version)
* `{blended_version_message}` (Gives Blended's current version with a nice message: `Built with Blended v4.9`)

Wherever you put these variables in the templates, they will be replaced by the values in your config.py file. The variables must stay within the curley brackets. You can even put variables inside the content of other variables!

## Working With Plugins

You can install plugins from PyPi, for example `pip install blended_google_analytics`.
You can also install plugins from GitHub using `blended install-plugin`.

To use plugins, include them in the `plugins` list in `config.py`.

If the plugin is meant to be called in your templates, ex. `{html_comment_box}` then insert it into the plugins list like `plugins = ["html_comment_box"]`.

You can use multiple plugins at once, ex. `plugins = ["html_comment_box", "minify_images"]`

## Working With Custom Variables

Inside of your `config.py` there is a variable `custom_variables = {}`. This is a dictionary of all of the custom variables you would like to use. To add a variable, add it as a dictionary item.

Here are some examples:

`custom_variables = {"software_name": "Blended"}`

`custom_variables = {"software_name": "Blended", "software_version": "5.0"}`

## Pre-Made Templates

Remember that you can install templates from GitHub using `blended install-template`.

* Simple ([GitHub page](https://github.com/BlendedSiteGenerator/blended-simple))

* Blog ([GitHub page](https://github.com/BlendedSiteGenerator/blended-blog))

* Software Showcase ([GitHub page](https://github.com/BlendedSiteGenerator/blended-software))

## Plugins

* Google Analytics ([GitHub page](https://github.com/BlendedSiteGenerator/blended_google_analytics))

* HTML Comment Box ([GitHub page](https://github.com/BlendedSiteGenerator/blended_html_comment_box))

* Twitter Cards ([GitHub page](https://github.com/BlendedSiteGenerator/blended_twitter_cards))

* Google Fonts ([GitHub page](https://github.com/BlendedSiteGenerator/blended_google_fonts))

* Import Bootstrap ([GitHub page](https://github.com/BlendedSiteGenerator/blended_import_bootstrap))

## Projects That Use Blended

* The [Blended website](http://jmroper.com/blended)

* The [Art Of Illusion website redesign](https://github.com/ArtOfIllusion/AOI-website)

* A full render management dashboard ([GitHub page](https://github.com/johnroper100/RenderManagementDashboard))

* DVDStyler website redesign ([GitHub page](https://github.com/johnroper100/dvdstyler-web))

* MakeHuman website redesign ([GitHub page](https://github.com/johnroper100/makehuman-web))

* LilyPond website redesign ([GitHub page](https://github.com/johnroper100/LilyPond-Web-Redesign))

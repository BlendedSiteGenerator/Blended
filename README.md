# Blended
Static Site Generation Using HTML and Python. Blended is a command line tool that helps you easily create HTML websites by mimicing the templating system used by PHP and WordPress. Blended supports interactive (on file change) building as well as a standatrd build command. Websites created using Blended are easy to manage ande deploy.

## Installing

To install Blended from PyPi (recommended) run:

`pip install blended`

To build and install Blended from source run:

`git clone https://github.com/johnroper100/Blended.git`

`cd Blended`

`pip install Click`

`pip install colorama`

`pip install .`

## Running

To use Blended after you have installed it, run:

`blended init`

This will help you start up a new website. If you need help, run:

`blended --help`

and you will see all of the commands that are available.

## Working with templates

Each Blended website uses four template files:

* header.html (Required)
* footer.html (Required)
* home_page.html (Not required but the site looks better)
* content_page.html (Not required but the site looks better)
* nav(1-6).html (You can have up to 6 different nav templates. For example, `nav2.html`)

in these files you place the markup for each section to be generated.

You have some variables that you can use in your templates to pull in values while building:

* `{website_name}`
* `{website_description}`
* `{author_name}`
* `{website_language}`
* `{website_license}`
* `{page_content}` (Can only be used in the content_page.html template file)
* `{random_number}`
* `{build_date}`
* `{build_time}`
* `{build_datetime}`
* `{nav(1-6)}` (Use to place navbars. You can have up to 6 different templates. For example, `{nav2}`)

Wherever you put these variables in the templates, they will be replaced by the values in your config.py file. The variables must stay within the curley brackets.

There is a simple starter template for Blended called blended-simple. You can download it to use and take a look at from it's own [GitHub page](https://github.com/johnroper100/blended-simple).

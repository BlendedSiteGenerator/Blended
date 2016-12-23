# Blended
Websites created using Blended are easy to manage and deploy. It combines the 'just write' mentality of Markdown and Plain Text with the design and practicality of HTML and Textile. Websites created using Blended are easy to manage and deploy. Blended supports interactive (on file change) building as well as a standard build command. It is able to build from HTML, Markdown, Textile, and Plain Text source files at the same time. This gives you the flexibily to write however you want and to also be able to take other writings and use them easily. Content and templates written for Blended are easy for anyone, even non-coders, to understand. Blended uses a simple, robust, HTML templating system which is very quick to learn. Blended runs on any operating system that has Python 2.7 or Python 3.5 installed. All that is required is access to a command line and the abiliy to install packages using PIP. Blended also supports upload for the built website via FTP to your own server.

There is a full step-by-step *Getting Started* tutorial on [the website](http://jmroper.com/blended/getting-started).

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

## Working with templates

Each Blended website uses four template files:

* header.html (Required)
* footer.html (Required)
* home_page.html (Not required but the site looks better)
* content_page.html (Not required but the site looks better)
* nav(1-6).html (You can have up to 6 different nav templates. For example, `nav2.html`)

In these files you place the markup for each section to be generated.

You have some variables that you can use in your templates to pull in values while building:

* `{website_name}`
* `{website_description}`
* `{author_name}`
* `{website_language}`
* `{website_license}`
* `{page_content}` (Can only be used in the content_page.html template file)
* `{page_time}` (Time the page was modified)
* `{random_number}`
* `{build_date}`
* `{build_time}`
* `{build_datetime}`
* `{nav(1-6)}` (Use to place navbars. You can have up to 6 different templates. For example, `{nav2}`)
* `{page_list}` (Lists all the pages in `<ul><li><a href="page-name.html">page-name</a></li></ul>` format)
* `{page_name}` (Gives the name of the current page. Makes the page name look more pretty. For example, `getting-started.html` is converted to `Getting Started`)
* `{blended_version}` (Gives Blended's current version)
* `{blended_version_message}` (Gives Blended's current version with a nice message: `Built with Blended v2.8`)

Wherever you put these variables in the templates, they will be replaced by the values in your config.py file. The variables must stay within the curley brackets.

There is a simple starter template for Blended called blended-simple. You can download it to use and take a look at from it's own [GitHub page](https://github.com/johnroper100/blended-simple).

There is also a full render managment dashboard built with Blended. You can download it from [GitHub](https://github.com/johnroper100/RenderManagementDashboard).

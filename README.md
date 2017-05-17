# Blended
Blended is a static website generator written in Python and licensed under the GPL 3.0 open-source license. It uses the Jinja2 templating language and has full support for HTML, Markdown, Textile, reStructuredText, Jade, Microsoft Word, and Plain Text documents. In addition, Blended has tools to support easy website management such as direct-to-server FTP transfer.

## Installing

To install Blended, you must first have Python 2.7 or greater installed. Next you should installed Blended using pip by running

`pip install blended`

## Setting up your website

First, create a folder and run `blended init` to create the necessary files.

If you see a theme you would like in [the themes repository](https://github.com/BlendedSiteGenerator/BlendedThemes), download it by running `blended download-theme <theme_name>`. You can also create your own theme.

Once you have a theme, run `blended setup-theme <theme_name>` to configure your website to use it.

## Importing from WordPress

Blended has built-in tools to help you import your WordPress posts. Note that the tool only supports posts at this time. To do so, in WordPress export just your posts. Then, download the file to the root of your Blended blog. Let's call the file `export.xml`. Finally, on the command line, run `blended import-wp export.xml` and the posts should be created.

## Building your website

To build, simply run the `blended build` command.

## Projects That Use Blended

* The [Blended website](http://jmroper.com/blended)

* The [Art Of Illusion website redesign](https://github.com/ArtOfIllusion/AOI-website)

* A full render management dashboard ([GitHub page](https://github.com/johnroper100/RenderManagementDashboard))

* DVDStyler website redesign ([GitHub page](https://github.com/johnroper100/dvdstyler-web))

* MakeHuman website redesign ([GitHub page](https://github.com/johnroper100/makehuman-web))

* LilyPond website redesign ([GitHub page](https://github.com/johnroper100/LilyPond-Web-Redesign))

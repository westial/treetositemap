# treetositemap #

Command line tool that automates the creation of sitemap resources and 
recursively indexes large amount of filtered files and directories.

It recursively looks for files matching the given pattern and creates a full
scalable sitemap resource directory files.

The sitemap resource directory is composed by a main sitemap.xml file, with a
"sitemapindex" node on root tag and a list of "sitemap" nodes into. Those 
"sitemap" nodes contain a "loc" tag respectively pointing to a file with a 
"urlset" node on root tag. And those "urlset" nodes contain a list of "url" 
nodes with the "loc" for every file indexed into.

The maximum number of "url" contained by a "urlset" node file can be set by
command option so you can scale a huge amount of items.


## Requirements ##

Python >= 3.6.2


## Install ##

Install requirements.

`pip install -r requirements.txt`

Run the tests before install.

`python setup.py behave_test`

Definitively install

`python setup.py install`


## Versioning ##

We use [SemVer](http://semver.org/) for versioning.


## Author

* **Jaume Mila** - *Initial work* - [westial](https://github.com/westial)


## License

This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the 
[LICENSE.md](LICENSE.md) file for details.



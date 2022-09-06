Setup.py.local was the version when I came back to this in fall 2022
after almost a year away.

Setup.py.build is what I am now trying out.

BuildWheel, builds a wheel, so the .c and .cython files are not cluttering these directories.  Very nice.

buldInPlace, builds the files in place, easier for develoment. 

There is a problem with ttw/html.py
When cythonizing it gets confuseed.
cython -e html.py
then move it to html.pyx.

Then all is maybe well.
It gets confused with some other html.py file.

setup.py.local setes extensions = []
Meaning nothing gets cythonized.

The inplace command just builds the extensions in place.
Then they have to be copied.  I guess that is old stuff.

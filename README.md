InvisibleCharm
=====

InvisibleCharm is a python script that allows you to hide your files.

Install Python
--------------

Inorder to install Python, please visit [Python.org](https://Python.org/).

Changes
-------

### 2.1.0

Using `Cython`, increased the speed of converting a file to an image and extracting the file from the image.

### 2.1.1 - 2.1.3

Auto release fixed.


Install InvisibleCharm
----------------------

To install **InvisibleCharm**, you can simply use the `pip install InvisibleCharm` command:

```commandline
python -m pip install InvisibleCharm
```

Or you can clone [the repository](https://github.com/MPCodeWriter21/InvisibleCharm) and run:

```commandline
python setup.py install
```

Usage
-----

```
usage: main.py [-h] [--win-embed] [--win-attribute] [--embed] [--to-image] --source-file SOURCE
               [--cover-file COVER] [--dest-file DESTINATION] [--delete-source] [--compress]
               [--encrypt ENCRYPTION_PASS] [--verbose] [--quiet]
               mode

positional arguments:
  mode                  modes: Hide, Reveal

optional arguments:
  -h, --help            show this help message and exit
  --win-embed, -we      Embed files invisibly (Only works on Windows)
  --win-attribute, -wa  Change windows attributes to hide file (Only works on Windows)
  --embed, -e
  --to-image, -i        Converts a file into a png image
  --source-file SOURCE, -s SOURCE
                        Sets the path of SOURCE file
  --cover-file COVER, -c COVER
                        Sets the path of COVER file
  --dest-file DESTINATION, -d DESTINATION
                        Sets the path of DESTINATION file
  --delete-source, -D   Deletes source file
  --compress, -C
  --encrypt ENCRYPTION_PASS, -E ENCRYPTION_PASS
                        Enables encryption - needs an ENCRYPTION_PASSword
  --verbose, -v
  --quiet, -q
```

Examples
--------

- Embed

```shell
# Embeds the source file and the cover file into the destination file.
InvisibleCharm hide --embed --source-file SOURCEFILEPATH -c COVERFILEPATH.PNG -d HIDDENFILEPATH.PNG

# Extracts hidden data from the source file and write it into the destination file
InvisibleCharm reveal -e -s HIDDENFILEPATH.PNG --dest-file EXTRACTEDFILEPATH
```

![Embed](https://i.imgur.com/GWnCYca.png)

----

- Convert to Image

```shell
# Reads the source file and encrypts its data using 2121 password and convert the data into a PNG image and save it in the destination path
python -m InvisibleCharm h --to-image -s SOURCEFILEPATH -d HIDDENFILEPATH.png --encrypt 2121

# Reads the PNG image and extract the hidden data and decrypt it using 2121 password and write it into the destination path
python -m InvisibleCharm r -i -s HIDDENFILEPATH.png -d DESTINATIONPATH -E 2121 -v
```

![ToImage](https://i.imgur.com/izYKFnZ.png)

----

- Windows Embed

```shell
InvisibleCharm hide --win-embed -s SOURCEFILEPATH --cover-file COVERFILEPATH.png -d HIDDENFILEPATH --compress -v
InvisibleCharm reveal -we -s HIDDENFILEPATH -d DESTINATIONPATH -C
```

![WinEmbed](https://i.imgur.com/MiP2yey.png)

----

- Windows Attribute Change

```shell
InvisibleCharm h --win-attribute -s SOURCEFILEPATH
InvisibleCharm r -wa -s SOURCEFILEPATH
```

![WinAttrib](https://i.imgur.com/UiKAaKy.gif)

About
-----
Author: CodeWriter21 (Mehrad Pooryoussof)

GitHub: [MPCodeWriter21](https://github.com/MPCodeWriter21)

Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

Aparat Channel: [CodeWriter21](https://www.aparat.com/CodeWriter21)
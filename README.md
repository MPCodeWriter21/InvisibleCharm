# InvisibleCharm

**InvisibleCharm** is a python script that allows you to hide your files.

## Installation

In order to use this script you'll need to install some packages and Python libraries.

### Installing Python

Linux:
```sh
apt-get install python
```
Windows:
> Get the latest version from [python.org](https://www.python.org)

### Installing pip

Download the get-pip Python file [get-pip.py](https://bootstrap.pypa.io/get-pip.py) then run it:
```sh
python get-pip.py
```
### Installing required libraries with pip

### Automatically
You can enter command bellow or install libraries manually
```sh
pip3 install -r requirements.txt
```
### Manually

#### colorama
We use [*colorama*](https://github.com/tartley/colorama) library to write colorful texts in windows console.
```sh
pip3 install colorama
```
#### python-magic
We use [*python-magic*](https://github.com/ahupp/python-magic#installation) to check compatible file types for embedding.
```sh
pip install python-magic
```
Windows:
```sh
pip install python-magic-bin
```
#### PyCryptodome
We use [*PyCryptodome*](https://github.com/Legrandin/pycryptodome) for encryption.
```sh
pip install pycryptodome
```
## Usage
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
### Example
- Embed
```sh
# Embeds the source file and the cover file into the destination file.
python main.py Hide --embed --source-file SOURCEFILEPATH -c COVERFILEPATH -d DESTINATIONPATH

# Extracts hidden data from the source file and write it into the destination file
python main.py Reveal -e -s SOURCEFILEPATH --dest-file DESTINATIONPATH
```
- Convert to Image
```sh
# Reads the source file and encrypts its data using 2121 password and convert the data into a PNG image and save it in the destination path
python main.py Hide --to-image -s SOURCEFILEPATH -d DESTINATIONPATH.png --encrypt 2121

# Reads the PNG image and extract the hidden data and decrypt it using 2121 password and write it into the destination path
python main.py Reveal -i -s SOURCEFILEPATH.png -d DESTINATIONPATH -e 2121
```
- Windows Embed
```sh
python main.py Hide --win-embed -s SOURCEFILEPATH --cover-file COVERFILEPATH -d DESTINATIONPATH --compress
python main.py Reveal -we -s SOURCEFILEPATH -d DESTINATIONPATH -C
```
- Windows Attribute Change
```sh
python main.py Hide --win-attribute -s SOURCEFILEPATH
python main.py Reveal -wa -s SOURCEFILEPATH
```

## About

My Telegram: [@MehradP21](https://t.me/MehradP21)

My Telegram Channel: [@CodeWriter21](https://t.me/CodeWriter21)

My Blog: [CodeWriter21.blog.ir](http://CodeWriter21.blog.ir)

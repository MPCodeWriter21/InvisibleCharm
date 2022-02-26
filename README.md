InvisibleCharm
=====

InvisibleCharm is a python script that allows you to hide your files.

Requirements
------------

- [Python 3.x](https://Python.org)
- [Microsoft Visual C++ 14.0 or greater](https://visualstudio.microsoft.com/visual-cpp-build-tools/) (For Windows)
- [python3-dev](https://openwrt.org/packages/pkgdata/python3-dev) (For Linux)
- [Cython](https://cython.readthedocs.io/en/latest/src/quickstart/install.html)
- [setuptools](https://pypi.org/project/setuptools/)
- [log21](https://github.com/MPCodeWriter21/log21)
- [pycryptodome](https://pycryptodome.readthedocs.io/en/latest/src/installation.html)
- [Pillow](https://pillow.readthedocs.io/en/latest/installation.html)
- [python-magic](https://pypi.org/project/python-magic/)
- [importlib_resources](https://pypi.org/project/importlib-resources/)

*Note: You might need to install some of the requirements manually.*

Install InvisibleCharm
----------------------

To install **InvisibleCharm**, you can simply use the `pip install InvisibleCharm` command:

```commandline
python -m pip install InvisibleCharm
```

Or you can clone [the repository](https://github.com/MPCodeWriter21/InvisibleCharm) and run:

```commandline
git clone https://github.com/MPCodeWriter21/InvisibleCharm
cd InvisibleCharm
```

```commandline
python setup.py install
```

Usage
-----

```
usage: InvisibleCharm [-h] [--ntfs-embed] [--win-attribute] [--embed] [--to-image] [--image-mode {
                      3, 4 }] --source-file SOURCE [--cover-file COVER] [--dest-file DESTINATION]
                      [--delete-source] [--compress] [--encrypt-aes] [--encrypt-aes-pass
                      AES_ENCRYPTION_PASS] [--encrypt-rsa RSA_ENCRYPTION_KEY]
                      [--rsa-key-passphrase RSA_KEY_PASS] [--verbose] [--quiet]
                      { hide, reveal, h, r }

positional arguments:
  { hide, reveal, h, r }
                        modes: hide, reveal

options:
  -h, --help
                        show this help message and exit
  --ntfs-embed, -we
                        Embed files invisibly (Only works on NTFS file system)
  --win-attribute, -wa
                        Change windows attributes to hide file
  --embed, -e
  --to-image, -i
                        Converts a file into a png image
  --image-mode { 3, 4 }, -I { 3, 4 }
                        Sets output image mode. Valid values: 3:RGB, 4:ARGB
  --source-file SOURCE, -s SOURCE
                        Sets the path of SOURCE file
  --cover-file COVER, -c COVER
                        Sets the path of COVER file
  --dest-file DESTINATION, -d DESTINATION, -o DESTINATION
                        Sets the path of DESTINATION file
  --delete-source, -D
                        Deletes source file
  --compress, -C
  --encrypt-aes, -aes
                        Enables AES encryption - Asks for an ENCRYPTION_PASSword
  --encrypt-aes-pass AES_ENCRYPTION_PASS, -aes-pass AES_ENCRYPTION_PASS
                        Enables AES encryption - Needs an ENCRYPTION_PASSword
  --encrypt-rsa RSA_ENCRYPTION_KEY, -rsa RSA_ENCRYPTION_KEY
                        Enables RSA encryption - Needs a path to a RSA private/public key
  --rsa-key-passphrase RSA_KEY_PASS, -rsa-pass RSA_KEY_PASS
                        A passphrase to decrypt the input RSA private key.
  --verbose, -v
                        Verbose mode
  --quiet, -q
                        Quiet mode
```

Changes
-------

### 2.4.1

Added auto name generation for output files

[Full Changelog](CHANGELOG.md)

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

Donate
------

If you like this project, please [donate to me](DONATE.md) 8D!
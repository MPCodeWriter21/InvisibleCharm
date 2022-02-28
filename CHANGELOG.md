CHANGELOG
=========

### 2.4.2

Encryption for auto generated names

### 2.4.1

Added auto name generation for output files

### 2.4.0

Added RSA encryption support

### 2.3.0

Some exceptions handled and some comments added to the files.

### 2.2.0

`to_image` and `from_image` renamed to `to_image_file` and `from_image_file`. New `to_image` and `from_image` functions
use bytes and PIL.Image as input and output.

`embed` and `extract` renamed to `embed_file` and `extract_file`. New `to_image` and `from_image` functions use bytes as
input and output.

### 2.1.4

`MANIFEST.in` added.

### 2.1.1 - 2.1.3

Auto release fixed.

### 2.1.0

Using `Cython`, increased the speed of converting a file to an image and extracting the file from the image.
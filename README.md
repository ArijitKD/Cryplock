# Cryplock
Cryplock is a command line encryption/decryption utility implemented using Python Fernet, available for use under the terms of the MIT License.

# How to use:
Download the script ```cryplock.py``` and run it using ```python3 cryplock.py```. Use the ```-help``` option to get acquainted with the available options. Cryplock has currently only been tested on Linux Ubuntu 23.10 AMD64.

# Known issues:
* Cryplock may fail to encrypt files over 1 GB.
* Cryplock will ignore encryption of files in sub-directories.

# TODO:
* Test Cryplock on various other operating systems.
* Implement large file encryption/decryption support.
* Enable Cryplock to encrypt/decrypt files recursively in sub-directories.

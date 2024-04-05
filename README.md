# Cryplock
Cryplock is a command line encryption/decryption utility implemented using Python Fernet, available for use under the terms of the MIT License.

# How to use:
Download the script ```cryplock.py``` and run it using ```python3 cryplock.py```. Use the ```-help``` option to get acquainted with the available options. Cryplock has currently only been tested on Linux Ubuntu 23.10 AMD64. Cryptography module is required for running Cryplock. If you do not have the cryptography module, install it first. For Linux distros using ```apt-get```, you can install it by running ```sudo apt-get install python3-cryptography``` in the terminal. For Windows, you can install it using ```<path-to-pip>\pip.exe install cryptography``` or simply ```pip install cryptography``` if pip was added to %PATH%.

# Known issues:
* Cryplock may fail to encrypt files over 1 GB.
* Cryplock will ignore encryption of files in sub-directories.

# TODO:
* Test Cryplock on various other operating systems.
* Implement large file encryption/decryption support.
* Enable Cryplock to encrypt/decrypt files recursively in sub-directories.

# mspw-pdf

Multisignature paper wallet creator which outputs a pdf..

Simply copy the .py file and a suitable background picture to your computer and run with python.

You will need to install the following modules for python: pybitcointools, PIL, fpdf and qrcode, like so:
sudo pip install bitcoin
etc..

The script simply asks for and m of n combination (n is total number of keys involved in creating the multisignature
bitcoin address, m is the number of keys required to spend the funds). The script supports up to an n of 12. Keys
can be randomly generated or provided by the user (or a combination of the two).

The script then creates an A4 pdf containing the details of m-of-n, the multisignature bitcoin address and qr code, 
all private keys and qr codes, and the multisignature script. PDF allows the script to be copy and pasted easily.

Example output is contained in the mspw.pdf file here on github.

Todo: 
1) minor formatting error if n > 10 as goes onto third page.
2) creating separate pages for each multi signature private key
3) allowing bip38 functionality for printed private keys..(m of n with bip38 encrypted private keys used)
4) finish a spending script that comes with it..:)

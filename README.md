# Checking a stego container in an image (LSB)

## Description

Checking the stego container in the image is carried out using the method of forming an image of the same dimension as the original one. Bitwise verification of each pixel of the image in the split channels (R, G, B) is performed. The check is performed on the least significant bit. If the bit is equal to one, the image pixel is filled with an arbitrary color, for example, black.

Thus, noise is generated on each channel of the image. If there is a stego container in the image, the encrypted areas will be visually highlighted in one or several channels. The observer will be able to visually identify the distinctive features of the stego container on the image - uneven areas of overlapping noise.

## Install requirements

```python
pip3 install -r requirements.txt
```
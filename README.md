## Image Classifier
Docker based Python tool for classifying pictures based on the average color value.

### Usage

* Launch the app with command 
   - ```make``` for error level logging
   - ``make build-verbose`` for info level logging

 * After the app is running, you can add images (or folders with images) into the system with command 
```docker cp <PATH> module_parser:/images/unclassified/```

* PATH can be path for an exact image or folder (with sub-folders) of images.
Unsupported image formats or images without extension will be ignored.

* To check contents of classified files folder, you can use
``docker exec -it module_parser ls -LR /images/classified``

* Run the tests with command ```make test```
* Remove app containers, images and volume ```make clean```

### Requirements
  - Docker 19.03.6 and up
  - Docker-compose 1.27 and up

### Overview

Image classifier uses Docker, NATs messaging system and OpenCV to process images, determine the average color using
numpy and then classify it in a folder with given color (16 base Web colors).

Images are stored in a volume, which is attached to all 3 modules.
This volume has given hierarchy:
```
-───unclassified
│   │   img1.png
|   |   ...
│   └───subfolder-with-images
│       │   img10.jpg
│       │   ...
│   
└───classified
    └───red
        │   red-image.png
        │   ...
```
 After the image is classified, it is moved into correct directory 
without changing its name.
### Supported image types
 * jpg, jpeg
 * png
 * bmp
 * tiff, tif
 
 ### Communication
 There are 3 main modules participating in the image classification process
 1. Parser 
    * scans the unclassified folder for new images
    * if a new image is found, message is sent with path to image
    using NATs
 2. Image handler
    * Subscribes to parser's messages
    * After a new message is received, opens image with OpenCV and calculates
    average color using numpy
    * Sends color information and file path using NATs
 3. Classifier
    * Subscribers to image handler's messages
    * After a new message is received, finds the exact or closest 
    Web color out of 16 standard colors and moves the image into a folder
  
 ### Color classification
 If the average color does not fit any of the 16 standard Web colors,
 a closest Web color is determined by calculating Euclidean distance
 in the RGB space where each of 16 colors is compared to the average
 color and then smallest distance is chosen.
 
  
  ### Example usage
1. ``make`` 
2. ``docker cp ~/Downloads/images/ module_parser:/images/unclassified/``
3. ``docker exec -it module_parser ls -LR /images/classified``

And the result is:
```
/images/classified:
black  blue  lime  red	silver	white

/images/classified/black:
black_bmp.bmp

/images/classified/blue:
blue_jpeg.jpeg

/images/classified/lime:
green_jpg.jpg

/images/classified/red:
red_png.png

/images/classified/silver:
grey_tif.tif

/images/classified/white:
white_tiff.tiff

```
FROM schovancova/image-classifier:1.0
ADD modules/image_handler.py /
ADD modules/constants.py /
CMD ["python", "image_handler.py"]
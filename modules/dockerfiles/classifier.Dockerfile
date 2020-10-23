FROM schovancova/image-classifier:1.0
ADD modules/classifier.py /
ADD modules/constants.py /
CMD ["python", "classifier.py"]
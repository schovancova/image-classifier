FROM schovancova/image-classifier:1.0
ADD modules/parser.py /
ADD modules/constants.py /
CMD ["python", "parser.py"]
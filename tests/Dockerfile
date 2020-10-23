FROM schovancova/image-classifier:1.0
WORKDIR /image-classifier
ENV PYTHONPATH "${PYTHONPATH}:/image-classifier/modules"
RUN pip install --no-cache-dir Pillow
COPY tests/ ./tests
COPY modules/ ./modules
COPY Makefile ./Makefile
RUN python -m unittest discover -p '*.py' -v

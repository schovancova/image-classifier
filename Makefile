APP_NAME = image-classifier

build:
	export LOG_LEVEL=ERROR; docker-compose up

build-verbose:
	export LOG_LEVEL=INFO; docker-compose up

test:
	docker build -t $(APP_NAME):test -f tests/Dockerfile .
	docker image rm $(APP_NAME):test

clean:
	docker-compose rm -f
	docker image rm $(APP_NAME)_parser $(APP_NAME)_image_handler $(APP_NAME)_classifier
	docker volume rm $(APP_NAME)_images


.PHONY: build
build:
	docker build ./django_image_gallery -f django_image_gallery/Dockerfile -t dig

.PHONY: start
start:
	docker run -it -p 8000:8000 dig

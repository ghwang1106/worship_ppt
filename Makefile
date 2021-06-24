.PHONY: build
build:
	docker-compose up --build --d

.PHONY deploy
deploy: build
	docker-compose push
build:
	docker build -t stockholm .

up:
	docker run -d stockholm

start:
	make build
	make up

stop:
	docker stop ${shell docker ps -qa}

purge:
	docker rm $(shell docker ps -qa)

re:
	make stop
	make purge
	make build
	make up
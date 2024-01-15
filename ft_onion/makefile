build:
	docker build -t onion .

up:
	docker run -d -p 80:80 -p 4242:4242 onion

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
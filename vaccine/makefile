build:
	docker pull vulnerables/web-dvwa

up:
	docker run --rm -it -p 80:80 vulnerables/web-dvwa

all:
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
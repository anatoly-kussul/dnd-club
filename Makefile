build:
	docker build -f docker/Dockerfile -t dnd-club-env:latest .

run:
	docker-compose -f docker/docker-compose.yml up

run_prod:
	docker-compose -f docker/docker-compose.yml up -d

logs:
	docker-compose -f docker/docker-compose.yml logs -f

stop:
	docker-compose -f docker/docker-compose.yml stop

bash:
	docker run -it -v $(shell pwd):/app dnd-club-env:latest bash

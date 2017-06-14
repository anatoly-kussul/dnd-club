build:
	docker build -f docker/Dockerfile -t dnd-club-env:latest .

run:
	docker run -i -p 8080:8080 -v $(shell pwd):/app dnd-club-env:latest python -m dnd_club.main

bash:
	docker run -it -v $(shell pwd):/app dnd-club-env:latest bash

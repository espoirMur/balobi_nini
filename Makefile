.PHONY: deploy logs

deploy:
	# copy the ssh key to the droplet
	docker-compose -f docker-compose-prod.yml up -d --build
logs-worker:
	docker-compose -f docker-compose-prod.yml logs worker

build:
	docker build -t assistent_bot_image .
run:
	docker run -it -d --env-file .env --restart=unless-stopped --name assistent_bot assistent_bot_image
stop:
	docker stop assistent_bot
attach:
	docker attach assistent_bot
dell:
	docker rm assistent_bot
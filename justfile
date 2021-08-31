build:
	cd ./fiesta-front && ng build

build-prod:
	cd fiesta-front && ng build --prod

run-back:
	#!/bin/zsh
	source activate fiesta
	cd ./fiesta-back && gunicorn -b 0.0.0.0:5000 -k eventlet api:app -D

kill-back:
	pkill -9 gunicorn

test-back: run-back && kill-back
	#!/bin/zsh
	sleep 2
	source activate fiesta
	cd ./fiesta-back && pytest -s
run: run-back run-front 
	echo "Front and back launched."

terminate: kill-front kill-back 
	echo "Front and back terminated."

### Frontend ###

run-front:
	cd fiesta-front && ng serve &

kill-front:
	kill -9 $(pgrep "ng serve")

build-front:
	cd fiesta-front && ng build

build-prod-front:
	cd fiesta-front && ng build --prod

### Backend ###

run-back:
	#!/bin/zsh
	cd fiesta-back && gunicorn -b 0.0.0.0:5000 -k eventlet api:app -D

kill-back:
	pkill -9 gunicorn

restart-back: kill-back && run-back
	echo "Backend restarted."

test-back: run-back && kill-back
	#!/bin/zsh
	sleep 2
	cd fiesta-back && pytest -s
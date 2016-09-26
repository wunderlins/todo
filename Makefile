.PHONY:

bower:
	cd www; bower install

www-start:
	./bin/serve.sh &

www-stop:
	./bin/stop.sh &



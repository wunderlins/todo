.PHONY:

bower:
	cd www; bower install

pip:
	pip install --ignore-installed -t lib/site-packages zodb hexdump

www-start:
	./bin/serve.sh &

www-stop:
	./bin/stop.sh &

install: bower pip

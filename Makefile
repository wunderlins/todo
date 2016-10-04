.PHONY:

bower:
	cd www; bower install

pip:
	pip install --ignore-installed -t lib/site-packages zodb zope.interface zc.lockfile Flask
	touch lib/site-packages/zope/__init__.py
	touch lib/site-packages/zc/__init__.py
	touch lib/site-packages/__init__.py

www-start:
	./bin/serve.sh &

www-stop:
	./bin/stop.sh &

dep: bower pip


test:
	python -m unittest discover -s test/ -p 'test_*.py'

local_install:
	python setup.py sdist
	pip install dist/service-request-helper-1.0.0.tar.gz
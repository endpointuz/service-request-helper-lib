
test:
	python -m unittest discover -s test/ -p 'test_*.py'

local_install:
	python setup.py sdist
	pip install dist/service-request-helper-1.0.0.tar.gz

build:
	rm -rf build/*
	rm -rf dist/*
	python setup.py sdist bdist_wheel

load_to_pypi:
	twine upload dist/*
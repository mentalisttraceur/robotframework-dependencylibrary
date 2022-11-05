default:
	python3 setup.py sdist bdist_wheel --universal

clean:
	rm -rf __pycache__ build *.egg-info dist
	rm -f *.py[oc] MANIFEST *.html *.xml

test:
	PYTHONPATH=. robot README.rst

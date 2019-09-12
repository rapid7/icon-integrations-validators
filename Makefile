packagedeps:
	python3 -m pip install --user --upgrade setuptools wheel twine

package:
	rm -rf dist/
	python3 setup.py sdist bdist_wheel

disttest: package
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

distprod: package
	python3 -m twine upload dist/*
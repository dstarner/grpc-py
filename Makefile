.PHONY: deploy
deploy:
	python setup.py bdist_wheel
	twine upload dist/*  --skip-existing

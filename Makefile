# Simple makefile for wulftp utils

lint:
	python -m py_compile *.py
	flake8 .
	mypy .

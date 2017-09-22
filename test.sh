#!/bin/bash

py.test tests --doctest-modules --pep8 -v --cov-report term-missing --cov=pyarxiv

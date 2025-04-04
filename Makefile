# -*- Makefile -*-
SHELL = /bin/sh

.PHONY: export install build serve

export:
	rm -rf ./jin-11ty-template/posts/*
	rm -rf ./jin-11ty-template/thoughts/*
	mkdir -p ./jin-11ty-template/posts/en
	mkdir -p ./jin-11ty-template/posts/zh
	mkdir -p ./jin-11ty-template/thoughts/en
	mkdir -p ./jin-11ty-template/thoughts/zh
	uv run notes-publish.py ./jin-11ty-template/posts posts
	uv run notes-publish.py ./jin-11ty-template/thoughts thoughts
install:
	cd ./jin-11ty-template; npm install;
build:
	cd ./jin-11ty-template; npx @11ty/eleventy
serve:
	cd ./jin-11ty-template; npx @11ty/eleventy --serve

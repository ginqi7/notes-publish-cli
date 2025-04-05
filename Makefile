# -*- Makefile -*-
SHELL = /bin/sh

.PHONY: export install build serve

clean:
	rm -rf ./jin-11ty-template/posts/*
	rm -rf ./jin-11ty-template/thoughts/*
	rm -rf ./jin-11ty-template/_site/*
	mkdir -p ./jin-11ty-template/posts/en
	mkdir -p ./jin-11ty-template/posts/zh
	mkdir -p ./jin-11ty-template/thoughts/en
	mkdir -p ./jin-11ty-template/thoughts/zh
	echo '{"layout" : "post-layout", "permalink" : "/{{ page.fileSlug }}/", "lang" : {"type" : "en", "href" : "/"}}' > ./jin-11ty-template/posts/en/en.json
	echo '{"layout" : "post-layout", "permalink" : "/zh/{{ page.fileSlug }}/", "lang" : {"type" : "zh", "href" : "/zh/"}}' > ./jin-11ty-template/posts/zh/zh.json
export:
	uv run notes-publish.py ./jin-11ty-template/posts posts
	uv run notes-publish.py ./jin-11ty-template/thoughts thoughts
install:
	cd ./jin-11ty-template; npm install;
build:
	cd ./jin-11ty-template; npx @11ty/eleventy
serve:
	cd ./jin-11ty-template; npx @11ty/eleventy --serve

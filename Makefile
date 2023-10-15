.PHONY: submission

submission:
	rm -rf submission
	mkdir submission
	cp README.md submission/README.md
	cp -r src submission
	gcc -o submission/libtglang.so src/tglang.c -shared
	zip -r submission.zip submission
	gcc -o submission/test src/tglang.c src/test.c

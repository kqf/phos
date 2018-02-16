paths.log:
	./io.sh >> paths.log
	echo "\n" >> paths.log

download: paths.log
	download

upload: paths.log
	upload

clean:
	rm paths.log
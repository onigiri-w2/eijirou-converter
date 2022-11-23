init:
	mkdir -p output && mkdir -p input

download_sample:
	curl -OL http://www.eijiro.jp/eijiro-sample-1448.zip && \
	unzip eijiro-sample-1448.zip -d input && \
	rm eijiro-sample-1448.zip

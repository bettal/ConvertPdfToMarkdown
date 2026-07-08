.PHONY: build clean bump-major bump-minor bump-patch

build: bump-patch
	dpkg-buildpackage -b -uc -us
	mkdir -p dist
	mv ../convert-pdf-to-markdown_*.deb ../convert-pdf-to-markdown_*.buildinfo ../convert-pdf-to-markdown_*.changes dist/ 2>/dev/null || true

clean:
	rm -f ../convert-pdf-to-markdown_* 2>/dev/null || true
	rm -rf dist/ .pybuild/ *.egg-info/ debian/convert-pdf-to-markdown/ 2>/dev/null || true

bump-patch:
	./debian/bump-version.sh patch

bump-minor:
	./debian/bump-version.sh minor

bump-major:
	./debian/bump-version.sh major

release: build

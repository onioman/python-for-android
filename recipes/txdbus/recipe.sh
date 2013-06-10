#!/bin/bash

# version of your package
VERSION_txdbus=1.0.2
# dependencies of this recipe
DEPS_txdbus=(twisted)
# url of the package
URL_txdbus=https://pypi.python.org/packages/source/t/txdbus/txdbus-$VERSION_txdbus.tar.gz
# md5 of the package
MD5_txdbus=3e24f29bdba2e8bdf054fca95d54abda
# default build path
BUILD_txdbus=$BUILD_PATH/txdbus/$(get_directory $URL_txdbus)
# default recipe path
RECIPE_txdbus=$RECIPES_PATH/txdbus

# function called for preparing source code if needed
# (you can apply patch etc here.)
function prebuild_txdbus() {
	true
}

# function called to build the source code
function build_txdbus() {
	if [ -d "$BUILD_PATH/python-install/lib/python2.7/site-packages/txdbus" ]; then
		return
	fi
	cd $BUILD_txdbus
	push_arm
	export PYTHONPATH=$BUILD_PATH/hostpython/Python-2.7.2/Lib/site-packages
        try $BUILD_PATH/hostpython/Python-2.7.2/hostpython setup.py install -O2 --root=$BUILD_PATH/python-install --install-lib=lib/python2.7/site-packages
	pop_arm
}

# function called after all the compile have been done
function postbuild_txdbus() {
	true
}

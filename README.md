# gflags

[Conan.io](https://conan.io) package for Google's GFlags library

## Build packages

Download conan client from [Conan.io](https://conan.io) and run:

    $ python build.py

## Reuse the packages

### Basic setup

    $ conan install gflags/master@sunside/snapshot

### Project setup

If you handle multiple dependencies in your project is better to add a *conanfile.txt*

    [requires]
    gflags/master@sunside/snapshot

    [options]
    gtest:shared=true # false

    [generators]
    txt
    cmake

Complete the installation of requirements for your project running:

    conan install .

Project setup installs the library (and all his dependencies) and generates the files
*conanbuildinfo.txt* and *conanbuildinfo.cmake* with all the paths and variables that
you need to link with your dependencies.

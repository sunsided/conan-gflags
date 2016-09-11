from conans import ConanFile
import os
from conans.tools import download
from conans.tools import unzip
from conans import CMake

class GFlagsConan(ConanFile):
    name = "gflags"
    version = "master"
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "nothreads": [True, False]}
    default_options = "shared=True", "nothreads=False"
    exports="CMakeLists.txt", "FindGflags.cmake", "change_dylib_names.sh"
    url="https://github.com/sunsided/conan-gflags"
    license="https://github.com/gflags/gflags/blob/master/COPYING.txt"
    zip_folder_name = "gflags-%s" % version

    def source(self):
        zip_name = "%s.zip" % self.version
        url = "https://github.com/gflags/gflags/archive/%s" % zip_name
        download(url, zip_name)
        unzip(zip_name)
        os.unlink(zip_name)

    def build(self):
        cmake = CMake(self.settings)
        if self.settings.os == "Windows":
            self.run("IF not exist _build mkdir _build")
        else:
            self.run("mkdir _build")
        cd_build = "cd _build"
        shared = "-DBUILD_SHARED_LIBS=1" if self.options.shared else ""
        nothreads = "-DBUILD_gflags_nothreads_LIB=0" if not self.options.nothreads else ""

        self.run("%s && cmake .. %s %s %s" % (cd_build, cmake.command_line, shared, nothreads))
        self.run("%s && cmake --build . %s" % (cd_build, cmake.build_config))

    def package(self):

        if self.settings.os == "Macos" and self.options.shared:
            self.run("bash ./change_dylib_names.sh")

        # Copy findgflags script into project
        self.copy("FindGflags.cmake", ".", ".")

        # Copying headers
        incdir = "_build/%s/include" % self.zip_folder_name
        self.copy(pattern="*.h", dst="include", src=incdir, keep_path=True)

        # Copying static and dynamic libs
        libdir = "_build/lib"
        self.copy(pattern="*.a", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dylib*", dst="lib", src=libdir, keep_path=False)
        self.copy(pattern="*.dll", dst="bin", src=libdir, keep_path=False)

        # Copying binaries
        bindir = "_build/bin"
        self.copy(pattern="*.dll", dst="bin", src=bindir, keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ['gflags']

from conans.model.conan_file import ConanFile
from conans import CMake
import os

#This easily allows to copy the package in other user or channel
channel = os.getenv("CONAN_CHANNEL", "snapshot")
username = os.getenv("CONAN_USERNAME", "sunside")

class DefaultNameConan(ConanFile):
    name = "DefaultName"
    version = "0.1"
    settings = "os", "compiler", "arch", "build_type"
    generators = "cmake"
    requires = "gflags/master@%s/%s" % (username, channel)

    def build(self):
        cmake = CMake(self.settings)
        self.run('cmake %s %s' % (self.conanfile_directory, cmake.command_line))
        self.run("cmake --build . %s" % cmake.build_config)

    def imports(self):
        self.copy(pattern="*.dll", dst="bin", src="bin")
        self.copy(pattern="*.dylib", dst="bin", src="lib")

    def test(self):
        self.run("cd bin && .%smytest" % os.sep)

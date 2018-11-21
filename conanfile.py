#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools,CMake
import os
from conanos.build import config_scheme

class NettleConan(ConanFile):
    name = "nettle"
    version = "3.4"
    url = "https://github.com/DEGoodmanWilson/conan-nettle"
    description = "The Nettle and Hogweed low-level cryptographic libraries"
    license = "https://www.lysator.liu.se/~nisse/nettle/nettle.html#Copyright"
    exports_sources = ["CMakeLists.txt",'cmake/*']
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    requires = 'gmp/6.1.2@conanos/stable'

    source_subfolder = '%s-%s'%(name,version)
    generators = 'cmake'

    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx

        config_scheme(self)



    def source(self):
        source_url = "https://ftp.gnu.org/gnu/nettle"
        tools.get("{0}/nettle-{1}.tar.gz".format(source_url, self.version))
        #extracted_dir = self.name + "-" + self.version
        #os.rename(extracted_dir, "sources")
       
    def autotool_build(self):

        with tools.chdir(self.source_subfolder):
            env_build = AutoToolsBuildEnvironment(self)
            env_build.fpic = True

            config_args = []
            for option_name in self.options.values.fields:
                if(option_name == "shared"):
                    if(getattr(self.options, "shared")):
                        config_args.append("--enable-shared")
                        config_args.append("--disable-static")
                    else:
                        config_args.append("--enable-static")
                        config_args.append("--disable-shared")
                else:
                    activated = getattr(self.options, option_name)
                    if activated:
                        self.output.info("Activated option! %s" % option_name)
                        config_args.append("--%s" % option_name)

            env_build.configure(args=config_args)
            env_build.make()

    def cmake_build(self):
        cmake = CMake(self)
        cmake.configure(build_folder='~build',
        defs={'USE_CONAN_IO':True,
            'NETTLE_PROJECT_DIR':self.source_subfolder,            
            'ENABLE_UNIT_TESTS':'ON'
        })
        cmake.build()
        cmake.test()
        cmake.install()

    def build(self):
        if self.settings.compiler == 'Visual Studio':
            self.cmake_build()
        else:
            self.autotool_build()
    def package(self):
        self.copy(pattern="COPYING*", src="sources")
        self.copy(pattern="*.h", dst="include/nettle", src="sources")
        # self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="sources", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)



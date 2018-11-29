#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools,CMake
import os
from conanos.build import config_scheme,pkgconfig_adaption

def _abspath(folder):
    return os.path.abspath(folder).replace('\\','/')

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

    #_source_folder = '%s-%s'%(name,version)
    generators = 'cmake'
    
    _source_folder    ='_source'
    _pkgconfig_folder ='_pkgconfig'
    _build_folder     ='_build'

    @property
    def is_msvc(self):
        return self.settings.compiler == "Visual Studio"

    @property
    def run_checks(self):
        CONANOS_RUN_CHECKS = os.environ.get('CONANOS_RUN_CHECKS')
        if CONANOS_RUN_CHECKS:
            return self.name in CONANOS_RUN_CHECKS.split()
        return False
		
    def configure(self):
        # Because this is pure C
        del self.settings.compiler.libcxx
        if self.settings.compiler == "Visual Studio":
            del self.options.fPIC
            if self.options.shared:
               raise tools.ConanException("The nettle package cannot be built shared on Visual Studio.")
        
    def requirements(self):
        config_scheme(self)

    def source(self):
        source_url = "https://ftp.gnu.org/gnu/nettle"
        tools.get("{0}/nettle-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_folder)
       
    def autotool_build(self):

        with tools.chdir(self._source_folder):
            env_build = AutoToolsBuildEnvironment(self)
            #env_build.fpic = True

            _args=["--enable-public-key"]            
            if self.options.shared:
                _args.extend(['--enable-shared=yes','--enable-static=no'])
            else:
                _args.extend(['--enable-shared=no','--enable-static=yes'])
            env_build.configure(args=_args,pkg_config_paths=_abspath(self._pkgconfig_folder))
            env_build.make()
            env_build.install()

    def gcc_build(self):
        with tools.chdir(self.source_subfolder):
            with tools.environment_append({
                #'PKG_CONFIG_PATH':'%s/lib/pkgconfig'%(self.deps_cpp_info["gmp"].rootpath),
                #'LD_LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
                'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),       #For generation of libhogweed
                'C_INCLUDE_PATH' : "%s/include"%(self.deps_cpp_info["gmp"].rootpath)  #For generation of libhogweed
                }):
                
                _args = ["--prefix=%s/builddir"%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()) ,
                         "--enable-public-key"]

                if self.options.shared:
                    _args.extend(['--enable-shared=yes','--enable-static=no'])
                else:
                    _args.extend(['--enable-shared=no','--enable-static=yes'])
                
                self.run('./configure %s'%(' '.join(_args)))#space
                self.run('make')
                self.run('make install')

    def cmake_build(self):
        #NETTLE_PROJECT_DIR = _abspath(self._source_folder)
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_folder,
        defs={'USE_CONAN_IO':True,
            'PROJECT_HOME_DIR':_abspath(self._source_folder),
            'ENABLE_TESTS':self.run_checks,           

            'ENABLE_UNIT_TESTS':self.run_checks,
            'NETTLE_PROJECT_DIR':_abspath(self._source_folder),

        })
        cmake.build()
        if self.run_checks:
            cmake.test()
        cmake.install()

    def build(self):
        pkgconfig_adaption(self,_abspath(self._pkgconfig_folder))
        
        if self.is_msvc:
            self.cmake_build()
        else:
            self.autotool_build()
    def package(self):
        return
        self.copy(pattern="COPYING*", src="sources")
        self.copy(pattern="*.h", dst="include/nettle", src="sources")
        self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.so*", dst="lib", src="sources", keep_path=False)
        self.copy(pattern="*.dylib", dst="lib", src="sources", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)



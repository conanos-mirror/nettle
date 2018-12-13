#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools,MSBuild
import os, shutil
from conanos.build import config_scheme

class NettleConan(ConanFile):
    name = "nettle"
    version = "3.4.1"
    release_timestamp = "20181204"
    description = "The Nettle and Hogweed low-level cryptographic libraries"
    url = "https://github.com/conanos/nettle"
    homepage = "http://www.lysator.liu.se/~nisse/nettle/"
    license = "LGPL-3.0+, GPL-2.0+"
    exports = ["COPYINGv3","COPYINGv2"]
    generators = "visual_studio", "gcc"
    settings = "os", "arch", "compiler", "build_type"
    options = { "shared": [True, False], "fPIC": [True, False] }
    default_options = { 'shared': True, 'fPIC': True }


    _source_subfolder = "source_subfolder"
    _build_subfolder = "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        config_scheme(self)
        
    def requirements(self):
        self.requires.add("gmp/6.1.2-5@conanos/stable")

    def source(self):
        url_ = "https://github.com/ShiftMediaProject/nettle/archive/nettle_{version}_release_{timestamp}.tar.gz"
        tools.get(url_.format(version=self.version,timestamp=self.release_timestamp))
        extracted_dir = self.name + "-" + "nettle_%s_release_%s"%(self.version, self.release_timestamp)
        os.rename(extracted_dir, self._source_subfolder)

    #def autotool_build(self):

    #    with tools.chdir(self._source_folder):
    #        env_build = AutoToolsBuildEnvironment(self)
    #        #env_build.fpic = True

    #        _args=["--enable-public-key"]            
    #        if self.options.shared:
    #            _args.extend(['--enable-shared=yes','--enable-static=no'])
    #        else:
    #            _args.extend(['--enable-shared=no','--enable-static=yes'])
    #        env_build.configure(args=_args,pkg_config_paths=_abspath(self._pkgconfig_folder))
    #        env_build.make()
    #        env_build.install()

    #def gcc_build(self):
    #    with tools.chdir(self.source_subfolder):
    #        with tools.environment_append({
    #            #'PKG_CONFIG_PATH':'%s/lib/pkgconfig'%(self.deps_cpp_info["gmp"].rootpath),
    #            #'LD_LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),
    #            'LIBRARY_PATH' : "%s/lib"%(self.deps_cpp_info["gmp"].rootpath),       #For generation of libhogweed
    #            'C_INCLUDE_PATH' : "%s/include"%(self.deps_cpp_info["gmp"].rootpath)  #For generation of libhogweed
    #            }):
    #            
    #            _args = ["--prefix=%s/builddir"%(os.getcwd()), '--libdir=%s/builddir/lib'%(os.getcwd()) ,
    #                     "--enable-public-key"]

    #            if self.options.shared:
    #                _args.extend(['--enable-shared=yes','--enable-static=no'])
    #            else:
    #                _args.extend(['--enable-shared=no','--enable-static=yes'])
    #            
    #            self.run('./configure %s'%(' '.join(_args)))#space
    #            self.run('make')
    #            self.run('make install')

    #def cmake_build(self):
    #    #NETTLE_PROJECT_DIR = _abspath(self._source_folder)
    #    cmake = CMake(self)
    #    cmake.configure(build_folder=self._build_folder,
    #    defs={'USE_CONAN_IO':True,
    #        'PROJECT_HOME_DIR':_abspath(self._source_folder),
    #        'ENABLE_TESTS':self.run_checks,           

    #        #'ENABLE_UNIT_TESTS':self.run_checks,
    #        #'NETTLE_PROJECT_DIR':_abspath(self._source_folder),

    #    })
    #    cmake.build()
    #    if self.run_checks:
    #        cmake.test()
    #    cmake.install()

    def build(self):
        #pkgconfig_adaption(self,_abspath(self._pkgconfig_folder))
        
        #if self.is_msvc:
        #    self.cmake_build()
        #else:
        #    self.autotool_build()
        if self.settings.os == "Windows":
            with tools.chdir(os.path.join(self._source_subfolder,"SMP")):
                msbuild = MSBuild(self)
                build_type = str(self.settings.build_type) + ("DLL" if self.options.shared else "")
                msbuild.build("libnettle.sln",upgrade_project=True, build_type=build_type)

    def package(self):
        #return
        #self.copy(pattern="COPYING*", src="sources")
        #self.copy(pattern="*.h", dst="include/nettle", src="sources")
        #self.copy(pattern="*.dll", dst="bin", src="bin", keep_path=False)
        #self.copy(pattern="*.lib", dst="lib", src="sources", keep_path=False)
        #self.copy(pattern="*.a", dst="lib", src="sources", keep_path=False)
        #self.copy(pattern="*.so*", dst="lib", src="sources", keep_path=False)
        #self.copy(pattern="*.dylib", dst="lib", src="sources", keep_path=False)
        if self.settings.os == "Windows":
            platform = {'x86': 'x86','x86_64': 'x64'}
            rplatform = platform.get(str(self.settings.arch))
            self.copy("*", dst=os.path.join(self.package_folder,"include"), src=os.path.join(self.build_folder,"..", "msvc","include"))
            for i in ["lib","bin"]:
                self.copy("*", dst=os.path.join(self.package_folder,i), src=os.path.join(self.build_folder,"..","msvc",i,rplatform))
            self.copy("*", dst=os.path.join(self.package_folder,"licenses"), src=os.path.join(self.build_folder,"..", "msvc","licenses"))

            tools.mkdir(os.path.join(self.package_folder,"lib","pkgconfig"))
            for pc in ["nettle", "hogweed"]:
                shutil.copyfile(os.path.join(self.build_folder,self._source_subfolder, pc + ".pc.in"),
                                os.path.join(self.package_folder,"lib","pkgconfig", pc + ".pc"))
                replacements = {
                    "@prefix@"      : self.package_folder,
                    "@exec_prefix@" : "${prefix}/bin",
                    "@libdir@"      : "${prefix}/lib",
                    "@includedir@"  : "${prefix}/include",
                    "@PACKAGE_VERSION@" : self.version
                }
                if pc == "hogweed":
                    replacements.update({
                        "@IF_NOT_SHARED@" : "",
                        "@IF_SHARED@" : "",
                        "@LIBS@" : ""
                    })
                for s, r in replacements.items():
                    tools.replace_in_file(os.path.join(self.package_folder,"lib","pkgconfig", pc +".pc"),s,r)

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)



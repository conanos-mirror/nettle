from conans import ConanFile, CMake, tools
from shutil import copyfile
import os

class NettleConan(ConanFile):
    name = "nettle"
    version = "3.4"
    description = "a low-level cryptographic library"
    url = "https://github.com/conanos/nettle"
    homepage = "http://www.lysator.liu.se/~nisse/nettle/"
    license = "LGPLv2_1Plus"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    generators = "cmake"
    #For generation of libhogweed
    requires = "gmp/6.1.2@conanos/dev"

    source_subfolder = "source_subfolder"

    def source(self):
        tools.get('http://ftp.gnu.org/gnu/{0}/{0}-{1}.tar.gz'.format(self.name, self.version))
        extracted_dir = "%s-%s"%(self.name, self.version)
        os.rename(extracted_dir, self.source_subfolder)

    def build(self):
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

    def package(self):
        if tools.os_info.is_linux:
            with tools.chdir(self.source_subfolder):
                self.copy("*", src="%s/builddir"%(os.getcwd()))

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)


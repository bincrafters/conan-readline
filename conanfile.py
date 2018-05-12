#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os


class ReadLineConan(ConanFile):
    name = "readline"
    version = "7.0"
    description = "A set of functions for use by applications that allow users to edit command lines as they are typed in"
    url = "https://github.com/bincrafters/conan-readline"
    homepage = "https://tiswww.case.edu/php/chet/readline/rltop.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPL-3"
    exports = ["LICENSE.md"]
    exports_sources = ["readline_mingw.patch"]
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = "shared=False", "fPIC=True"
    source_subfolder = "source_subfolder"
    autotools = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            pass
            # TODO (uilian): Log warning about Curses

    def source(self):
        source_url = "https://git.savannah.gnu.org/cgit/readline.git/snapshot/readline"
        tools.get("{0}-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self.source_subfolder)
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            tools.patch(base_path=self.source_subfolder, patch_file="readline_mingw.patch")

    def system_requirements(self):
        if tools.os_info.linux_distro == "ubuntu":
            arch = {'x86': 'i386', 'x86_64': 'amd64'}
            installer = tools.SystemPackageTool()
            libncurses = 'libncurses5-dev:%s' % arch[str(self.settings.arch)]
            installer.install(libncurses)

    def configure_autotools(self):
        if not self.autotools:
            configure_args = ['--enable-static', '--disable-shared']
            if self.options.shared:
                configure_args = ['--enable-shared', '--disable-static']
            configure_args.append('--with-curses')

            self.autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            if self.settings.os != "Windows":
                self.autotools.fpic = self.options.fPIC
            self.autotools.configure(args=configure_args)
        return self.autotools

    def build(self):
        with tools.chdir(self.source_subfolder):
            autotools = self.configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self.source_subfolder)
        with tools.chdir(self.source_subfolder):
            autotools = self.configure_autotools()
            autotools.make(["install"])

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('termcap')
        elif self.settings.os == "Windows" and self.settings.compiler == "gcc":
            self.cpp_info.libs.append('curses')

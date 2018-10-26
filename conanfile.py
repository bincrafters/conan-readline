#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from conans import ConanFile, AutoToolsBuildEnvironment, tools


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
    default_options = {"shared": False, "fPIC": True}
    _source_subfolder = "source_subfolder"
    _autotools = None

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC
        if self.settings.os == "Macos":
            del self.options.shared

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://git.savannah.gnu.org/cgit/readline.git/snapshot/readline"
        tools.get("{0}-{1}.tar.gz".format(source_url, self.version))
        extracted_dir = self.name + "-" + self.version
        os.rename(extracted_dir, self._source_subfolder)

    def system_requirements(self):
        self.output.warn("Readline requires ncurses installed")
        if tools.os_info.linux_distro == "ubuntu":
            arch = {'x86': 'i386', 'x86_64': 'amd64'}
            installer = tools.SystemPackageTool()
            libncurses = 'libncurses5-dev:%s' % arch[str(self.settings.arch)]
            installer.install(libncurses)

    def _configure_autotools(self):
        if not self._autotools:
            configure_args = ['--enable-static', '--disable-shared']
            if self.settings.os == "Macos" or self.options.shared:
                configure_args = ['--enable-shared', '--disable-static']

            self._autotools = AutoToolsBuildEnvironment(self, win_bash=tools.os_info.is_windows)
            self._autotools.configure(args=configure_args)
        return self._autotools

    def build(self):
        if self.settings.os == "Windows" and self.settings.compiler == "gcc":
            tools.patch(base_path=self._source_subfolder, patch_file="readline_mingw.patch")
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=self._source_subfolder)
        with tools.chdir(self._source_subfolder):
            autotools = self._configure_autotools()
            autotools.make(["install"])

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.libs.append('termcap')

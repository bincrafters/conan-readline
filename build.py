#!/usr/bin/env python
# -*- coding: utf-8 -*-


import platform
from bincrafters import build_template_default

if __name__ == "__main__":

    builder = build_template_default.get_builder()

    if platform.system() == "Darwin":
        filtered_builds = []
        for settings, options, env_vars, build_requires, reference in builder.items:
            if options['readline:shared']:
                filtered_builds.append([settings, {}, env_vars, build_requires])

        builder.builds = filtered_builds
    builder.run()

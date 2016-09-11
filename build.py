from conan.packager import ConanMultiPackager


if __name__ == "__main__":
    builder = ConanMultiPackager(username="sunside", channel="snapshot")
    builder.add_common_builds(shared_option_name="gtest:shared", pure_c=False)

    patched_builds = []
    for settings, options in builder.builds:

        # Selecting the debug runtimes (MTd, MDd) on Windows for Debug builds
        if settings["compiler"] == "Visual Studio" and settings["build_type"] == "Debug":
            if not settings["compiler.runtime"].endswith("d"):
                settings["compiler.runtime"] = settings["compiler.runtime"] + "d"
        patched_builds.append([settings, options])

    builder.builds = patched_builds

    builder.run()


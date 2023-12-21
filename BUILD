# load("@python_dev_deps//:requirements.bzl", test_entry_point = "entry_point")
# load("@rules_python//python/entry_points:py_console_script_binary.bzl", "py_console_script_binary")

package(
    default_visibility = ["//visibility:public"],
)

exports_files(["pytest.ini"])

# filegroup(
#     # gather all the data for pytest binary to work
#     name = "_pytest",
#     srcs = [
#         test_entry_point("pytest"),
#         "//:pytest.ini",
#     ],
# )

# filegroup(
#     name = "_ruff",
#     srcs = [
#         devtools_entry_point("ruff"),
#     ],
# )

filegroup(
    name = "ffmpeg-amd64",
    srcs = glob(["vendor/ffmpeg/amd/**/*"]),
)

filegroup(
    name = "ffmpeg-osx",
    srcs = glob(["vendor/ffmpeg/osx/**/*"]),
)

filegroup(
    name = "youtube-dl",
    srcs = glob(["vendor/youtube-dl/**/*"]),
)

# py_console_script_binary(
#     name = "ruff",
#     pkg = "@python_deps_v1//ruff",
# )

# py_console_script_binary(
#     name = "pytest",
#     pkg = "@python_dev_deps//pytest:pkg",
# )

# alias(
#     name = "pytest",
#     actual = ":_pytest",
# )

# alias(
#     name = "binpytest",
#     actual = test_entry_point("pytest"),
#     tags = ["local"],
# )

# filegroup(
#     name = "_mypy",
#     srcs = [
#         devtools_entry_point("mypy"),
#     ],
# )

# alias(
#     name = "mypy",
#     actual = devtools_entry_point("mypy"),
#     tags = ["local"],
# )

config_setting(
    name = "osx_build",
    constraint_values = [
        ":osx",
    ],
)

constraint_setting(name = "os")

constraint_value(
    name = "osx",
    constraint_setting = "os",
)

constraint_value(
    name = "linux",
    constraint_setting = "os",
)

platform(
    name = "osx_platform",
    constraint_values = [
        ":osx",
    ],
)

# # + select({
# # "//:osx_build": ["vendor/ffmpeg/osx/ffmpeg"],
# # "//conditions:default": ["vendor/ffmpeg/amd/ffmpeg"],
# # }),

# # config_setting(
# #     name = "linux_build",
# #     constraint_values = [
# #         ":white",
# #         ":metamorphic",
# #     ],
# # )

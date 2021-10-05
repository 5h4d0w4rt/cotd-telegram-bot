load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_runtime_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_library(
    name = "helpers",
    srcs = ["helpers.py"],
    deps = [
        requirement("python-telegram-bot"),
        requirement("pillow"),
    ],
)

py_library(
    name = "all",
    srcs = [
        "anti_voice.py",
        "cringelord.py",
        "cringer.py",
        "inliner.py",
        "manet.py",
        "misc.py",
        "motivationv2.py",
        "prospector.py",
        "security.py",
    ],
    deps = [
        requirement("python-telegram-bot"),
        requirement("pillow"),
        requirement("ratelimit"),
        "helpers",
        "//cotd:cacher",
        "//cotd:static",
    ],
)

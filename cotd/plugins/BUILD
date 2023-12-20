load("@rules_python//python:defs.bzl", "py_library")
load("@python_deps//:requirements.bzl", "requirement")

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
        "cringelord.py",
        "cronjobs.py",
        "inliner.py",
        "kandinsky.py",
        "misc.py",
        "motivationv2.py",
        "prospector.py",
        "security.py",
        "webm_to_mp4.py",
        "youtuber.py",
    ],
    data = ["//static:lobster.ttf"],
    deps = [
        requirement("python-telegram-bot"),
        requirement("pillow"),
        requirement("ratelimit"),
        requirement("requests"),
        "helpers",
        "//cotd:cacher",
        "//cotd:static",
    ],
)

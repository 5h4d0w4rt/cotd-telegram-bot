load("@rules_python//python:defs.bzl", "py_binary")
load("@python_workspace_deps//:requirements.bzl", "requirement")

py_library(
    name = "config",
    srcs = ["config.py"],
)

py_library(
    name = "handlers",
    srcs = ["handlers.py"],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        "//static:KEKW.mp4",
        "//static:oldfellow.mp4",
        "//static:smileyOne.webp",
    ],
    deps = [
        requirement("python-telegram-bot"),
        "config",
        "handlers",
    ],
)

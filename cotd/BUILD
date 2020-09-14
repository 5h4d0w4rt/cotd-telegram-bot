load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_workspace_deps//:requirements.bzl", "requirement")

py_library(
    name = "handlers",
    srcs = ["handlers.py"],
)

py_library(
    name = "flags",
    srcs = ["flags.py"],
)

py_library(
    name = "options",
    srcs = ["options.py"],
)

py_library(
    name = "logger",
    srcs = ["logger.py"],
)

py_library(
    name = "updater",
    srcs = ["updater.py"],
)

py_binary(
    name = "main",
    srcs = ["main.py"],
    data = [
        "//static:KEKW.mp4",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
    ],
    deps = [
        requirement("python-telegram-bot"),
        requirement("flask"),
        "flags",
        "handlers",
        "logger",
        "options",
        "updater",
    ],
)
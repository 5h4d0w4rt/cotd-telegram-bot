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
        "//static:smileyOne.webp",
        "//static:starina.mp4",
    ],
    deps = [
        requirement("python-telegram-bot"),
        "config",
        "handlers",
    ],
)

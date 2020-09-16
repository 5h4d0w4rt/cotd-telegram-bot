load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_workspace_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_library(
    name = "handlers",
    srcs = ["handlers.py"],
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
    name = "cotdbot",
    srcs = ["main.py"],
    args = [
        "--mode",
        "token",
        "--log-level",
        "info",
    ],
    data = [
        "//static:KEKW.mp4",
        "//static:cringe-sniff-dog.jpg",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
        "//static:smileyOne512x512.png",
    ],
    main = "main.py",
    deps = [
        requirement("python-telegram-bot"),
        requirement("flask"),
        "handlers",
        "logger",
        "updater",
    ],
)

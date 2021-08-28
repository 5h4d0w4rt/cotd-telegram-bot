load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_workspace_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_library(
    name = "cacher",
    srcs = ["cacher.py"],
)

py_library(
    name = "repository",
    srcs = ["repository.py"],
)

py_library(
    name = "handlers",
    srcs = ["handlers.py"],
    deps = [
        requirement("python-telegram-bot"),
        "cacher",
        "static",
    ],
)

py_library(
    name = "static",
    srcs = ["static.py"],
    data = [
        "//static:KEKW.mp4",
        "//static:cringe-sniff-dog.jpg",
        "//static:stuffy.jpg",
        "//static:journalism.jpg",
        "//static:go_away.mp4",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
        "//static:smileyOne512x512.png",
        "//static:music.jpg",
        "//static:deadinside.jpg",
        "//static:motivator.jpg",
        "//static:lobster.ttf",
    ],
    deps = [
        requirement("python-telegram-bot"),
    ],
)

py_library(
    name = "logger",
    srcs = ["logger.py"],
)

py_library(
    name = "service",
    srcs = ["service.py"],
    data = ["//static:smileyOne512x512.png"],
    deps = [
        requirement("python-telegram-bot"),
    ],
)

py_binary(
    name = "cotdbot",
    srcs = ["main.py"],
    args = [
        "--mode",
        "token",
        "--log-level",
        "debug",
        "--group",
        "-1001061349179",
    ],
    data = [
        "//static:KEKW.mp4",
        "//static:cringe-sniff-dog.jpg",
        "//static:stuffy.jpg",
        "//static:journalism.jpg",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
        "//static:smileyOne512x512.png",
        "//static:music.jpg",
        "//static:deadinside.jpg",
        "//static:motivator.jpg",
        "//static:lobster.ttf",
    ],
    main = "main.py",
    deps = [
        requirement("python-telegram-bot"),
        requirement("flask"),
        "handlers",
        "logger",
        "service",
        "static",
    ],
)

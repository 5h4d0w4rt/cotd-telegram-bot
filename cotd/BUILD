load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_runtime_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_library(
    name = "cacher",
    srcs = ["cacher.py"],
)

py_library(
    name = "storage",
    srcs = ["storage.py"],
)

py_library(
    name = "handlers",
    srcs = ["handlers.py"],
    deps = [
        requirement("python-telegram-bot"),
        requirement("pillow"),
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
        "//static:deadinside.jpg",
        "//static:go_away.mp4",
        "//static:journalism.jpg",
        "//static:lobster.ttf",
        "//static:motivator.jpg",
        "//static:music.jpg",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
        "//static:smileyOne512x512.png",
        "//static:stuffy.jpg",
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
        "storage",
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
        "--version",
        "1.3",
        "--db",
        "-1001530261511",
        "--feature-enable-persistence",
    ],
    data = [
        "//static:KEKW.mp4",
        "//static:cringe-sniff-dog.jpg",
        "//static:deadinside.jpg",
        "//static:journalism.jpg",
        "//static:lobster.ttf",
        "//static:motivator.jpg",
        "//static:music.jpg",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
        "//static:smileyOne512x512.png",
        "//static:stuffy.jpg",
    ],
    main = "main.py",
    deps = [
        requirement("python-telegram-bot"),
        "handlers",
        "logger",
        "service",
        "static",
        "storage",
        "//cotd/plugins:all",
    ],
)

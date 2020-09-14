load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_workspace_deps//:requirements.bzl", "requirement")

py_binary(
    name = "stickerpack",
    srcs = ["sticker-pack-creator.py"],
    data = [
        "//static:KEKW.mp4",
        "//static:ezgif.com-resize.png",
        "//static:oldfellow.mp4",
        "//static:ribnikov.based.mp4",
        "//static:smileyOne.webp",
    ],
    main = "sticker-pack-creator.py",
    deps = [
        requirement("python-telegram-bot"),
        "//cotd:updater",
    ],
)

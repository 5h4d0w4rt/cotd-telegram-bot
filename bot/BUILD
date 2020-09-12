load("@rules_python//python:defs.bzl", "py_binary")
load("@python_workspace_deps//:requirements.bzl", "requirement")

py_binary(
    name = "main",
    srcs = ["main.py"],
    deps = [requirement("python-telegram-bot")],
)

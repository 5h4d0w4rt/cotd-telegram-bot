load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@python_runtime_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_library(
    name = "motivationv2",
    srcs = ["motivationv2.py"],
    deps = [
        requirement("python-telegram-bot"),
        requirement("pillow"),
        requirement("ratelimit"),
    ],
)

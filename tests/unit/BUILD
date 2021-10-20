load("@rules_python//python:defs.bzl", "py_test")
load("@python_test_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_test(
    name = "test_static",
    srcs = ["test_static.py"],
    data = [
        "//:pytest",
    ],
    imports = ["$(BINDIR)/test_static.runfiles/python_test_deps/pypi__pyfakefs/pyfakefs/pytest_plugin.py"],
    deps = [
        "//cotd:static",
        requirement("pytest"),
        requirement("pyfakefs"),
    ],
)

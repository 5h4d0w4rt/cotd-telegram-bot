load("@rules_python//python:defs.bzl", "py_test")
load("@python_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//tests:__subpackages__"],
)

py_test(
    name = "test_static_integration",
    srcs = ["test_static_integration.py"],
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

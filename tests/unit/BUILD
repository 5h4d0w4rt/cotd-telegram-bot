load("@rules_python//python:defs.bzl", "py_test")
load("@python_test_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//tests:__subpackages__"],
)

py_test(
    name = "test_static_unit",
    srcs = ["test_static_unit.py"],
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

py_test(
    name = "test_utils_unit",
    srcs = ["test_utils_unit.py"],
    data = [
        "//:pytest",
    ],
    imports = ["$(BINDIR)/test_static.runfiles/python_test_deps/pypi__pyfakefs/pyfakefs/pytest_plugin.py"],
    deps = [
        "//cotd:utils",
        requirement("pytest"),
        requirement("pyfakefs"),
    ],
)

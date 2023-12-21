load("@rules_python//python:defs.bzl", "py_test")
load("@python_deps_v1//:requirements.bzl", "requirement")

package(
    default_visibility = ["//tests:__subpackages__"],
)

py_test(
    name = "test_static_integration_v1",
    srcs = ["test_static_integration.py"],
    data = [
        "//:pytest",
    ],
    imports = ["$(BINDIR)/test_static_integration.runfiles/python_deps_v1_pyfakefs/site-packages/pyfakefs/pytest_plugin.py"],
    deps = [
        "//cotd:static",
        requirement("pytest"),
        requirement("pyfakefs"),
    ],
)

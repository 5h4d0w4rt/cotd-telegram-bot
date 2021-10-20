load("@python_dev_deps//:requirements.bzl", devtools_entry_point = "entry_point")
load("@python_test_deps//:requirements.bzl", test_entry_point = "entry_point")

package(
    default_visibility = ["//visibility:public"],
)

exports_files(["pytest.ini"])

filegroup(
    # gather all the data for pytest binary to work
    name = "_pytest",
    srcs = [
        test_entry_point("pytest"),
        "//:pytest.ini",
    ],
)

alias(
    name = "black",
    actual = devtools_entry_point("black"),
)

alias(
    name = "pytest",
    actual = ":_pytest",
)

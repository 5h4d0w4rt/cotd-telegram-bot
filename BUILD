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

filegroup(
    name = "_black",
    srcs = [
        devtools_entry_point("black"),
    ],
)

alias(
    name = "black",
    actual = devtools_entry_point("black"),
    tags = ["local"],
)

alias(
    name = "pytest",
    actual = ":_pytest",
)

alias(
    name = "binpytest",
    actual = test_entry_point("pytest"),
    tags = ["local"],
)

filegroup(
    name = "_mypy",
    srcs = [
        devtools_entry_point("mypy"),
    ],
)

alias(
    name = "mypy",
    actual = devtools_entry_point("mypy"),
    tags = ["local"],
)

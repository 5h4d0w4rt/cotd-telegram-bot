load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "9fcf91dbcc31fde6d1edb15f117246d912c33c36f44cf681976bd886538deba6",
    strip_prefix = "rules_python-0.8.0",
    url = "https://github.com/bazelbuild/rules_python/archive/refs/tags/0.8.0.tar.gz",
)

load("@rules_python//python:repositories.bzl", "python_register_toolchains")

python_register_toolchains(
    name = "python",
    # Available versions are listed in @rules_python//python:versions.bzl.
    # We recommend using the same version your team is already standardized on.
    python_version = "3.10.2",
)

load("@python//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
    name = "python_runtime_deps",
    python_interpreter_target = interpreter,
    requirements = "//:requirements.txt",
)

pip_install(
    name = "python_test_deps",
    python_interpreter_target = interpreter,
    requirements = "//:requirements_testing.txt",
)

pip_install(
    name = "python_dev_deps",
    python_interpreter_target = interpreter,
    requirements = "//:requirements_devtools.txt",
)

#

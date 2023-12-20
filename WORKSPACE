load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

SHA = "e85ae30de33625a63eca7fc40a94fea845e641888e52f32b6beea91e8b1b2793"

VERSION = "0.27.1"

http_archive(
    name = "rules_python",
    sha256 = SHA,
    strip_prefix = "rules_python-{}".format(VERSION),
    url = "https://github.com/bazelbuild/rules_python/releases/download/{}/rules_python-{}.tar.gz".format(VERSION, VERSION),
)

load("@rules_python//python:repositories.bzl", "py_repositories", "python_register_toolchains")

py_repositories()

python_register_toolchains(
    name = "python",
    # Available versions are listed in @rules_python//python:versions.bzl.
    python_version = "3.11",
)

load("@python//:defs.bzl", "interpreter")
load("@rules_python//python:pip.bzl", "pip_parse")

pip_parse(
    name = "python_deps",
    python_interpreter_target = interpreter,
    requirements_lock = "//:requirements.txt.lock",
)

load("@python_deps//:requirements.bzl", "install_deps")

# Initialize repositories for all packages in requirements_lock.txt.
install_deps(python_interpreter_target = interpreter)

# pip_install(
#     name = "python_test_deps",
#     python_interpreter_target = interpreter,
#     requirements = "//:requirements_testing.txt",
# )

# pip_install(
#     name = "python_dev_deps",
#     python_interpreter_target = interpreter,
#     requirements = "//:requirements_devtools.txt",
# )

#

load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "b5668cde8bb6e3515057ef465a35ad712214962f0b3a314e551204266c7be90c",
    strip_prefix = "rules_python-0.0.2",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.0.2/rules_python-0.0.2.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_repositories")

pip_repositories()

load("@rules_python//python:pip.bzl", "pip_import")

# Create a central repo that knows about the dependencies needed for
# requirements.txt.
pip_import(
    # or pip3_import
    name = "python_workspace_deps",
    requirements = "//:requirements.txt",
)

load("@python_workspace_deps//:requirements.bzl", "pip_install")

pip_install()

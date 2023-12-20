load("@rules_python//python:defs.bzl", "py_binary")
load("@python_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//visibility:public"],
)

py_binary(
    name = "inspect_db",
    srcs = ["inspect_db.py"],
    deps = [
        requirement("python-telegram-bot"),
    ],
)

# throwaway
# genrule(
#     name = "inspect_db.sh",
#     srcs = [":inspect_db"],
#     outs = ["inspect_db1.sh"],
#     cmd_bash = "$(locations $(SRCS)) $$@ > $(OUTS)",
#     executable = True,
#     tags = [
#         "local",
#         "manual",
#     ],
# )

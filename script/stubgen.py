#!/usr/bin/env python3
"""Generate stub files for API classes with async and sync interface."""
from __future__ import annotations

import os
import sys
from copy import copy

from mypy.stubgen import (
    Options,
    StubGenerator,
    StubSource,
    collect_build_targets,
    generate_asts_for_modules,
    generate_guarded,
    mypy_options,
)


class ApiStubGenerator(StubGenerator):
    """Generate stub text from a mypy AST."""

    def add_sync(self):
        """Add sync methods."""
        output = copy(self._output)
        for i in range(len(output)):
            if "async" in output[i]:
                self.add(output[i].replace("async_", "").replace("async ", ""))
                self.add(output[i + 1])
                self.add(output[i + 2])


def generate_stubs() -> None:
    """Main entry point for the program."""
    options = Options(
        pyversion=sys.version_info[:2],
        no_import=True,
        doc_dir="",
        search_path=[],
        interpreter=sys.executable,
        parse_only=False,
        ignore_errors=False,
        include_private=False,
        output_dir="",
        modules=[],
        packages=[],
        files=["devolo_plc_api/device_api/deviceapi.py", "devolo_plc_api/plcnet_api/plcnetapi.py"],
        verbose=False,
        quiet=True,
        export_less=True,
    )
    mypy_opts = mypy_options(options)
    py_modules, _ = collect_build_targets(options, mypy_opts)
    generate_asts_for_modules(py_modules, options.parse_only, mypy_opts, options.verbose)
    files = []
    for mod in py_modules:
        target = mod.module.replace(".", "/")
        target += ".pyi"
        target = os.path.join(options.output_dir, target)
        files.append(target)
        with generate_guarded(mod.module, target, options.ignore_errors, options.verbose):
            generate_stub_from_ast(
                mod, target, options.parse_only, options.pyversion, options.include_private, options.export_less
            )


def generate_stub_from_ast(
    mod: StubSource, target: str, parse_only: bool, pyversion: tuple[int, int], include_private: bool, export_less: bool
) -> None:
    """Use analysed (or just parsed) AST to generate type stub for single file."""
    gen = ApiStubGenerator(
        mod.runtime_all, pyversion=pyversion, include_private=include_private, analyzed=not parse_only, export_less=export_less
    )
    mod.ast.accept(gen)
    gen.add_sync()

    with open(target, "w") as file:  # Write output to file.
        file.write("".join(gen.output()))


if __name__ == "__main__":
    generate_stubs()

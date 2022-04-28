#!/usr/bin/env python3
"""Generate stub files for API classes with async and sync interface."""
from __future__ import annotations

import os
import re
import sys
from contextlib import suppress
from copy import copy

from mypy.nodes import ConditionalExpr, Expression, ListExpr
from mypy.stubgen import (
    Options,
    StubGenerator,
    StubSource,
    collect_build_targets,
    generate_asts_for_modules,
    generate_guarded,
    mypy_options,
)

HEADER = '''"""
@generated by stubgen.  Do not edit manually!
isort:skip_file
"""
'''


class ApiStubGenerator(StubGenerator):
    """Generate stub text from a mypy AST."""

    def get_str_type_of_node(self, rvalue: Expression, can_infer_optional: bool = False, can_be_any: bool = True) -> str:
        """Get type of node as string."""
        if isinstance(rvalue, ConditionalExpr):
            if_type = self.get_str_type_of_node(rvalue.if_expr, can_infer_optional, False)
            else_type = self.get_str_type_of_node(rvalue.else_expr, can_infer_optional, False)
            if if_type and else_type and if_type != else_type:
                return f"{if_type} | {else_type}"
            return if_type or else_type or "Any" if can_be_any else ""
        if isinstance(rvalue, ListExpr):
            list_item_type = {self.get_str_type_of_node(item, can_infer_optional, can_be_any) for item in rvalue.items}
            return f"list[{' | '.join(list_item_type)}]"
        return super().get_str_type_of_node(rvalue, can_infer_optional, can_be_any)

    def add_sync(self):
        """Add sync methods."""
        output = copy(self._output)
        for i in range(len(output)):
            if "async" in output[i]:
                self.add(output[i].replace("async_", "").replace("async ", ""))
                self.add(output[i + 1])
                self.add(output[i + 2])

    def fix_union_annotations(self):
        """Fix Union annotations"""
        for i, output in enumerate(self._output):
            match = re.search(r"Union\[([a-z, ]+)\]", output)
            if match:
                types = match.group(1).replace(",", " |")
                self._output[i] = output.replace(match.group(0), types)


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
    if "annotations" in mod.ast.future_import_flags:
        gen.add_import_line("from __future__ import annotations\n")
        gen.fix_union_annotations()
    gen.add_sync()

    old_output = ""
    new_output = HEADER + "".join(gen.output())

    with suppress(FileNotFoundError), open(target, "r") as file:
        old_output = file.read()

    if new_output != old_output:
        with open(target, "w") as file:
            file.write(new_output)
            sys.exit(1)


if __name__ == "__main__":
    generate_stubs()

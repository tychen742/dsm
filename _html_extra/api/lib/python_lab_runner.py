import ast
import contextlib
import io
import json
import math
import os
import sys
import tempfile


ALLOWED_CALLS = {
    "print": print,
    "abs": abs,
    "int": int,
    "round": round,
    "ord": ord,
    "bin": bin,
    "hex": hex,
    "str": str,
    "float": float,
    "type": type,
    "bool": bool,
    "sum": sum,
    "len": len,
    "max": max,
    "min": min,
    "set": set,
    "sorted": sorted,
    "list": list,
}

ALLOWED_METHODS = {
    "append",
    "count",
    "get",
    "index",
    "items",
    "keys",
    "lower",
    "split",
    "strip",
    "upper",
    "values",
}

ALLOWED_NODES = (
    ast.Module,
    ast.Assign,
    ast.Expr,
    ast.Name,
    ast.Load,
    ast.Store,
    ast.Constant,
    ast.BinOp,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.FloorDiv,
    ast.Mod,
    ast.Pow,
    ast.UnaryOp,
    ast.UAdd,
    ast.USub,
    ast.Call,
    ast.keyword,
    ast.JoinedStr,
    ast.FormattedValue,
    ast.Attribute,
    ast.Compare,
    ast.Eq,
    ast.NotEq,
    ast.Lt,
    ast.LtE,
    ast.Gt,
    ast.GtE,
    ast.BoolOp,
    ast.And,
    ast.Or,
    ast.Not,
    ast.If,
    ast.For,
    ast.While,
    ast.AugAssign,
    ast.List,
    ast.Tuple,
    ast.Set,
    ast.Dict,
    ast.Subscript,
    ast.Slice,
    ast.FunctionDef,
    ast.arguments,
    ast.arg,
    ast.Return,
    ast.Pass,
    ast.Import,
    ast.alias,
)


# Matplotlib profile: plotting code needs a few more builtins and list
# comprehensions. File and system access is blocked by attribute name.
MATPLOTLIB_EXTRA_CALLS = {
    "abs": abs,
    "dict": dict,
    "enumerate": enumerate,
    "range": range,
    "tuple": tuple,
    "zip": zip,
}

MATPLOTLIB_EXTRA_NODES = (
    ast.ListComp,
    ast.comprehension,
)

MATPLOTLIB_IMPORTS = {"numpy", "pandas", "matplotlib", "matplotlib.pyplot"}

# Seaborn profile: the matplotlib profile plus seaborn. Dataset loaders are
# blocked because they read files or the network; labs supply inline data.
SEABORN_IMPORTS = MATPLOTLIB_IMPORTS | {"seaborn"}

PLOT_PROFILES = {"matplotlib", "seaborn"}

MATPLOTLIB_BLOCKED_ATTRIBUTES = {
    "api",
    "backends",
    "builtins",
    "canvas",
    "cbook",
    "compat",
    "ctypeslib",
    "DataSource",
    "eval",
    "fromfile",
    "fromregex",
    "get_data_home",
    "get_dataset_names",
    "genfromtxt",
    "get_cachedir",
    "get_configdir",
    "imread",
    "imsave",
    "io",
    "lib",
    "load",
    "load_dataset",
    "loadtxt",
    "matplotlib",
    "memmap",
    "os",
    "pickle",
    "print_figure",
    "query",
    "rc_file",
    "rc_params_from_file",
    "save",
    "savetxt",
    "savez",
    "savez_compressed",
    "subprocess",
    "switch_backend",
    "sys",
    "testing",
    "tofile",
}

MATPLOTLIB_ALLOWED_TO_METHODS = {"to_dict", "to_frame", "to_list", "to_numpy", "to_string"}


class LabCodeValidator(ast.NodeVisitor):
    def __init__(self, profile="plain_python"):
        self.profile = profile
        self.allowed_nodes = ALLOWED_NODES
        if profile in PLOT_PROFILES:
            self.allowed_nodes = ALLOWED_NODES + MATPLOTLIB_EXTRA_NODES

    def generic_visit(self, node):
        if not isinstance(node, self.allowed_nodes):
            raise ValueError(f"{type(node).__name__} is not allowed in this lab.")
        super().generic_visit(node)

    def visit_Import(self, node):
        if self.profile == "matplotlib":
            for alias in node.names:
                if alias.name not in MATPLOTLIB_IMPORTS:
                    raise ValueError("Only numpy, pandas, and matplotlib imports are allowed in this lab.")
            self.generic_visit(node)
            return
        if self.profile == "seaborn":
            for alias in node.names:
                if alias.name not in SEABORN_IMPORTS:
                    raise ValueError("Only numpy, pandas, matplotlib, and seaborn imports are allowed in this lab.")
            self.generic_visit(node)
            return
        if self.profile != "pandas":
            raise ValueError("Import is not allowed in this lab.")
        for alias in node.names:
            if alias.name not in {"pandas", "numpy"}:
                raise ValueError("Only pandas and numpy imports are allowed in this lab.")
        self.generic_visit(node)

    def visit_Name(self, node):
        if node.id.startswith("__"):
            raise ValueError("Names beginning with __ are not allowed.")
        self.generic_visit(node)

    def visit_Attribute(self, node):
        if node.attr.startswith("__"):
            raise ValueError("Attributes beginning with __ are not allowed.")
        if self.profile in PLOT_PROFILES and matplotlib_attribute_blocked(node.attr):
            raise ValueError(f"{node.attr} is not allowed in this lab.")
        self.generic_visit(node)

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            if node.func.id.startswith("__"):
                raise ValueError("Names beginning with __ are not allowed.")
        elif isinstance(node.func, ast.Attribute):
            if node.func.attr.startswith("__"):
                raise ValueError("Attributes beginning with __ are not allowed.")
            if self.profile == "plain_python" and node.func.attr not in ALLOWED_METHODS:
                raise ValueError("Only the allowed lab methods can be called.")
        else:
            raise ValueError("Only simple function and method calls are allowed.")
        self.generic_visit(node)


def prepare_pandas_tree(tree):
    aliases = {"pd": "pandas", "np": "numpy"}
    body = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                target = alias.asname or alias.name
                aliases[target] = alias.name
            continue
        body.append(node)
    tree.body = body
    ast.fix_missing_locations(tree)
    return aliases


def matplotlib_attribute_blocked(name):
    if name in MATPLOTLIB_BLOCKED_ATTRIBUTES:
        return True
    if name.startswith("read_"):
        return True
    if name.startswith("to_") and name not in MATPLOTLIB_ALLOWED_TO_METHODS:
        return True
    return False


def prepare_matplotlib_tree(tree, profile="matplotlib"):
    aliases = {"pd": "pandas", "np": "numpy", "plt": "matplotlib.pyplot"}
    if profile == "seaborn":
        aliases["sns"] = "seaborn"
    body = []
    for node in tree.body:
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.asname:
                    aliases[alias.asname] = alias.name
                else:
                    top_level = alias.name.split(".")[0]
                    aliases[top_level] = top_level
            continue
        body.append(node)
    tree.body = body
    ast.fix_missing_locations(tree)
    return aliases


def load_matplotlib(mplconfig_dir=None):
    # A persistent config dir keeps the font cache between runs. Without it,
    # every submission rebuilds the cache and exceeds the grader timeout.
    if not mplconfig_dir:
        mplconfig_dir = os.path.join(tempfile.gettempdir(), "dsm-mplconfig")
    os.makedirs(mplconfig_dir, exist_ok=True)
    os.environ["MPLCONFIGDIR"] = mplconfig_dir

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.figure
    import matplotlib.pyplot as plt

    saved = []

    def record_savefig(fig, fname=None, *args, **kwargs):
        # Record the dpi Matplotlib would use: the argument, else the
        # savefig.dpi setting, where "figure" means the figure's own dpi.
        dpi = kwargs.get("dpi")
        if dpi is None:
            dpi = matplotlib.rcParams["savefig.dpi"]
        if dpi == "figure":
            dpi = fig.dpi
        saved.append({
            "fname": fname if isinstance(fname, str) else "",
            "dpi": round_number(dpi),
            "format": kwargs.get("format") or "",
        })

    matplotlib.figure.Figure.savefig = record_savefig
    plt.show = lambda *args, **kwargs: None
    plt.close = lambda *args, **kwargs: None
    return matplotlib, plt, saved


def plot_color(value):
    import matplotlib.colors

    try:
        return matplotlib.colors.to_hex(value, keep_alpha=False)
    except (ValueError, TypeError):
        return ""


def plot_marker(value):
    if value in (None, "None", "none", ""):
        return ""
    return str(value)


def round_number(value):
    value = float(value)
    return round(value, 4) if math.isfinite(value) else None


def plot_alpha(value):
    return 1.0 if value is None else round_number(value)


def summarize_axes(ax):
    from matplotlib.collections import PathCollection
    from matplotlib.container import BarContainer

    lines = []
    for line in ax.get_lines():
        label = line.get_label()
        lines.append({
            "color": plot_color(line.get_color()),
            "linestyle": line.get_linestyle(),
            "linewidth": round_number(line.get_linewidth()),
            "marker": plot_marker(line.get_marker()),
            "label": "" if label.startswith("_") else label,
            "points": len(line.get_xdata()),
            "alpha": plot_alpha(line.get_alpha()),
        })

    bars = []
    for container in ax.containers:
        if isinstance(container, BarContainer):
            label = container.get_label() or ""
            bars.append({
                "bars": len(container.patches),
                "heights": [round_number(patch.get_height()) for patch in container.patches],
                "label": "" if label.startswith("_") else label,
                "alpha": plot_alpha(container.patches[0].get_alpha()) if container.patches else 1.0,
            })

    scatters = []
    for collection in ax.collections:
        if isinstance(collection, PathCollection):
            label = collection.get_label() or ""
            facecolors = collection.get_facecolors()
            scatters.append({
                "points": len(collection.get_offsets()),
                "colors": len({tuple(round(float(v), 4) for v in color[:3]) for color in facecolors}),
                "label": "" if label.startswith("_") else label,
                "alpha": plot_alpha(collection.get_alpha()),
            })

    # Seaborn box plots add one BoxPlotContainer per hue level (or one for all).
    boxes = sum(
        len(getattr(container, "boxes", []))
        for container in ax.containers
        if type(container).__name__ == "BoxPlotContainer"
    )

    legend = ax.get_legend()
    return {
        "title": ax.get_title(),
        "xlabel": ax.get_xlabel(),
        "ylabel": ax.get_ylabel(),
        "xlim": [round_number(v) for v in ax.get_xlim()],
        "ylim": [round_number(v) for v in ax.get_ylim()],
        "position": [round_number(v) for v in ax.get_position(original=True).bounds],
        "xscale": ax.get_xscale(),
        "yscale": ax.get_yscale(),
        "xticklabels": [t.get_text() for t in ax.get_xticklabels() if t.get_text()],
        "lines": lines,
        "bars": bars,
        "scatters": scatters,
        "boxes": boxes,
        "meshes": sum(1 for c in ax.collections if type(c).__name__ == "QuadMesh"),
        "texts": [t.get_text() for t in ax.texts],
        "legend": [t.get_text() for t in legend.get_texts()] if legend else [],
        "legend_title": legend.get_title().get_text() if legend else "",
        "has_legend": legend is not None,
    }


def summarize_figure(fig):
    fig.canvas.draw()
    suptitle = fig._suptitle.get_text() if getattr(fig, "_suptitle", None) else ""
    width, height = fig.get_size_inches()
    axes = fig.axes
    first = axes[0] if axes else None
    return {
        "size": [round_number(width), round_number(height)],
        "dpi": round_number(fig.dpi),
        "suptitle": suptitle,
        "sharex": len(axes) > 1 and all(first.get_shared_x_axes().joined(first, ax) for ax in axes),
        "sharey": len(axes) > 1 and all(first.get_shared_y_axes().joined(first, ax) for ax in axes),
        "axes": [summarize_axes(ax) for ax in axes],
        # Figure-level Seaborn functions (relplot, catplot, displot) put the
        # hue legend on the figure rather than on an axes.
        "figure_legend": [t.get_text() for legend in fig.legends for t in legend.get_texts()],
    }


def summarize_plots(plt, saved):
    figures = [plt.figure(num) for num in plt.get_fignums()]
    summary = summarize_figure(figures[-1]) if figures else {
        "size": [], "dpi": None, "suptitle": "", "sharex": False, "sharey": False, "axes": [],
        "figure_legend": [],
    }
    summary["figure_count"] = len(figures)
    summary["savefig"] = saved
    return summary


def resolve_plot_path(summary, path):
    # Paths look like "axes[0].lines[1].color" or "axes.count".
    current = summary
    for part in path.split("."):
        name, _, rest = part.partition("[")
        if name == "count" and not rest:
            if not isinstance(current, (list, dict)):
                raise KeyError(path)
            current = len(current)
            continue
        if name:
            if not isinstance(current, dict) or name not in current:
                raise KeyError(path)
            current = current[name]
        while rest:
            index_text, _, rest = rest.partition("]")
            rest = rest.lstrip("[")
            if not isinstance(current, list):
                raise KeyError(path)
            index = int(index_text)
            if index >= len(current) or index < -len(current):
                raise KeyError(path)
            current = current[index]
    return current


def plot_values_equal(actual, expected):
    if isinstance(expected, bool) or isinstance(actual, bool):
        return actual is expected
    if isinstance(expected, (int, float)) and isinstance(actual, (int, float)):
        return math.isclose(float(actual), float(expected), rel_tol=1e-3, abs_tol=1e-6)
    if isinstance(expected, list) and isinstance(actual, list):
        return len(actual) == len(expected) and all(
            plot_values_equal(a, e) for a, e in zip(actual, expected)
        )
    if isinstance(expected, str) and isinstance(actual, str):
        return actual.strip() == expected.strip()
    return actual == expected


def plot_check_passes(actual, expected):
    if isinstance(expected, dict):
        for op, value in expected.items():
            if op == "min" and not (isinstance(actual, (int, float)) and actual >= value):
                return False
            if op == "max" and not (isinstance(actual, (int, float)) and actual <= value):
                return False
            if op == "one_of" and not any(plot_values_equal(actual, v) for v in value):
                return False
            if op == "contains" and not (isinstance(actual, (str, list)) and value in actual):
                return False
            if op not in {"min", "max", "one_of", "contains"}:
                raise ValueError(f"Unknown plot check operator: {op}")
        return True
    return plot_values_equal(actual, expected)


def run_plot_checks(summary, checks):
    # Only hints go back to the student; expected values stay on the server.
    hints = []
    for check in checks:
        path = str(check.get("path", ""))
        try:
            actual = resolve_plot_path(summary, path)
            passed = plot_check_passes(actual, check.get("expected"))
        except (KeyError, ValueError, IndexError):
            passed = False
        if not passed:
            hint = str(check.get("hint") or "Check your chart against the instructions.")
            if hint not in hints:
                hints.append(hint)
    return {"passed": not hints, "hints": hints}


def run_matplotlib_code(code, python_paths=None, plot_checks=None, mplconfig_dir=None, profile="matplotlib"):
    add_python_paths(python_paths)
    tree = ast.parse(code, mode="exec")
    LabCodeValidator(profile).visit(tree)
    aliases = prepare_matplotlib_tree(tree, profile)
    compiled = compile(tree, "<student-code>", "exec")

    import numpy as np
    import pandas as pd

    matplotlib, plt, saved = load_matplotlib(mplconfig_dir)
    modules = {"numpy": np, "pandas": pd, "matplotlib": matplotlib, "matplotlib.pyplot": plt}
    if profile == "seaborn":
        import seaborn

        modules["seaborn"] = seaborn
    safe_globals = {"__builtins__": {**ALLOWED_CALLS, **MATPLOTLIB_EXTRA_CALLS}}
    for alias, module_name in aliases.items():
        safe_globals[alias] = modules[module_name]

    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout):
        exec(compiled, safe_globals, safe_globals)

    summary = summarize_plots(plt, saved)
    plot = run_plot_checks(summary, plot_checks or [])
    return stdout.getvalue(), summary, plot


def add_python_paths(paths):
    if not isinstance(paths, list):
        return
    for path in reversed(paths):
        if isinstance(path, str) and path and path not in sys.path:
            sys.path.insert(0, path)


def run_code(code, profile="plain_python", python_paths=None):
    if profile == "pandas":
        add_python_paths(python_paths)
    tree = ast.parse(code, mode="exec")
    LabCodeValidator(profile).visit(tree)
    pandas_aliases = {}
    if profile == "pandas":
        pandas_aliases = prepare_pandas_tree(tree)
    compiled = compile(tree, "<student-code>", "exec")
    stdout = io.StringIO()
    safe_globals = {"__builtins__": ALLOWED_CALLS}
    if profile == "pandas":
        # Loops over DataFrame columns need zip/range/enumerate, as in the plot profiles.
        safe_globals["__builtins__"] = {**ALLOWED_CALLS, **MATPLOTLIB_EXTRA_CALLS}
        import numpy as np
        import pandas as pd

        modules = {"pandas": pd, "numpy": np}
        for alias, module_name in pandas_aliases.items():
            safe_globals[alias] = modules[module_name]
    with contextlib.redirect_stdout(stdout):
        exec(compiled, safe_globals, {})
    return stdout.getvalue()


def main():
    try:
        payload = json.loads(sys.stdin.read() or "{}")
        code = str(payload.get("code", ""))
        profile = str(payload.get("profile", "plain_python"))
        if profile not in {"plain_python", "pandas"} | PLOT_PROFILES:
            raise ValueError("Unknown code runner profile.")
        if profile in PLOT_PROFILES:
            checks = payload.get("plot_checks") or []
            if not isinstance(checks, list):
                raise ValueError("plot_checks must be a list.")
            output, summary, plot = run_matplotlib_code(
                code,
                payload.get("python_paths", []),
                checks,
                payload.get("mplconfig_dir"),
                profile,
            )
            result = {"ok": True, "stdout": output, "stderr": "", "error": None, "plot": plot}
            if payload.get("include_summary"):
                result["summary"] = summary
            print(json.dumps(result))
            return
        output = run_code(code, profile, payload.get("python_paths", []))
        print(json.dumps({"ok": True, "stdout": output, "stderr": "", "error": None}))
    except Exception as exc:
        print(json.dumps({"ok": False, "stdout": "", "stderr": "", "error": str(exc)}))


if __name__ == "__main__":
    main()

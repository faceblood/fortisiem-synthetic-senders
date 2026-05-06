from __future__ import annotations

import argparse

from ..loaders import build_send_context
from ..runner import run_sender
from .common import (
    add_context_overrides,
    add_network_args,
    add_repo_arg,
    add_src_ip_args,
    add_throughput_args,
    cli_main_wrapper,
    context_kwargs_from_ns,
    resolve_repo_root,
)


def _parse() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Envía logs sintéticos Windows (EVTX-like text)")
    add_repo_arg(p)
    add_network_args(p)
    add_throughput_args(p)
    add_src_ip_args(p)
    add_context_overrides(p)
    p.add_argument(
        "--category",
        default="powershell",
        help="Categoría en plantillas (powershell, security, process, ransomware, ...)",
    )
    p.add_argument("--event-hint", default="")
    return p.parse_args()


def _main() -> int:
    ns = _parse()
    base = resolve_repo_root(ns)
    ctx = build_send_context(
        base,
        **context_kwargs_from_ns(ns),
        active_sources=frozenset({"windows"}),
        run_label="windows",
    )
    total = run_sender(
        base,
        source="windows",
        category=ns.category,
        event_hint=ns.event_hint,
        ctx=ctx,
        target=ns.target,
        port=ns.port,
        syslog_hostname=ns.syslog_hostname,
        count=max(1, ns.count),
        rate=max(1, ns.rate),
        dry_run=ns.dry_run,
    )
    print(f"Done. run_id={ctx.run_id} events={total}")
    return 0


def main() -> int:
    return cli_main_wrapper(_main)


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..constants import DEFAULT_PORT, DEFAULT_RATE, DEFAULT_TARGET
from ..ip_utils import parse_src_ip_mode


def resolve_repo_root(ns: argparse.Namespace) -> Path:
    cfg = getattr(ns, "config_dir", None)
    if cfg is not None:
        p = Path(cfg).resolve()
        if p.name == "config":
            return p.parent
        return p
    if getattr(ns, "repo_root", None):
        return Path(ns.repo_root).resolve()
    return Path.cwd().resolve()


def add_repo_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Directorio que contiene config/ y log_repository/ (por defecto: directorio actual)",
    )
    parser.add_argument(
        "--config-dir",
        type=Path,
        default=None,
        help="Ruta a la carpeta config/ del proyecto; la raíz del repo se toma como su directorio padre",
    )


def add_network_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--target", default=DEFAULT_TARGET, help="IP del collector syslog")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--syslog-hostname", default="localhost", help="Hostname en prefijo RFC3164")


def add_throughput_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--count", type=int, default=100)
    parser.add_argument("--rate", type=int, default=DEFAULT_RATE, help="Eventos por segundo (aprox.)")
    parser.add_argument("--dry-run", action="store_true", help="Solo imprime el mensaje, no envía UDP")


def add_src_ip_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--src-ip-mode", default="random", type=parse_src_ip_mode)
    parser.add_argument("--attacker-ip", default="", help="Fuerza IP de origen en el paquete y contexto")


def context_kwargs_from_ns(ns: argparse.Namespace) -> dict:
    """Map shared CLI namespace fields into build_send_context keyword args."""
    return {
        "user_samaccountname": ns.user_samaccountname,
        "vmware_user_spec": ns.vmware_user,
        "endpoint_ip": ns.endpoint_ip,
        "initial_asset_ip": ns.initial_asset_ip,
        "initial_asset_hostname": ns.initial_asset_hostname,
        "lateral_asset_ip": ns.lateral_asset_ip,
        "vmware_asset_ip": ns.vmware_asset_ip,
        "linux_asset_ip": ns.linux_asset_ip,
        "fortigate_devname": ns.fortigate_devname,
        "fortigate_serial": ns.fortigate_serial,
        "hostname": ns.hostname,
        "attacker_ip": ns.attacker_ip,
        "src_ip_mode": ns.src_ip_mode,
        "vpn_remote_ip": ns.vpn_remote_ip,
        "c2_ip": ns.c2_ip,
        "c2_domain": ns.c2_domain,
    }


def add_context_overrides(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--endpoint-ip", default="", help="IP del endpoint Windows (sintético si no está en assets)")
    parser.add_argument("--initial-asset-ip", default="")
    parser.add_argument("--initial-asset-hostname", default="")
    parser.add_argument("--hostname", default="", help="Hostname personalizado (no FortiGate)")
    parser.add_argument("--lateral-asset-ip", default="")
    parser.add_argument("--vmware-asset-ip", default="")
    parser.add_argument("--linux-asset-ip", default="")
    parser.add_argument("--user-samaccountname", default="")
    parser.add_argument("--vmware-user", default="")
    parser.add_argument("--fortigate-devname", default="")
    parser.add_argument("--fortigate-serial", default="")
    parser.add_argument("--vpn-remote-ip", default="")
    parser.add_argument("--c2-ip", default="")
    parser.add_argument("--c2-domain", default="")


def cli_main_wrapper(entry_fn) -> int:
    try:
        return entry_fn()
    except KeyboardInterrupt:
        print("\nInterrumpido por usuario.", file=sys.stderr)
        return 130
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

# fortisiem-synthetic-senders

[![CI](https://github.com/faceblood/fortisiem-synthetic-senders/actions/workflows/ci.yml/badge.svg)](https://github.com/faceblood/fortisiem-synthetic-senders/actions/workflows/ci.yml)

Herramientas **por fuente** para generar y enviar syslog sintético orientado a FortiSIEM. Este repo contiene las mismas plantillas (`log_repository/`) y datos (`config/`) que el proyecto de campañas, pero **sin** CSV de campañas, `--campaign`, ni pasos encadenados: cada ejecutable solo cubre una fuente y categoría acotada.

## Requisitos

- Python 3.10+
- Dependencias: `scapy>=2.5.0` (ver `requirements.txt` / `pyproject.toml`)

## Instalación

Desde la raíz del repo (donde están `config/` y `log_repository/`):

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -U pip setuptools wheel
pip install .
```

Los scripts de consola quedan como: `send-fortigate-vpn`, `send-fortigate-traffic`, `send-fortiedr`, `send-vmware`, `send-windows`, `send-linux`, `send-fortimail`.

Sin instalar en el entorno, puedes usar:

```bash
export PYTHONPATH=src
python3 -m fortisiem_send.cli.fortigate_vpn --help
```

## Uso

Por defecto se buscan `config/` y `log_repository/` en el **directorio actual**. Opcional: `--repo-root /ruta/al/repo` o `--config-dir /ruta/al/repo/config` (la raíz de datos será el directorio padre de `config/`).

Flags comunes (todos los CLIs): `--target`, `--port`, `--syslog-hostname`, `--count`, `--rate`, `--dry-run`, `--src-ip-mode`, `--attacker-ip`, overrides de contexto (`--endpoint-ip`, `--user-samaccountname`, `--fortigate-devname`, `--vpn-remote-ip`, `--c2-ip`, etc.; ver `--help`).

### Ejemplos

FortiGate VPN (categoría fija `vpn`):

```bash
send-fortigate-vpn --dry-run --count 5 --event-hint "tunnel"
```

FortiGate tráfico (`traffic`):

```bash
send-fortigate-traffic --dry-run --count 3 --c2-ip 203.0.113.50
```

FortiEDR (categoría por defecto `detection`):

```bash
send-fortiedr --dry-run --count 2 --category ransomware --event-hint "Ransomware"
```

VMware vCenter (categoría por defecto `auth`):

```bash
send-vmware --dry-run --count 2 --vmware-user administrator --event-hint "login"
```

Windows (categoría por defecto `powershell`):

```bash
send-windows --dry-run --count 2 --user-samaccountname jgarcia
```

Linux (categoría por defecto `ssh`):

```bash
send-linux --dry-run --count 2 --linux-asset-ip 10.10.50.10
```

FortiMail (categoría por defecto `phishing`):

```bash
send-fortimail --dry-run --count 2
```

## Equivalencia con `fortisiem-simple-log-campaign`

| Monolito (`fortisiem_log_sender.py`) | Este repo |
|--------------------------------------|-----------|
| `--sources fortigate --category vpn` | `send-fortigate-vpn` |
| `--sources fortigate --category traffic` | `send-fortigate-traffic` |
| `--sources fortiedr --category …` | `send-fortiedr --category …` |
| `--sources vmware` | `send-vmware --category …` |
| `--sources windows` | `send-windows --category …` |
| `--sources linux` | `send-linux --category …` |
| `--sources fortimail` | `send-fortimail --category …` |
| `--campaign` / `log_repository/campaigns/` | No soportado aquí (usar el proyecto de campañas) |

## Estructura

- `src/fortisiem_send/`: paquete compartido (carga CSV, plantillas, render, syslog Scapy).
- `config/`, `log_repository/`: datos y plantillas (las carpetas `campaigns/` se ignoran al cargar plantillas).

## Proyecto Git aparte (otra cuenta u organización)

Este directorio es un **repositorio Git independiente** (`git init` en la raíz, rama `main`). No depende de que vivas dentro del repo CSIRT: puedes **moverlo o clonarlo** a otra ruta (por ejemplo `~/Projects/fortisiem-synthetic-senders`) y seguir trabajando igual.

Para publicarlo en GitHub **con otra cuenta** (no la que usas por defecto en el Mac):

1. Crea en esa cuenta un repo **vacío** (sin README) con el nombre que quieras.
2. En esta carpeta, ajusta autor si hace falta: `git config user.name "…"` y `git config user.email "…"` (local, sin `--global`, solo para este repo).
3. Añade el remoto y sube:

   ```bash
   git remote add origin https://github.com/OTRA-CUENTA/fortisiem-synthetic-senders.git
   git push -u origin main
   ```

   Con **SSH** y una clave asociada a la otra cuenta: `git remote add origin git@github.com:OTRA-CUENTA/fortisiem-synthetic-senders.git`.

Si el repo CSIRT también es Git y no quieres un “repo dentro del repo”, añade `fortisiem-synthetic-senders/` al `.gitignore` del padre o mueve esta carpeta fuera del árbol CSIRT.

## Licencia / procedencia

Lógica y plantillas derivadas del proyecto interno de campañas FortiSIEM; este repo es un troceo operativo por fuente.

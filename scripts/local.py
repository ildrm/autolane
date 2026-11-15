#!/usr/bin/env python3
"""Local-only, resource-conscious process control. No hosting or deployment actions."""

import argparse
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / ".local"
LOCAL.mkdir(mode=0o700, exist_ok=True)
LOCAL.chmod(0o700)
ENV = {
    **os.environ,
    "UV_CACHE_DIR": str(LOCAL / "uv-cache"),
    "UV_CONCURRENT_DOWNLOADS": "2",
    "UV_CONCURRENT_BUILDS": "1",
    "npm_config_cache": str(LOCAL / "npm-cache"),
    "NODE_OPTIONS": "--max-old-space-size=1024",
    "RAYON_NUM_THREADS": "1",
    "NEXT_TELEMETRY_DISABLED": "1",
}


def run(args, cwd=ROOT, check=True):
    return subprocess.run([str(v) for v in args], cwd=cwd, env=ENV, check=check)


def pg(name):
    found = shutil.which(name)
    if found:
        return found
    for base in ["/opt/homebrew/opt/postgresql@17/bin", "/usr/lib/postgresql/17/bin"]:
        path = Path(base) / name
        if path.exists():
            return str(path)
    raise SystemExit(
        f"Install PostgreSQL17 and add {name} to PATH. No system services were changed."
    )


def database():
    data = LOCAL / "postgres"
    if not (data / "PG_VERSION").exists():
        password = LOCAL / "postgres-password"
        password.write_text("autolane-local")
        password.chmod(0o600)
        run(
            [
                pg("initdb"),
                "-D",
                data,
                "-U",
                "autolane",
                "--auth-local=trust",
                "--auth-host=scram-sha-256",
                "--pwfile",
                password,
                "--encoding=UTF8",
                "--no-locale",
            ]
        )
        with (data / "postgresql.conf").open("a") as f:
            f.write(
                "\nlisten_addresses='127.0.0.1'\nport=55432\nshared_buffers='32MB'\nwork_mem='2MB'\nmaintenance_work_mem='16MB'\nmax_connections=16\nmax_parallel_workers=0\nmax_worker_processes=2\nunix_socket_directories='/tmp'\n"
            )
    if run([pg("pg_ctl"), "-D", data, "status"], check=False).returncode:
        run([pg("pg_ctl"), "-D", data, "-l", LOCAL / "postgres.log", "start"])
    import psycopg

    with psycopg.connect(
        "postgresql://autolane:autolane-local@127.0.0.1:55432/postgres", autocommit=True
    ) as db:
        if not db.execute("SELECT 1 FROM pg_database WHERE datname='autolane'").fetchone():
            db.execute("CREATE DATABASE autolane")


def start_process(name, args, cwd):
    marker = LOCAL / (name + ".json")
    if marker.exists():
        info = json.loads(marker.read_text())
        birth = subprocess.run(
            ["ps", "-p", str(info["pid"]), "-o", "lstart="], capture_output=True, text=True
        ).stdout.strip()
        if birth and birth == info["birth"]:
            print(name + " is already running")
            return
    with (LOCAL / (name + ".log")).open("a") as log:
        (LOCAL / (name + ".log")).chmod(0o600)
        process = subprocess.Popen(
            args, cwd=cwd, env=ENV, stdout=log, stderr=log, start_new_session=True
        )
    birth = subprocess.run(
        ["ps", "-p", str(process.pid), "-o", "lstart="], capture_output=True, text=True
    ).stdout.strip()
    marker.write_text(json.dumps({"pid": process.pid, "birth": birth}))
    print(f"Started {name}; logs in .local/{name}.log")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "action", choices=["setup", "start", "stop", "test", "build", "worker", "database"]
    )
    args = parser.parse_args()
    python = ROOT / ".venv/bin/python"
    manage = [python, ROOT / "apps/api/manage.py"]
    if args.action == "setup":
        run(["uv", "sync", "--frozen"])
        run(["npm", "ci", "--no-audit", "--no-fund", "--maxsockets=2"], ROOT / "apps/web")
        # Re-execute in the project environment for the PostgreSQL driver.
        run([python, __file__, "database"])
        run(manage + ["migrate", "--noinput"])
        run(manage + ["seed_development"])
    elif args.action == "database":
        database()
    elif args.action == "start":
        database()
        start_process(
            "api",
            [
                str(python),
                "-m",
                "uvicorn",
                "config.asgi:application",
                "--app-dir",
                str(ROOT / "apps/api"),
                "--host",
                "127.0.0.1",
                "--port",
                "8000",
                "--workers",
                "1",
                "--limit-concurrency",
                "12",
                "--no-access-log",
            ],
            ROOT,
        )
        web_command = "start" if (ROOT / "apps/web/.next/BUILD_ID").exists() else "dev"
        start_process("web", ["npm", "run", web_command], ROOT / "apps/web")
        start_process("worker", [str(v) for v in manage + ["work_events"]], ROOT)
        print("Local app: http://127.0.0.1:3000 · API health: http://127.0.0.1:8000/health/")
    elif args.action == "stop":
        for name in ["web", "api", "worker"]:
            marker = LOCAL / (name + ".json")
            if marker.exists():
                info = json.loads(marker.read_text())
                birth = subprocess.run(
                    ["ps", "-p", str(info["pid"]), "-o", "lstart="], capture_output=True, text=True
                ).stdout.strip()
                if birth and birth == info["birth"]:
                    try:
                        os.killpg(info["pid"], signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                marker.unlink()
        run([pg("pg_ctl"), "-D", LOCAL / "postgres", "stop", "-m", "fast"], check=False)
    elif args.action == "test":
        run([ROOT / ".venv/bin/ruff", "check", "apps/api", "scripts/local.py"])
        run(manage + ["test", "marketplace.tests", "--noinput", "--parallel=1"])
        run(["npm", "run", "typecheck"], ROOT / "apps/web")
    elif args.action == "build":
        run(["npm", "run", "build"], ROOT / "apps/web")
    elif args.action == "worker":
        run(manage + ["work_events", "--once"])


if __name__ == "__main__":
    main()

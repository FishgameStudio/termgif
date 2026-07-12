"""
Simple Windows recorder using winpty.
Usage examples (cmd):
  python record_win.py -o session.cast -- cmd /c "echo hi & timeout /t 1"
PowerShell:
  python record_win.py -o session.cast -- powershell -Command "for ($i=0;$i -lt 5;$i++){Write-Output \"line $i\"; Start-Sleep -Milliseconds 200}"
"""

# pyright: reportMissingTypeStubs=false, reportUnknownMemberType=false, reportAny=false
import argparse, json, time, sys, ctypes, contextlib

def _get_console_encoding() -> str:
    if sys.platform != "win32":
        return "utf-8"
    try:
        codepage = ctypes.cdll.kernel32.GetConsoleOutputCP()
        if codepage == 936:
            return "gbk"
        elif codepage == 65001:
            return "utf-8"
        return f"cp{codepage}"
    except Exception:
        return "gbk"

def record_with_winpty(cmdlist: list[str], out_path: str, width: int = 80, height: int = 24) -> None:
    import winpty
    # TODO: Support other platforms.
    if sys.platform != "win32":
        raise NotImplementedError("winpty recording only supports Windows platform in v0.1.0")

    # Build command line string for spawn (winpty expects a commandline string)
    cmdline: str = " ".join(cmdlist)
    p: winpty.ptyprocess.PtyProcess = winpty.PtyProcess.spawn(argv=cmdline)
    events: list[list[float | str]] = []
    start = time.time()
    try:
        while True:
            try:
                data = p.read(1024)
            except EOFError:
                break
            if not data:
                break
            # winpty returns str on Python3; ensure str
            if isinstance(data, bytes):
                data = data.decode(_get_console_encoding(), "replace")
            events.append([time.time() - start, data])
    finally:
        with contextlib.suppress(Exception):
            _ = p.wait()
    cast = {"version": 2, "width": width, "height": height, "events": events}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(cast, f, ensure_ascii=False)
    print(f"Recorded {len(events)} events -> {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    _ = parser.add_argument("-o", "--out", required=True, help="Output cast file (JSON)")
    _ = parser.add_argument("--width", type=int, default=80)
    _ = parser.add_argument("--height", type=int, default=24)
    _ = parser.add_argument("cmd", nargs=argparse.REMAINDER, help="Command to run (after --)")
    args: argparse.Namespace = parser.parse_args()
    if not args.cmd:
        parser.error('Missing command. Example: python record_win.py -o session.cast -- cmd /c "echo hi"')
    # args.cmd is list; keep as-is (works if user supplies full tokens)
    record_with_winpty(args.cmd, args.out, width=args.width, height=args.height)


if __name__ == "__main__":
    main()

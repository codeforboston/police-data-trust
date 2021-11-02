import subprocess
import sys

req_files = [
    "requirements/dev_unix.in",
    "requirements/dev_windows.in",
    "requirements/prod.in",
    "requirements/docs.in",
]


def run():
    results = []
    for filename in req_files:
        results.append((filename, subprocess.call(["pip-compile", filename])))

    succeeded = lambda r: r[1] == 0
    print()
    for result in results:
        print(f"{result[0]} {'succeeded' if succeeded(result) else 'failed'}")

    return 0 if all(map(succeeded, results)) else 1


if __name__ == "__main__":
    code = run()
    sys.exit(code)

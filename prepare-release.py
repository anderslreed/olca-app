# Checks and updates the resources that go into a final release. These are:
# * the olca-modules (we assume that the olca-modules repository is located
#   next to this repository)
# * the current reference database
# * the HTML pages
# * the current modules interface for the Jython interpreter

from dataclasses import dataclass
import os
from pathlib import Path
from subprocess import call

@dataclass
class Commands:
    mvn: str
    npm: str

def get_commands():
    if os.name == "posix":
        return Commands("mvn", "npm")
    else:
        return Commands("mvn.cmd", "npm.cmd")

def update_modules(commands: Commands, current_dir: Path):
    modules_path = current_dir.parent / "olca-modules"
    app_path = current_dir / "olca-app"
    print(f"install olca-modules from {modules_path}")
    call(["mvn", "install", "-DskipTests"], cwd=modules_path)
    print(f"update packages in {app_path}/libs")
    call([commands.mvn, "-f", "pom_libs.xml", "package"], cwd=current_dir / "olca-app")
    print("all done")

def main():
    commands = get_commands()
    current_dir = Path(__file__).parent
    call([commands.mvn, "-f", "pom_libs.xml", "clean"], cwd=current_dir / "olca-app")
    update_modules(commands, current_dir)
    call([commands.mvn, "package"], cwd=current_dir / "olca-refdata")
    call([commands.npm, "install"], cwd=current_dir / "olca-app-html")
    call([commands.npm, "run", "build"], cwd=current_dir / "olca-app-html")
    call([commands.npm, "install"], cwd=current_dir / "olca-app-build/credits")
    call(["node", "credits-gen.js"], cwd=current_dir / "olca-app-build/credits")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from pathlib import Path
from typing import List, Dict, Set


def discover_packages_and_modules(root_path: Path) -> Dict[str, List[str]]:
    """
    Discover all packages and modules recursively.
    Returns: Dict with package_path -> list of modules
    """
    packages_modules = {}

    def _discover_recursive(current_path: Path, base_package: str = "") -> Set[str]:
        """Recursively discover all Python packages and modules."""
        discovered = set()

        for item in current_path.iterdir():
            if item.is_dir() and (item / '__init__.py').exists():
                # It's a package
                package_name = f"{base_package}.{item.name}" if base_package else item.name
                discovered.add(package_name)

                # Recursively discover subpackages
                sub_items = _discover_recursive(item, package_name)
                discovered.update(sub_items)

            elif item.is_file() and item.suffix == '.py':
                # It's a module
                if item.name != '__init__.py' and not item.name.startswith('setup'):
                    module_name = item.stem
                    full_module_name = f"{base_package}.{module_name}" if base_package else module_name
                    discovered.add(full_module_name)

        return discovered

    all_items = _discover_recursive(root_path)

    # Organize by package
    for full_name in all_items:
        if '.' in full_name:
            package = full_name.rsplit('.', 1)[0]
        else:
            package = full_name

        if package not in packages_modules:
            packages_modules[package] = []

        packages_modules[package].append(full_name)

    return packages_modules


def generate_package_docs(package_name: str, modules: List[str], output_dir: Path):
    """Generate .rst files for a package and its modules."""
    package_title = package_name
    package_underline = '=' * len(package_title)

    # Start package documentation
    package_rst = f"""{package_title}
{package_underline}

.. automodule:: {package_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__
   :no-index:

"""

    # Group modules by subpackages and direct modules
    subpackages = {}
    direct_modules = []

    for module in modules:
        if module == package_name:
            continue  # Skip the package itself

        if module.startswith(package_name + '.'):
            remaining = module[len(package_name) + 1:]
            if '.' in remaining:
                # It's in a subpackage
                subpackage = remaining.split('.')[0]
                if subpackage not in subpackages:
                    subpackages[subpackage] = []
                subpackages[subpackage].append(module)
            else:
                # It's a direct module in this package
                direct_modules.append(module)
        else:
            direct_modules.append(module)

    # Add subpackages section if there are any
    if subpackages:
        package_rst += """Subpackages
-----------

.. toctree::
   :maxdepth: 1

"""
        for subpackage in sorted(subpackages.keys()):
            package_rst += f"   {package_name}.{subpackage}\n"

    # Add modules section if there are any direct modules
    if direct_modules:
        package_rst += """Modules
-------

.. toctree::
   :maxdepth: 1

"""
        for module in sorted(direct_modules):
            module_name = module.split('.')[-1]
            package_rst += f"   {module}\n"

    # Write package documentation
    package_path = output_dir / f"{package_name}.rst"
    with open(package_path, 'w') as f:
        f.write(package_rst)

    # Generate individual module documentation
    for module in direct_modules:
        generate_module_doc(module, output_dir)

    # Generate subpackage index files recursively
    for subpackage, subpackage_modules in subpackages.items():
        generate_package_docs(f"{package_name}.{subpackage}", subpackage_modules, output_dir)


def generate_module_doc(module_name: str, output_dir: Path):
    module_title = module_name
    module_underline = '=' * len(module_title)

    module_rst = f"""{module_title}
{module_underline}

.. automodule:: {module_name}
   :members:
   :undoc-members:
   :show-inheritance:
   :special-members: __init__

"""
    safe_module_name = module_name.replace('.', '_')
    module_path = output_dir / f"{safe_module_name}.rst"
    with open(module_path, 'w') as f:
        f.write(module_rst)


def generate_main_index(packages_modules: Dict[str, List[str]], output_dir: Path):
    """Generate the main modules.rst index file."""
    modules_rst = """API Reference
=============

.. toctree::
   :maxdepth: 3

"""
    for package in sorted(packages_modules.keys()):
        if '.' not in package and not package.startswith(('setup', 'generate_')):  # Only top-level items
            modules_rst += f"   {package}\n"

    modules_path = output_dir / "modules.rst"
    with open(modules_path, 'w') as f:
        f.write(modules_rst)


def main():
    project_root = Path('..')
    api_dir = Path('api')
    api_dir.mkdir(exist_ok=True)

    print("Discovering packages and modules...")
    packages_modules = discover_packages_and_modules(project_root)

    print(f"Found {len(packages_modules)} packages:")
    for package, modules in packages_modules.items():
        print(f"  {package}: {len(modules)} modules")

    # Only remove auto-generated API documentation files
    for file in api_dir.glob("*.rst"):
        file.unlink()

    for package, modules in packages_modules.items():
        if package.startswith(('setup', 'generate_')):
            print(f"Skipping {package}...")
            continue
        print(f"Generating docs for {package}...")
        generate_package_docs(package, modules, api_dir)

    print("API documentation generation complete!")
    print(f"Files generated in: {api_dir.absolute()}")


if __name__ == '__main__':
    main()

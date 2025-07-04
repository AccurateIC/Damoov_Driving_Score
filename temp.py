import os
import ast

project_dir = "."  # or your project path
imports = set()

for root, dirs, files in os.walk(project_dir):
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    try:
                        node = ast.parse(f.read(), filename=file)
                        for n in ast.walk(node):
                            if isinstance(n, ast.Import):
                                for alias in n.names:
                                    imports.add(alias.name.split('.')[0])
                            elif isinstance(n, ast.ImportFrom):
                                if n.module:
                                    imports.add(n.module.split('.')[0])
                    except SyntaxError:
                        print(f"⚠️ Syntax error in {path}, skipping.")
            except UnicodeDecodeError:
                print(f"⚠️ Could not decode {path}, skipping due to encoding issue.")

print("\n✅ Unique imported modules:")
for name in sorted(imports):
    print(name)

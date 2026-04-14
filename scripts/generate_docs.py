#!/usr/bin/env python3

import os
import shutil
import sys

# Get the version from command line arguments (e.g., 'v4' or 'canary')
# Default to 'canary' if no argument is provided
version_folder = sys.argv[1] if len(sys.argv) > 1 else 'canary'

script_dir = os.path.dirname(os.path.abspath(__file__))
wit_module = os.path.join('src', 'spin_sdk', 'wit', '__init__.py')
expected_doc_comment = '""" Module with the bindings generated from the wit by componentize-py """\n\n'

with open(wit_module, 'r') as init_file:
    content = init_file.read()

if expected_doc_comment not in content:
    with open(wit_module, 'w') as init_file:
        init_file.write(expected_doc_comment + content)

# Change to the root directory of the project
os.chdir(os.path.join(script_dir, '..'))

# Use the dynamic version_folder for the target directory
target_docs_path = os.path.join('docs', version_folder)

# Clean existing folder for this specific version
shutil.rmtree(target_docs_path, ignore_errors=True)

# Change directory to 'src' and generate HTML documentation using pdoc
os.chdir('src')
os.system('pdoc --html spin_sdk')

# Move the generated documentation to the versioned directory
shutil.move('html/spin_sdk', os.path.join('..', target_docs_path))

# Remove the 'src/html' directory
os.rmdir('html')
os.chdir('..')

# Generate a redirect index.html at the root of the docs folder
root_index_path = os.path.join(script_dir, '..', 'docs', 'index.html')

redirect_content = f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="0; url={version_folder}/" />
    <script type="text/javascript">
      window.location.href = "{version_folder}/"
    </script>
    <title>Redirecting...</title>
  </head>
  <body>
    <p>If you are not redirected, <a href="{version_folder}/">click here</a>.</p>
  </body>
</html>
"""

# Only update the root redirect if we are building a major version (not canary)
if version_folder.startswith('v'):
    with open(root_index_path, 'w') as f:
        f.write(redirect_content)

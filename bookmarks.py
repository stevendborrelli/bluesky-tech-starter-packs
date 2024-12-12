import re
from jinja2 import Environment, FileSystemLoader

#
# Generate a bookmarks.html file from the README.md file 
# which can be imported inta a browser.
#

# Setup Jinja2 environment
env = Environment(
    loader=FileSystemLoader("."),
    trim_blocks=True,
    lstrip_blocks=True
)
template = env.get_template("bookmarks.jinja")

# Read the markdown input from file
with open("README.md", "r") as file:
    markdown = file.read()

# Omit everything before "## AI, ML & Data"
start_marker = "## AI, ML & Data"
if start_marker in markdown:
    markdown = markdown[markdown.index(start_marker):]

def parse_markdown(markdown):
    lines = markdown.strip().split("\n")
    category = None
    parsed_data = {}

    for line in lines:
        if line.startswith("##"):
            category = line[2:].strip()
            parsed_data[category] = []
        elif line.startswith("*") and category:
            match = re.match(r"\* (.+?) <(.+?)>", line)
            if match:
                title, url = match.groups()
                parsed_data[category].append({"title": title, "url": url})

    return parsed_data

# Parse the markdown
parsed_object = parse_markdown(markdown)

# Render the template
rendered = template.render(categories=parsed_object)

# Save the output to a file
with open("bookmarks.html", "w") as f:
    f.write(rendered)

print(rendered)

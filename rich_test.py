from rich import print
from rich.layout import Layout

layout = Layout()

layout.split_row(
    Layout(name="upper"),
    Layout(name="lower")
)
print(layout)

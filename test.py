from rich import print as rprint
from rich import pretty
from rich.panel import Panel
from rich import inspect
from rich.color import Color
from rich.console import Console
from rich.text import Text
import webcolors

a = ['brown', 'purple', 'maroon', 'blue', 'red', 'gray', 'green', 'black', 'orange', 'gold', 'darkred', 'violet', 'crimson', 'rainbow']
move = ""
for e in a:
    try:
        color = webcolors.name_to_hex(e)
    except ValueError:
        color = 'white'
    move += f"[{color}]{e}[/{color}] "
rprint(move)


console = Console()

def rainbow(text):
    colors = ["red", "orange", "yellow", "green", "blue", "purple"]
    result = Text()

    for i, char in enumerate(text):
        result.append(char, style=colors[i % len(colors)])

    return result

x = rainbow("Hello World!")

z = f"hello {x}"

console.print(z)
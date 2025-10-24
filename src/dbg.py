# Diagnostics Utilities
from yachalk import chalk

# ten tweakable values
v = [0] * 10
index = 0
increment = 0
increments = [0.1, 0.01, 0.001, 1]

# unpack for quick reads (kept in sync via update_values)
v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = v

def select(i: int):
    """Focus adjustments on v[i]."""
    global index
    index = i
    print(f"debug: v{index+1} = {v[index]}")

def update_values():
    """Refresh the convenience variables v1..v10 from the list."""
    global v1, v2, v3, v4, v5, v6, v7, v8, v9, v10
    v1, v2, v3, v4, v5, v6, v7, v8, v9, v10 = v

def up(inc_offset: int = 0):
    """Increase the selected value by a chosen step size (offset rotates sizes)."""
    v[index] += increments[(increment + inc_offset) % len(increments)]
    update_values()
    print(chalk.green(f"debug: v{index+1} = {v[index]}"))

def down(inc_offset: int = 0):
    """Decrease the selected value by a chosen step size (offset rotates sizes)."""
    v[index] -= increments[(increment + inc_offset) % len(increments)]
    update_values()
    print(chalk.red(f"debug: v{index+1} = {v[index]}"))

def cycle_increment():
    """Cycle through the predefined step sizes."""
    global increment
    increment = (increment + 1) % len(increments)
    print(f"debug: step = {increments[increment]}")

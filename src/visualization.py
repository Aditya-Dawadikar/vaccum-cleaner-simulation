"""
Module for Data visualization
"""
import os
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import patches
from PIL import Image
import numpy as np


def plot_grid(environment, path_followed, obstacles, dirt, file_path, fig_name=""):
    grid = np.array(environment.grid_descriptor.__get_grid__())
    
    # Define colors
    white = 'white'
    gray = 'gray'
    blue = 'blue'
    red = 'red'
    yellow = 'yellow'
    green = 'green'
    
    # Create color map
    color_map = {
        white: 0,
        gray: 1,
        blue: 2,
        red: 3,
        yellow: 4,
        green: 5
    }
    
    # Initialize grid with white background
    grid_color = np.full(grid.shape, color_map[white], dtype=int)

    # Mark obstacles
    for obs in obstacles:
        grid_color[obs["x"], obs["y"]] = color_map[gray]

    # Define start and end points
    if path_followed:
        start_point = path_followed[0]
        end_point = path_followed[-1]
        grid_color[start_point[0], start_point[1]] = color_map[yellow]
        grid_color[end_point[0], end_point[1]] = color_map[green]

    # Define a custom color map
    colors = [white, gray, blue, red, yellow, green]
    custom_cmap = mcolors.ListedColormap(colors)
    bounds = [0, 1, 2, 3, 4, 5]
    norm = mcolors.BoundaryNorm(bounds, custom_cmap.N)

    # Plotting
    plt.figure(figsize=(5, 5))  # 500x500 pixels
    plt.imshow(grid_color, cmap=custom_cmap, norm=norm, interpolation='nearest')

    ax = plt.gca()
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add circles for dirt and path
    for d in dirt:
        x, y = d["x"], d["y"]
        if grid_color[x, y] == color_map[gray]:
            # Dirt should not overlap with an obstacle
            continue
        circle = plt.Circle((y, x), 0.3, color=red, zorder=2)  # Red dot for dirt
        ax.add_patch(circle)
        
    for p in path_followed:
        x, y = p[0], p[1]
        
        if grid_color[x, y] == color_map[yellow]:
            rect = patches.Rectangle((y - 0.5, x - 0.5), 1, 1, linewidth=0, edgecolor='none', facecolor=yellow, zorder=1)
            ax.add_patch(rect)
        elif grid_color[x, y] == color_map[green]:
            rect = patches.Rectangle((y - 0.5, x - 0.5), 1, 1, linewidth=0, edgecolor='none', facecolor=green, zorder=1)
            ax.add_patch(rect)

        # Add blue dot for path
        circle = plt.Circle((y, x), 0.15, color=blue, zorder=3)  # Blue dot for path
        ax.add_patch(circle)
    
    plt.title('Agent Grid with Path and Dirt')
    plt.gca().invert_yaxis()  # To match typical grid orientation
    
    filename = f"{file_path}/step_{fig_name:03d}.png"  # Step number with leading zeros
    plt.savefig(filename, bbox_inches='tight')
    plt.close()

def create_gif(image_folder, gif_folder,gif_filename):
    images = []
    for filename in sorted(os.listdir(image_folder)):
        if filename.endswith(".png"):
            img_path = os.path.join(image_folder, filename)
            images.append(Image.open(img_path))
    
    if images:
        images[0].save(f"""{gif_folder}/{gif_filename}""", save_all=True, append_images=images[1:], duration=500, loop=0)

def plot_energy_expenditure_per_step(energy_expenditure):
    time = list(range(len(energy_expenditure)))  # Generate time based on the array length
    avg_energy = sum(energy_expenditure) / len(energy_expenditure)  # Calculate average energy expenditure
    
    plt.figure()
    plt.plot(time, energy_expenditure, 'g-', label='Energy Expenditure')
    
    # Plot the average line
    plt.axhline(y=avg_energy, color='r', linestyle='--', label=f'Average: {avg_energy:.2f}')
    
    plt.xlabel('Time (Index)')
    plt.ylabel('Energy Expenditure')
    plt.title('Energy Expenditure Per Step')
    plt.ylim(ymin=0)  # Set the minimum y value to 0
    plt.grid(True)
    plt.legend()  # Add legend for better clarity
    plt.show()

def plot_battery_usage(battery_usage):
    time = list(range(len(battery_usage)))  # Generate time based on the array length
    plt.figure()
    plt.plot(time, battery_usage, 'b-', label='Battery Usage')
    plt.xlabel('Time (Index)')
    plt.ylabel('Battery Usage')
    plt.ylim(ymin=0)
    plt.title('Battery Usage Over Time')
    plt.grid(True)
    plt.show()

def plot_steps_to_clean(steps_to_clean):
    plt.figure()
    plt.plot(range(len(steps_to_clean)), steps_to_clean, linestyle='-', color='b')  # Removed 'marker'
    plt.xlabel('Dirt Spot Index')
    plt.ylabel('Steps to Clean')
    plt.title('Steps Taken to Clean Each Dirt Spot')
    
    # Automatically adjust x-tick frequency based on number of dirt spots
    num_spots = len(steps_to_clean)
    tick_frequency = max(1, num_spots // 10)  # Show at least 10 ticks

    plt.xticks(ticks=range(0, num_spots, tick_frequency))  # Adjust x-ticks

    plt.grid(True)
    plt.show()

def plot_dirt_spots_left(dirt_spots_left):
    plt.figure()
    plt.plot(range(len(dirt_spots_left)), dirt_spots_left, linestyle='-', color='r')  # Line graph
    plt.xlabel('Time (Iteration)')
    plt.ylabel('Dirt Spots Left')
    plt.ylim(ymin=0)
    plt.title('Number of Dirt Spots Left Over Time')
    
    # Automatically adjust x-tick frequency based on number of iterations
    num_iterations = len(dirt_spots_left)
    tick_frequency = max(1, num_iterations // 10)  # Show at least 10 ticks

    plt.xticks(ticks=range(0, num_iterations, tick_frequency))  # Adjust x-ticks

    plt.grid(True)
    plt.show()
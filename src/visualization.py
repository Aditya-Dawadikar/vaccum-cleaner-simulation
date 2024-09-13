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

def dirt_clean_percentage(df):
    plt.figure(figsize=(10, 6))
    sns.barplot(x="simulation_name", y="percentage_dirt_cleaned", data=df)
    plt.xticks(rotation=45)
    plt.title("Percentage of Dirt Cleaned per Simulation")
    plt.ylabel("Percentage of Dirt Cleaned")
    plt.xlabel("Simulation Name")
    plt.show()

def energy_consumption_vs_dirt_cleaned(df):
    plt.figure(figsize=(10, 6))
    sns.lineplot(x="percentage_dirt_cleaned", y="total_energy_consumed", hue="simulation_name", data=df, marker='o')
    plt.title("Energy Consumed vs Dirt Cleaned")
    plt.xlabel("Percentage of Dirt Cleaned")
    plt.ylabel("Total Energy Consumed")
    plt.show()

def efficiency_and_energy_consumption_per_step(df):
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x="coverage_efficiency", y="percentage_energy_consumed_per_step", hue="simulation_name", data=df, s=100)
    plt.title("Coverage Efficiency vs Energy Consumed per Step")
    plt.xlabel("Coverage Efficiency")
    plt.ylabel("Percentage Energy Consumed per Step")
    plt.show()

def metrics_correlation(df):
    # Drop non-numeric columns, such as 'simulation_name'
    numeric_df = df.drop(columns=['simulation_name'])
    
    # Plot the correlation matrix for only the numeric columns
    plt.figure(figsize=(10, 6))
    correlation_matrix = numeric_df.corr()
    sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm")
    plt.title("Correlation Between Performance Metrics")
    plt.show()

def energy_consumption_per_empty_spot(df):
    df.boxplot(column='percentage_energy_consumed_per_dirty_spot', by='simulation_name', grid=False)
    plt.title('Energy Consumption per Dirty Spot Across Simulations')
    plt.suptitle('')  # Removes default subtitle
    plt.xlabel('Simulation Name')
    plt.ylabel('Energy Consumed per Dirty Spot')
    plt.xticks(rotation=12)
    plt.show()
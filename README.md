# Interactive Mandelbrot Set Viewer

This project implements an interactive viewer for the **Mandelbrot set**, a famous fractal, using **VisPy**, a high-performance visualization library. The viewer allows users to zoom and pan in real-time, with dynamic resolution adjustments based on the zoom level.

## Mathematical Background

The Mandelbrot set is defined by the following iterative process for a complex number **c**:

$$
z_0 = 0
$$
$$
z_{n+1} = z_n^2 + c \quad \text{for} \quad n = 0, 1, 2, \dots
$$

Here, **c** is a complex number, and **z_n** is a sequence of complex numbers. The set consists of all values of $c$ for which the sequence $z_n$ does not tend to infinity as **n** increases. In other words, if the magnitude of **z_n** remains bounded (i.e., $ |z_n| \leq 2 $ for all **n**), then **c** is in the Mandelbrot set.

The program visualizes the Mandelbrot set by calculating the number of iterations it takes for the sequence $z_n$ to exceed a given threshold (e.g., $$ |z_n| > 2 $$). The number of iterations is mapped to a color using a custom colormap.

### Parameters:
- **c**: The complex number, which is represented by the coordinates on the screen (x, y).
- **z_n**: The complex sequence generated iteratively.
- **Max Iterations**: The maximum number of iterations to run for each point. If the sequence does not escape (i.e., $ |z_n| \leq 2 $) within the given number of iterations, the point is assumed to be part of the Mandelbrot set.
- **Escape Threshold**: Typically set to 2, the sequence is considered to have "escaped" if $$ |z_n| > 2 $$.

The iteration count for each point is normalized to a range [0, 1], which is then used to map the point to a color in the fractal.

### Colormap:
A custom colormap is used to represent the number of iterations. The color values are determined by the formula:
$$
\text{colormap}(t) = \left( 9(1 - t)t^3, 15(1 - t)^2t^2, 8.5(1 - t)^3t \right)
$$
where **t** is the normalized iteration count, ranging from 0 (for points in the Mandelbrot set) to 1 (for points that escape quickly).

## Features

- **GLSL Shaders**: Efficient computation of the Mandelbrot set using vertex and fragment shaders. The fragment shader calculates the Mandelbrot iterations for each pixel and applies the colormap.
- **Dynamic Zooming**: The zoom factor is adjusted using the mouse wheel. As the zoom level changes, the resolution of the fractal is dynamically scaled to ensure that the fractal remains sharp at any zoom level.
- **Panning**: The user can click and drag to pan the view across the fractal.
- **Interactive Interface**: The application responds to mouse events to allow real-time interaction with the fractal.

## Installation

To run this project, you need Python and the required dependencies. Install the necessary packages using `pip`:

```bash
pip install numpy vispy

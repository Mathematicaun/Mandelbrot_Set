import numpy as np
from vispy import app, gloo

# GLSL shader for Mandelbrot computation with colormap
vertex_shader = """
attribute vec2 a_position;
void main() {
    gl_Position = vec4(a_position, 0.0, 1.0);
}
"""

fragment_shader = """
uniform vec2 u_resolution;
uniform vec2 u_center;
uniform float u_zoom;
uniform int u_max_iter;

vec3 colormap(float t) {
    return vec3(
        9.0 * (1.0 - t) * t * t * t,
        15.0 * (1.0 - t) * (1.0 - t) * t * t,
        8.5 * (1.0 - t) * (1.0 - t) * (1.0 - t) * t
    );
}

void main() {
    vec2 c = u_center + (gl_FragCoord.xy / u_resolution - 0.5) * 2.0 / u_zoom;
    vec2 z = vec2(0.0, 0.0);
    int iter;
    for (iter = 0; iter < u_max_iter; ++iter) {
        float x = (z.x * z.x - z.y * z.y) + c.x;
        float y = (2.0 * z.x * z.y) + c.y;
        if ((x * x + y * y) > 4.0) break;
        z.x = x;
        z.y = y;
    }
    float t = float(iter) / float(u_max_iter); // Normalize iterations
    gl_FragColor = vec4(colormap(t), 1.0);
}
"""

# Create a canvas with VisPy
class MandelbrotCanvas(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self, title="Mandelbrot Zoom with Dynamic Resolution", keys="interactive", show=True)
        self.program = gloo.Program(vertex_shader, fragment_shader)
        
        # Set up geometry
        self.program["a_position"] = gloo.VertexBuffer(np.array([
            [-1, -1],
            [-1, 1],
            [1, -1],
            [1, 1]
        ], dtype=np.float32))
        
        self.zoom = 1.0
        self.center = (-0.5, 0.0)
        self.max_iter = 500

        # Initial resolution
        self.resolution_factor = 1.0
        self.set_dynamic_resolution()

        # Interaction variables
        self.dragging = False
        self.last_mouse_pos = None

        self.show()

    def set_dynamic_resolution(self):
        """Adjust resolution dynamically based on zoom."""
        width, height = self.size
        dynamic_res = (int(width * self.zoom), int(height * self.zoom))
        self.program["u_resolution"] = dynamic_res
        self.program["u_center"] = self.center
        self.program["u_zoom"] = self.zoom
        self.program["u_max_iter"] = self.max_iter

    def on_resize(self, event):
        gloo.set_viewport(0, 0, *self.physical_size)
        self.set_dynamic_resolution()

    def on_mouse_wheel(self, event):
        # Zoom in/out with the mouse wheel
        factor = 1.1 if event.delta[1] > 0 else 1 / 1.1
        self.zoom *= factor
        self.set_dynamic_resolution()
        self.update()

    def on_mouse_press(self, event):
        # Start dragging
        self.dragging = True
        self.last_mouse_pos = event.pos

    def on_mouse_release(self, event):
        # Stop dragging
        self.dragging = False

    def on_mouse_move(self, event):
        if self.dragging:
            # Pan by dragging the mouse
            dx = (event.pos[0] - self.last_mouse_pos[0]) / self.size[0] / self.zoom
            dy = (event.pos[1] - self.last_mouse_pos[1]) / self.size[1] / self.zoom
            self.center = (self.center[0] - dx, self.center[1] + dy)
            self.set_dynamic_resolution()
            self.last_mouse_pos = event.pos
            self.update()

    def on_draw(self, event):
        gloo.clear(color="black")
        self.program.draw("triangle_strip")


if __name__ == "__main__":
    canvas = MandelbrotCanvas()
    app.run()

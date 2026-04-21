import secrets
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider

class RandomSearchMath:
    def __init__(self):
        self.gamma3 = 0.8  
        self.gamma4 = 1.5 
        self.w = np.array([0.0, 0.0]) 
        self.current_x = np.array([0.0, 0.0])
        self.history = [self.current_x.copy()]

    def target_function(self, x):
        """f(x) = -x1 - 2x2 + x2^2"""
        return -x[0] - 2*x[1] + x[1]**2

    def in_boundaries(self, x):
        if x[0] < 0 or x[1] < 0: return False
        if 3*x[0] + 2*x[1] > 6: return False
        if x[0] + 2*x[1] > 4: return False
        return True
    
    def generate_probes(self, a, m):

        # gamma = np.random.rand(m)
        # print(gamma[0:5])
        gamma=[]
        for i in range(m):
            gamma.append( secrets.SystemRandom().random())
        gamma = np.array(gamma)
        # print(gamma[0:5])
        angles = 2 * np.pi * gamma
        
        xi_0 = np.column_stack((np.cos(angles), np.sin(angles)))
        
        xi = xi_0 + self.w
        print(self.w)
        
        xi /= np.linalg.norm(xi, axis=1)[:, np.newaxis]
        
        probes = self.current_x + a * xi
        
        return probes, xi
    
    def perform_step(self, a, m):
        probes, directions = self.generate_probes(a, m)
        
        valid_indices = [i for i, p in enumerate(probes) if self.in_boundaries(p)]
        if not valid_indices:
            return None, probes, None 

        f_current = self.target_function(self.current_x)
        best_idx = valid_indices[np.argmin([self.target_function(probes[i]) for i in valid_indices])]
        best_probe = probes[best_idx]
        best_dir = directions[best_idx]
        f_best = self.target_function(best_probe)

        if f_best < f_current:
            delta_f = f_best - f_current
            step_vec = -(best_dir / a) * delta_f
            x_new = self.current_x + step_vec

            if not self.in_boundaries(x_new):
                x_new = best_probe
            
            delta_x = x_new - self.current_x
            actual_df = self.target_function(x_new) - f_current
            self.w = self.gamma3 * self.w - self.gamma4 * delta_x * actual_df
            
            self.current_x = x_new
            self.history.append(self.current_x.copy())
            return x_new, probes, best_probe
        
        return None, probes, None




class Visualizer:
    def __init__(self, math_engine):
        self.engine = math_engine
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        plt.subplots_adjust(bottom=0.2)
        
        self.a_slider = Slider(plt.axes([0.15, 0.1, 0.25, 0.03]), 'Крок (a)', 0.01, 1.5, valinit=0.1)
        self.m_slider = Slider(plt.axes([0.55, 0.1, 0.25, 0.03]), 'Проби (m)', 5, 50, valinit=15, valfmt='%0.0f')
        
        self.btn_next = Button(plt.axes([0.8, 0.025, 0.1, 0.04]), 'Next Step')
        self.btn_next.on_clicked(self.update)
        
        self.draw_base_map()
        self.current_plot, = self.ax.plot([], [], 'ko-', label='Траєкторія')
        self.probe_dots = self.ax.scatter([], [], c='blue', s=20, alpha=0.5, label='Проби')
        self.circle = plt.Circle((0, 0), 0, color='green', fill=False, linestyle='--', alpha=0.3)
        self.ax.add_artist(self.circle)
        
        self.status_text = self.ax.text(-0.8, 3.2, '', fontsize=9, verticalalignment='top', 
                                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))

    def draw_base_map(self):
        # Лінії рівня f(x)
        x1, x2 = np.meshgrid(np.linspace(-1, 3.5, 100), np.linspace(-1, 3.5, 100))
        z = -x1 - 2*x2 + x2**2
        self.ax.contour(x1, x2, z, levels=25, cmap='viridis', alpha=0.4)
        
        # Область допустимих значень (Feasible region)
        pts = np.array([[0,0], [2,0], [1, 1.5], [0, 2]])
        polygon = plt.Polygon(pts, closed=True, color='gray', alpha=0.2, label='Допустима область')
        self.ax.add_patch(polygon)
        
        self.ax.set_xlim(-1, 3.5); self.ax.set_ylim(-1, 3.5)
        self.ax.set_xlabel('x1'); self.ax.set_ylabel('x2')
        self.ax.legend(loc='upper right')

    def update(self, event):
        a = self.a_slider.val
        m = int(self.m_slider.val)
        
        old_x = self.engine.current_x.copy()
        new_x, probes, best_p = self.engine.perform_step(a, m)
        
        # Оновлення візуалізації кола та проб
        self.circle.set_center(old_x)
        self.circle.set_radius(a)
        
        self.probe_dots.set_offsets(probes)
        colors = ['green' if self.engine.in_boundaries(p) else 'red' for p in probes]
        self.probe_dots.set_color(colors)
        
        # Оновлення траєкторії
        hist = np.array(self.engine.history)
        self.current_plot.set_data(hist[:, 0], hist[:, 1])
        
        # Текст статусу
        f_val = self.engine.target_function(self.engine.current_x)
        status = (f"Крок: {len(self.engine.history)-1}\n"
                  f"x: [{self.engine.current_x[0]:.3f}, {self.engine.current_x[1]:.3f}]\n"
                  f"f(x): {f_val:.4f}\n"
                  f"w: [{self.engine.w[0]:.2f}, {self.engine.w[1]:.2f}]")
        self.status_text.set_text(status)
        
        self.fig.canvas.draw_idle()

if __name__ == "__main__":
    math_ = RandomSearchMath()
    viz = Visualizer(math_)
    plt.show()
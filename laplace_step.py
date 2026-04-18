from manim import *
import numpy as np

class LaplaceToTimeStep(Scene):
    def construct(self):
        # Pure second order form TF (K/(s+p1)(s+p2))
        sigma1 = ValueTracker(-10.0)
        omega1 = ValueTracker(0.0)
        sigma2 = ValueTracker(-10.0)
        omega2 = ValueTracker(0.0)
        k = ValueTracker(1.0)

        # Setting for axis labels
        axis_num_size = 24
        axis_legend_size = 28
        axis_header_size = 28

        # Left Axis (S-Plane)
        s_axes = Axes (
            x_range=[-5, 2, 1],
            y_range=[-8, 8, 2],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": axis_num_size}
        ).shift(LEFT * 3)

        s_label = s_axes.get_axis_labels(
            x_label=MathTex("\\sigma", font_size=axis_legend_size), 
            y_label=MathTex("j\\omega", font_size=axis_legend_size)
        )
        s_title = Text("S-Domain (Laplace)", font_size=axis_header_size).next_to(s_axes, UP * 2)


        # Right Axis (Time-Plane)
        time_axes = Axes (
            x_range=[0, 10, 2],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": axis_num_size}
        ).shift(RIGHT * 3)

        time_label = time_axes.get_axis_labels(
            x_label=MathTex("t", font_size=axis_legend_size),
            y_label=MathTex("y(t)", font_size=axis_legend_size)
        )
        time_title = Text("Time Domain", font_size=axis_header_size).next_to(time_axes, UP * 2)

        # Transform solver
        def transform_to_time():
            p1 = sigma1.get_value() + 1j*omega1.get_value()
            p2 = sigma2.get_value() + 1j*omega2.get_value()
            gain = k.get_value()

            TF = f"\\frac{{{gain.real:.2f}}}{{(s {-p1:+.2f})(s {-p2:+.2f})}}"

            # Input using step function (1/s)
            # Using Residual methode
            graph_color = YELLOW
            if abs(p1-p2) < 0.001:
                c1 = gain/(p1*p2)
                c2 = -gain/(p1*p2)
                c3 = gain/p1
                graph_color = ORANGE

                total_eq = f"[{c1.real:.2f} {c2.real:+.2f}e^{{({p1:.2f})t}} {c3.real:+.2f}te^{{({p1:.2f})t}}]u(t)"
                def transform_t(t):
                    return 0 if t < 0 else c1 + +c2*np.exp(p1*t) + c3*t*np.exp(p1*t)
            else:
                if abs(p1.imag) > 0.001:
                    graph_color = BLUE
                c1 = gain/((-p1) * (-p1 + p2))
                c2 = gain/((-p2) * (-p2 + p1))
                c3 = gain/(p1*p2)

                total_eq = f"[{c3.real:.2f} {c1.real:+.2f}e^{{({p1:.2f})t}} {c2.real:+.2f}e^{{({p2:.2f})t}}]u(t)"
                def transform_t(t):
                    return 0 if t < 0 else c1*np.exp(p1 * t) + c2*np.exp(p2 * t) + c3
            
            graph_result = time_axes.plot(transform_t, color=graph_color)
            equation = MathTex(f"{TF} \\rightarrow {total_eq}", font_size=24).to_corner(DOWN)

            return VGroup(graph_result, equation)
        
        #  Updater and Redraw
        time_graph = always_redraw(transform_to_time)
        pole_draw = [
            always_redraw(lambda: MathTex(
                "\\times", 
                color=YELLOW, 
                font_size=30, 
                stroke_width=3
            ).move_to(s_axes.c2p(sigma1.get_value(), omega1.get_value()))
            ),
            always_redraw(lambda: MathTex(
                "\\times", 
                color=YELLOW, 
                font_size=30, 
                stroke_width=3
            ).move_to(s_axes.c2p(sigma2.get_value(), omega2.get_value()))
            )
        ]

        line_draw = [
            always_redraw(lambda: s_axes.get_lines_to_point(
                s_axes.c2p(sigma1.get_value(), omega1.get_value()), color=GRAY)
            ),
            always_redraw(lambda: s_axes.get_lines_to_point(
                s_axes.c2p(sigma2.get_value(), omega2.get_value()), color=GRAY)
            )
        ]

        # Play Animation
        self.play(
            Create(s_axes), Write(s_label), Write(s_title),
            Create(time_axes), Write(time_label), Write(time_title)
        )
        self.wait(1)


        for pole in pole_draw:
            self.play(FadeIn(pole))
        self.wait(0.5)

        for line in line_draw:
            self.play(FadeIn(line))
        self.wait(0.5)

        self.play(Create(time_graph))
        self.wait(1)

        def change_gain_or_pole(gain=None, s1=None, s2=None, t=1):
            re1 = sigma1.get_value() if s1 == None else s1.real
            im1 = omega1.get_value() if s1 == None else s1.imag
            re2 = sigma2.get_value() if s2 == None else s2.real
            im2 = omega2.get_value() if s2 == None else s2.imag
            k_new = k if gain == 0 else gain

            self.play(
                sigma1.animate.set_value(re1),
                omega1.animate.set_value(im1),
                sigma2.animate.set_value(re2),
                omega2.animate.set_value(im2),
                k.animate.set_value(k_new), 
                run_time=t
            )

        
        # Make sure that K (gain) is a real number
        # Make sure s1 and s2 is a complex conjugate (if it is a complex)
        change_gain_or_pole(1, -1, -3, 2)
        self.wait(1)

        change_gain_or_pole(1, -1, -1, 2)
        self.wait(1)

        change_gain_or_pole(1, -1 + 5j, -1 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(50, -1 + 5j, -1 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(25, -1 + 5j, -1 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(25, 5j, -5j, 2)
        self.wait(1)

        change_gain_or_pole(25, 1+ 5j, 1 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(25, -3+ 5j, -3 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(5, -3+ 5j, -3 - 5j, 2)
        self.wait(1)

        change_gain_or_pole(5, -3, -3, 2)
        self.wait(1)

        change_gain_or_pole(5, -10, -3, 2)
        self.wait(1)
       
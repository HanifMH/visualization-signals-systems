from manim import *
import numpy as py

class LaplaceToTimeImpulse(Scene):
    def construct(self):
        # Pure Second order TF
        # Using desired pole for easier demonstration 
        # (instead of using bounded root locus requirements)
        p1 = [ValueTracker(-10.0), ValueTracker(0.0)] # sigma + jomega
        p2 = [ValueTracker(-10.0), ValueTracker(0.0)]

        title = Text("Laplace <-> Time Domain (Impulse)", font_size=28).to_edge(UP)
        # Laplace Axes
        s_axes = Axes (
            x_range=[-5, 2, 1],
            y_range=[-8, 8, 2],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": 24}
        ).shift(LEFT * 3)

        s_label = s_axes.get_axis_labels(x_label=MathTex("\\sigma", font_size=28), y_label=MathTex("j\\omega", font_size=28))
        s_title = Text("S Domain (Laplace)", font_size=28).next_to(s_axes, UP * 2)

        # Time Axes
        time_axes = Axes (
            x_range=[0, 10, 1],
            y_range=[-2, 2, 1],
            x_length=5,
            y_length=5,
            axis_config={"include_numbers": True, "font_size": 24}
        ).shift(RIGHT * 3)

        time_label = time_axes.get_axis_labels(x_label=MathTex("t", font_size=28), y_label=MathTex("y(t)", font_size=28))
        time_title = Text("Time Domain", font_size=28).next_to(time_axes, UP * 2)

        pole_draw = [
            always_redraw(lambda: MathTex("\\times", color=YELLOW, font_size=30, stroke_width=3).move_to(s_axes.c2p(p1[0].get_value(), p1[1].get_value()))),
            always_redraw(lambda: MathTex("\\times", color=YELLOW, font_size=30, stroke_width=3).move_to(s_axes.c2p(p2[0].get_value(), p2[1].get_value())))
        ]

        line_draw = [
            always_redraw(lambda: s_axes.get_lines_to_point(s_axes.c2p(p1[0].get_value(), p1[1].get_value()), color=GRAY)),
            always_redraw(lambda: s_axes.get_lines_to_point(s_axes.c2p(p2[0].get_value(), p2[1].get_value()), color=GRAY))
        ]

        def time_transform():
            pole1 = [p1[0].get_value(), p1[1].get_value()]
            pole2 = [p2[0].get_value(), p2[1].get_value()]

            s1 = pole1[0] + 1j*pole1[1]
            s2 = pole2[0] + 1j*pole2[1]

            def transform_t(t):
                if (abs(pole1[1]) < 0.001 and abs(pole2[1]) < 0.001 
                and abs(pole1[0] - pole2[0]) < 0.001):
                    return t * np.exp(s1 * t)
                k1 = 1/(s1 - s2)
                k2 = 1/(s2 - s1)
                return k1*np.exp(s1 * t) + k2*np.exp(s2 * t)
            
            return time_axes.plot(transform_t, color=YELLOW, use_smoothing=True)
        
        time_graph = always_redraw(time_transform)

        self.play(
            Create(s_axes), Write(s_label), Write(s_title),
            Create(time_axes), Write(time_label), Write(time_title)
        )

        self.play(
            FadeIn(pole_draw[0]), FadeIn(pole_draw[1]), 
            FadeIn(line_draw[0]), FadeIn(line_draw[1]), Create(time_graph)
        )
        self.wait(1)

        # For correct animation, all poles must be symetrical about the real axis
        def change_s_pole(s1=None, s2=None, t=1):
            _x1 = s1.real if s1 is not None else p1[0].get_value()
            _y1 = s1.imag if s1 is not None else p1[1].get_value()
            _x2 = s2.real if s2 is not None else p2[0].get_value()
            _y2 = s2.imag if s2 is not None else p2[1].get_value()

            self.play(
                p1[0].animate.set_value(_x1),
                p1[1].animate.set_value(_y1),
                p2[0].animate.set_value(_x2),
                p2[1].animate.set_value(_y2),
                run_time=t
            )

        # To change trajectory to the desired pole, use change_s_pole(s1, s2)
        # Make sure s1 and s2 is a complex conjugate (if it is a complex)
        change_s_pole(-1, -3, 2)
        self.wait(1)

        change_s_pole(-1, -1, 2)
        self.wait(1)

        change_s_pole(-1 + 5j, -1 - 5j, 2)
        self.wait(1)

        change_s_pole(5j, -5j, 2)
        self.wait(1)

        change_s_pole(1j, -1j, 2)
        self.wait(1)

        change_s_pole(0, 0, 1)
        self.wait(1)

        change_s_pole(3j, -3j, 2)
        self.wait(1)

        change_s_pole(1+3j, 1-3j, 2)
        self.wait(1)

        change_s_pole(-1+3j, -1-3j, 2)
        self.wait(1)

        change_s_pole(-3+3j, -3-3j, 2)
        self.wait(1)

        change_s_pole(0, 0, 2)
        self.wait(1)

        change_s_pole(-3, -3, 2)
        self.wait(1)

        change_s_pole(-3, 1, 2)
        self.wait(5)

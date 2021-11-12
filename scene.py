from manim import *


# Displays basic propped cantilever under loading
class ProppedCantilever(Scene):
    def construct(self):
        circle1 = Circle(radius=0.06)
        circle2 = circle1.copy()
        rectangle = Rectangle(PINK, fill_opacity=0.5, height=0.1)
        prop = Triangle().scale(0.20).set_color(WHITE).shift(RIGHT * 2, DOWN * 0.5)
        circle1.shift(RIGHT * 2, DOWN).next_to(prop, DOWN, LEFT * 2).shift(LEFT * 0.1)
        circle2.next_to(circle1, RIGHT).next_to(prop, DOWN, LEFT * 2).shift(RIGHT * 0.1)
        wheel = Group(circle1, circle2)

        # Construction of the wall
        vline = Line(start=[0., 0.5, 0.], end=[0., -0.5, 0.]).align_to(rectangle, LEFT)
        dline1 = Line(start=[0, 0, 0], end=[0, -0.2, 0]).set_angle(70).next_to(vline, LEFT * 0.2)
        dline2 = dline1.copy().next_to(dline1, UP * 0.5)
        dline3 = dline1.copy().next_to(dline1, DOWN * 0.5)
        wall = Group(dline1, dline2, dline3, vline)

        # Construction of the floor
        hline = Line(start=[0.5, 0, 0.], end=[-0.5, 0, 0.]).align_to(circle1, DOWN).shift(RIGHT * 2)
        dline4 = dline1.copy().next_to(hline, DOWN * 0.2)
        dline5 = dline4.copy().shift(LEFT * 0.3)
        dline6 = dline4.copy().shift(RIGHT * 0.3)
        floor = Group(dline4, dline5, dline6, hline)

        # Loading
        arrow = Arrow(start=config.top, end=ORIGIN).scale(0.20).align_to(rectangle, UP)
        weight = Text("Weight of Life", slant=ITALIC, font_size=20).shift(DOWN)
        loading = Group(arrow, weight)

        # Playing animation
        self.play(FadeIn(rectangle))
        self.play(FadeIn(prop, wheel))
        self.play(FadeIn(wall, floor))
        self.play(FadeIn(loading))
        self.wait(1)


# This shows the formation of two hinges required for catastrophic collapse
class UpperBound(Scene):
    def construct(self):
        # Deformed beam
        rectangle1 = Rectangle(PINK, fill_opacity=0.5, height=0.1, width=1.5)
        rectangle2 = rectangle1.copy().shift(RIGHT * 1.5).rotate(0.2)
        rectangle1.rotate(-0.2)
        beam = Group(rectangle1, rectangle2)
        hinge1 = Circle(radius=0.05).set_fill(BLACK, opacity=1)
        hinge2 = hinge1.copy().shift(RIGHT * 0.75, DOWN * 0.15)
        framebox1 = SurroundingRectangle(hinge2, buff=.1)

        # Prop
        circle1 = Circle(radius=0.06)
        circle2 = circle1.copy()
        prop = Triangle().scale(0.20).set_color(WHITE).shift(RIGHT * 2, DOWN * 0.5)
        circle1.shift(RIGHT * 2, DOWN).next_to(prop, DOWN, LEFT * 2).shift(LEFT * 0.1)
        circle2.next_to(circle1, RIGHT).next_to(prop, DOWN, LEFT * 2).shift(RIGHT * 0.1)
        wheel = Group(prop, circle1, circle2)

        # Formation of wall
        vline = Line(start=[0., 0.5, 0.], end=[0., -0.5, 0.]).align_to(rectangle1, LEFT)
        hinge1.align_to(rectangle1, LEFT).shift(UP * 0.15)
        dline1 = Line(start=[0, 0, 0], end=[0, -0.2, 0]).set_angle(70).next_to(vline, LEFT * 0.2)
        dline2 = dline1.copy().next_to(dline1, UP * 0.5)
        dline3 = dline1.copy().next_to(dline1, DOWN * 0.5)
        wall = Group(dline1, dline2, dline3, vline, hinge1)

        # Formation of floor
        hline = Line(start=[0.5, 0, 0.], end=[-0.5, 0, 0.]).align_to(circle1, DOWN).shift(RIGHT * 2)
        dline4 = dline1.copy().next_to(hline, DOWN * 0.2)
        dline5 = dline4.copy().shift(LEFT * 0.3)
        dline6 = dline4.copy().shift(RIGHT * 0.3)
        floor = Group(dline4, dline5, dline6, hline)
        support = Group(wheel, floor).shift(RIGHT * 0.25, UP * 0.15)

        self.play(FadeIn(beam, wall, support))
        self.wait(1)
        self.play(FadeIn(hinge2))
        self.play(Create(framebox1))
        self.wait(1)

        # Annotation Angle
        rotation_center = LEFT
        theta_tracker = ValueTracker(20)
        line1 = Line(LEFT, RIGHT)
        line_moving = Line(LEFT, RIGHT)
        line_moving.rotate(
            theta_tracker.get_value() * DEGREES, about_point=rotation_center
        )
        a = Angle(line1, line_moving, radius=0.5, other_angle=False)
        tex = MathTex(r"\theta", font_size=40).move_to(
            Angle(
                line1, line_moving, radius=0.5 + 3 * SMALL_BUFF, other_angle=False
            ).point_from_proportion(0.3)
        )
        angle = Group(line1, line_moving, a, tex)
        angle.shift(RIGHT * 4)

        self.play(FadeIn(angle))
        self.wait()


# Displays the Upper Bound Work Done Equation
class UpperBoundEquation(Scene):
    def construct(self):
        compatibility = MathTex(r"\theta=2\delta/L", font_size=50)
        energy = MathTex(r"W\times\delta", r"=M_{p}2\theta+M_{p}\theta", r"=", r"6M_{p}/L", font_size=50)

        self.play(FadeIn(compatibility))
        self.play(FadeIn(energy.shift(DOWN)))
        framebox1 = SurroundingRectangle(energy[0], buff=.1)
        framebox2 = SurroundingRectangle(energy[3], buff=.1)
        self.play(
            Create(framebox1),
        )
        self.wait()
        self.play(
            ReplacementTransform(framebox1, framebox2),
        )
        self.wait()


# Displays the graph for the bending moment of the beam under loading
class ParticularEquilibriumGraph(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 1, 0.5],
            y_range=[-1, 1],
            x_length=6,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 1, 0.5)},
            y_axis_config={"numbers_to_include": np.arange(-1, 1, 0.5)},
            tips=False,
        )
        labels = ax.get_axis_labels(
            x_label="length(l)", y_label="B.M.(WL/4)"
        )

        x_vals = [0, 0.5, 1]
        y_vals = [0, -1, 0]
        graph = ax.get_line_graph(x_values=x_vals, y_values=y_vals)

        self.play(FadeIn(ax, labels, graph))


# Displays the graph for the bending moment of the beam under self-stress, due to structural indeterminacy
class SelfStress(Scene):
    def construct(self):
        ax = Axes(
            x_range=[0, 1.5, 0.5],
            y_range=[0, 1.5, 0.5],
            x_length=6,
            y_length=6,
            x_axis_config={"numbers_to_include": np.arange(0, 1, 0.5)},
            y_axis_config={"numbers_to_include": np.arange(0, 1, 0.5)},
            tips=False,
        )
        labels = ax.get_axis_labels(
            x_label="length(l)", y_label="moment(M)"
        )
        x_vals = [0, 1]
        y_vals = [1, 0]
        graph = ax.get_line_graph(x_values=x_vals, y_values=y_vals)

        self.play(FadeIn(ax, labels, graph))

%%manim -ql -v WARNING RightTriangleScene

from manim import *
import numpy as np

def create_square_on_line(line: Line) -> Square:
    start = line.get_start()
    end = line.get_end()

    line_vector = end - start
    length = np.linalg.norm(line_vector)
    unit_vector = line_vector / length

    perp_up = np.array([-unit_vector[1], unit_vector[0], 0])

    sq = Square(side_length=length)
    sq.rotate(line.get_angle())

    line_center = line.get_center()
    square_center = line_center + (length / 2) * perp_up
    sq.move_to(square_center)

    return sq

class RightTriangleScene(Scene):
    def construct(self):
        A = np.array([0, 4, 0])
        B = np.array([3, 0, 0])
        C = np.array([0, 0, 0])
        line_a = Line(B, C, color=BLUE)
        line_b = Line(C, A, color=BLUE)
        line_c = Line(A, B, color=BLUE)

        line_a_prime = Line(C, B, color=BLUE)

        triangle_fill = Polygon(A, B, C, color=BLUE, fill_opacity=0.5, stroke_width=0)

        label_a = MathTex("A").next_to(A, UP, buff=0.2)
        label_b = MathTex("B").next_to(B, DOWN, buff=0.2)
        label_c = MathTex("C").next_to(C, DOWN, buff=0.2)

        label_side_a = MathTex("a").next_to(line_a.get_center(), DOWN, buff=0.2)
        label_side_b = MathTex("b").next_to(line_b.get_center(), LEFT, buff=0.2)
        label_side_c = MathTex("c").next_to(line_c.get_center(), RIGHT, buff=0.2)

        right_angle = RightAngle(line_b, line_a_prime, length=0.4, color=BLUE)

        triangle_group = VGroup(
            triangle_fill, line_a, line_b, line_c,
            label_a, label_b, label_c, right_angle,
            label_side_a, label_side_b, label_side_c
        )

        title = MathTex(r"a^2+b^2=c^2", font_size=48)
        title_rearranged = MathTex(r"c=\sqrt{a^2+b^2}", font_size=48)

        title.move_to(RIGHT*3)
        title_rearranged.move_to(RIGHT*3)

        triangle_group.move_to(ORIGIN)
        self.play(Create(triangle_group))
        self.wait(1)

        self.play(triangle_group.animate.shift(LEFT*3))
        self.play(Write(title))
        self.wait(1)
        self.play(Transform(title, title_rearranged))
        self.wait(1)
        self.play(triangle_group.animate.scale(0.5))
        self.wait(1)

        a_sq = create_square_on_line(line_a)
        b_sq = create_square_on_line(line_b)
        c_sq = create_square_on_line(line_c)

        sq_group = VGroup(
            a_sq, b_sq, c_sq
        )

        self.play(
          Create(sq_group),
          label_a.animate.shift(np.array([-0.1, 0.1, 0])),
          label_b.animate.shift(np.array([0.2, -0.1, 0])),
          label_c.animate.shift(np.array([-0.2, -0.1, 0]))
        )
        self.wait(2)

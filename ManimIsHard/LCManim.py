%%manim -ql -v WARNING LCCircuitDiagramFixed

class LCCircuitDiagramFixed(Scene):
    def construct(self):
        def create_vertical_capacitor(width=1.0, separation=0.3):
            cap = VGroup()
            cap.add(Line(LEFT * (width / 2) + UP * (separation / 2), RIGHT * (width / 2) + UP * (separation / 2), stroke_width=5))
            cap.add(Line(LEFT * (width / 2) + DOWN * (separation / 2), RIGHT * (width / 2) + DOWN * (separation / 2), stroke_width=5))
            cap.add(Line(UP * (separation / 2), UP * 0.8, stroke_width=4))
            cap.add(Line(DOWN * (separation / 2), DOWN * 0.8, stroke_width=4))
            return cap

        def create_vertical_inductor(coils=4, radius=0.3, spacing=0.3):
            ind = VGroup()
            total_length = coils * spacing
            start_y = total_length / 2
            
            coil_func = ParametricFunction(
                lambda t: np.array([
                    radius * abs(np.sin(t)),
                    start_y - (t / (coils * PI)) * total_length,
                    0
                ]),
                t_range=[0, coils * PI],
                stroke_width=4,
                color=WHITE
            )
            
            top_lead = Line(UP * start_y + UP * 0.4, UP * start_y, stroke_width=4)
            bottom_lead = Line(DOWN * start_y, DOWN * start_y + DOWN * 0.4, stroke_width=4)
            ind.add(top_lead, coil_func, bottom_lead)
            return ind

        capacitor = create_vertical_capacitor().move_to(LEFT * 2.5)
        inductor = create_vertical_inductor().move_to(RIGHT * 2.8)
        
        top_wire = Line(LEFT * 2.5 + UP * 2, RIGHT * 2.65 + UP * 2, stroke_width=4)
        bottom_wire = Line(LEFT * 2.5 + DOWN * 2, RIGHT * 2.65 + DOWN * 2, stroke_width=4)
        cap_to_top = Line(LEFT * 2.5 + UP * 0.8, LEFT * 2.5 + UP * 2, stroke_width=4)
        cap_to_bottom = Line(LEFT * 2.5 + DOWN * 0.8, LEFT * 2.5 + DOWN * 2, stroke_width=4)
        ind_to_top = Line(RIGHT * 2.65 + UP * 1.0, RIGHT * 2.65 + UP * 2, stroke_width=4)
        ind_to_bottom = Line(RIGHT * 2.65 + DOWN * 1.0, RIGHT * 2.65 + DOWN * 2, stroke_width=4)

        wiring = VGroup(top_wire, bottom_wire, cap_to_top, cap_to_bottom, ind_to_top, ind_to_bottom)

        c_label = MathTex("C", color=BLUE).next_to(capacitor, LEFT, buff=0.4).scale(1.2)
        l_label = MathTex("L", color=RED).next_to(inductor, RIGHT, buff=0.4).scale(1.2)
        title = Text("LC Tank Circuit", font_size=36).to_edge(UP, buff=0.5)

        # Path extends completely from the physical top plate surface to the bottom plate surface
        circuit_path = VMobject().set_points_as_corners([
            LEFT * 2.5 + UP * 0.15,   
            LEFT * 2.5 + UP * 2.0,    
            RIGHT * 2.65 + UP * 2.0,  
            RIGHT * 2.65 + DOWN * 2.0,
            LEFT * 2.5 + DOWN * 2.0,  
            LEFT * 2.5 + DOWN * 0.15  
        ])

        time_tracker = ValueTracker(0)
        
        # Increased dot count and introduced virtual boundaries to prevent end-gaps at peaks
        num_dots = 40
        shift_amplitude = 0.07
        electrons = always_redraw(lambda: VGroup(*[
            Dot(
                point=circuit_path.point_from_proportion(
                    np.clip(
                        -shift_amplitude + (i / (num_dots - 1)) * (1 + 2 * shift_amplitude) + shift_amplitude * np.sin(1 * time_tracker.get_value()),
                        0.0,
                        1.0
                    )
                ),
                color=YELLOW,
                radius=0.07
            )
            for i in range(num_dots)
        ]))

        # Dynamic Vector Arrows & Labels adjacent to the bottom wire
        q_label = MathTex("q(t)", color=YELLOW).scale(0.8).move_to(LEFT * 1.2 + DOWN * 2.4)
        i_label = MathTex("I(t)", color=GREEN).scale(0.8).move_to(LEFT * 1.2 + DOWN * 2.9)

        # Static anchor base point for the vectors
        base_x = 0.8

        def get_displacement_arrow():
            val = np.sin(time_tracker.get_value())
            if abs(val) < 0.05:
                return VMobject()
            # Start is fixed at base_x, only the tip (end) moves
            return Arrow(
                start=RIGHT * base_x + DOWN * 2.4,
                end=RIGHT * base_x + LEFT * (val * 1.2) + DOWN * 2.4,
                color=YELLOW,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25
            )

        def get_current_arrow():
            val = np.cos(time_tracker.get_value())
            if abs(val) < 0.05:
                return VMobject()
            # Start is fixed at base_x, only the tip (end) moves
            return Arrow(
                start=RIGHT * base_x + DOWN * 2.9,
                end=RIGHT * base_x + RIGHT * (val * 1.2) + DOWN * 2.9,
                color=GREEN,
                buff=0,
                stroke_width=4,
                max_tip_length_to_length_ratio=0.25
            )

        displacement_vector = always_redraw(get_displacement_arrow)
        current_vector = always_redraw(get_current_arrow)

        # --- Dynamic Energy Bars ---
        # Outer border settings
        bar_w = 0.25
        bar_h = 1.5
        inner_padding = 0.04
        max_fill_h = bar_h - (inner_padding * 2)
        fill_w = bar_w - (inner_padding * 2)

        # Static Outlines
        ec_bar_outline = Rectangle(width=bar_w, height=bar_h, color=BLUE_B).next_to(c_label, LEFT, buff=0.4)
        el_bar_outline = Rectangle(width=bar_w, height=bar_h, color=RED_B).next_to(l_label, RIGHT, buff=0.4)

        # Dynamic Fills locked to bottom reference point of the static outlines
        ec_bar_fill = always_redraw(lambda: 
            Rectangle(
                width=fill_w, 
                height=max(0.01, max_fill_h * (np.sin(time_tracker.get_value()) ** 2)), 
                fill_color=BLUE, 
                fill_opacity=0.8, 
                stroke_width=0
            ).move_to(
                ec_bar_outline.get_bottom() + UP * (inner_padding + max(0.01, max_fill_h * (np.sin(time_tracker.get_value()) ** 2)) / 2),
                coor_mask=np.array([1, 1, 0])
            )
        )

        el_bar_fill = always_redraw(lambda: 
            Rectangle(
                width=fill_w, 
                height=max(0.01, max_fill_h * (np.cos(time_tracker.get_value()) ** 2)), 
                fill_color=RED, 
                fill_opacity=0.8, 
                stroke_width=0
            ).move_to(
                el_bar_outline.get_bottom() + UP * (inner_padding + max(0.01, max_fill_h * (np.cos(time_tracker.get_value()) ** 2)) / 2),
                coor_mask=np.array([1, 1, 0])
            )
        )

        ec_title = MathTex("E_C", color=BLUE).scale(0.8).next_to(ec_bar_outline, UP, buff=0.2)
        el_title = MathTex("E_L", color=RED).scale(0.8).next_to(el_bar_outline, UP, buff=0.2)

        # --- Dynamic Total Energy Bar (Composite Blue + Red, Center of Screen) ---
        etot_w = 2.5
        etot_h = 0.25
        etot_max_fill_w = etot_w - (inner_padding * 2)
        etot_fill_h = etot_h - (inner_padding * 2)

        # Center Container Box
        etot_bar_outline = Rectangle(width=etot_w, height=etot_h, color=WHITE).move_to(DOWN * 0.5)
        
        # Left Segment (Blue - EC contribution)
        etot_blue_fill = always_redraw(lambda:
            Rectangle(
                width=max(0.01, etot_max_fill_w * (np.sin(time_tracker.get_value()) ** 2)),
                height=etot_fill_h,
                fill_color=BLUE,
                fill_opacity=0.8,
                stroke_width=0
            ).move_to(
                etot_bar_outline.get_left() + RIGHT * (inner_padding + max(0.01, etot_max_fill_w * (np.sin(time_tracker.get_value()) ** 2)) / 2),
                coor_mask=np.array([1, 1, 0])
            )
        )

        # Right Segment (Red - EL contribution)
        etot_red_fill = always_redraw(lambda:
            Rectangle(
                width=max(0.01, etot_max_fill_w * (np.cos(time_tracker.get_value()) ** 2)),
                height=etot_fill_h,
                fill_color=RED,
                fill_opacity=0.8,
                stroke_width=0
            ).move_to(
                etot_bar_outline.get_right() + LEFT * (inner_padding + max(0.01, etot_max_fill_w * (np.cos(time_tracker.get_value()) ** 2)) / 2),
                coor_mask=np.array([1, 1, 0])
            )
        )

        etot_brace = Brace(etot_bar_outline, UP, buff=0.08)
        etot_title = MathTex("E_{tot}", color=WHITE).scale(0.8).next_to(etot_brace, UP, buff=0.08)


        # --- Scene Animations ---
        self.play(Write(title))
        self.wait(0.3)
        self.play(Create(wiring), Create(capacitor), Create(inductor), run_time=2)
        self.play(
            FadeIn(c_label, shift=RIGHT * 0.2),
            FadeIn(l_label, shift=LEFT * 0.2),
            capacitor.animate.set_color(BLUE),
            inductor.animate.set_color(RED),
            run_time=1
        )
        
        # Introduce the vectors, energy bars, and labels
        self.play(
            Write(q_label),
            Write(i_label),
            Create(ec_bar_outline),
            Create(el_bar_outline),
            Write(ec_title),
            Write(el_title),
            Create(etot_bar_outline),
            Create(etot_brace),
            Write(etot_title),
            run_time=0.8
        )

        self.play(
            FadeIn(electrons, shift=UP * 0.2),
            Create(displacement_vector),
            Create(current_vector),
            GrowFromCenter(ec_bar_fill),
            GrowFromCenter(el_bar_fill),
            FadeIn(etot_blue_fill),
            FadeIn(etot_red_fill),
            run_time=1.2,
            rate_func=exponential_decay
        )
        self.play(time_tracker.animate.set_value(8 * np.pi), run_time=12, rate_func=linear)
        self.wait(1)
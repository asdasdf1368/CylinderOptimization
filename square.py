from manim import *

class Introduction(ThreeDScene):
    def construct(self):
        # Cylinder
        cylinder = Cylinder(resolution=32, fill_color=BLUE, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        cylinder.rotate(PI/2, [1, 0, 0]).scale([1, 1.5, 1])

        self.play(GrowFromCenter(cylinder))
        self.wait(1.5)

        self.play(cylinder.animate.scale([1.5, 0.5, 1]))
        self.wait(0.9)

        # Slap a question mark on that cylinder
        question_tex = Tex("?").scale(5).next_to(cylinder, OUT)
        self.play(LaggedStart(
                cylinder.animate.scale([0.75, 2, 1]),
                Write(question_tex),
                lag_ratio=0.25
            )
        )
        self.wait()

        self.play(FadeOut(VGroup(cylinder, question_tex)))

        definition_tex = Paragraph(
            "A volume-optimized object \n" 
            "is one that maximizes its \n"
            "volume, given a constraint \n"
            "on its surface area.",
            font_size=40, alignment='center').to_corner(UP + RIGHT, buff=1)
        

        # Growing Cube Section
        side_length = ValueTracker(1)
        
        cube = Cube(color=BLUE, fill_opacity=0.5, stroke_width=2, side_length=3).shift(UP * 1.25)

        # Number line for surface area
        surface_area_nl = NumberLine(
            x_range=[0, 54, 6],
            length=6,
            label_direction=DOWN,
        ).next_to(cube, DOWN, buff=1.5)

        def get_surface_area_nl_pos():
            return surface_area_nl.n2p(6 * (side_length.get_value() ** 2))

        # Pointer for surface area number line. What's a *pointer??
        surface_area_arrow = LabeledArrow(
            "S", 
            start=get_surface_area_nl_pos() + UP * 2, 
            end=get_surface_area_nl_pos(), 
            label_position=0.7,
            label_frame=False,
            frame_fill_opacity=0,
            max_stroke_width_to_length_ratio=0, 
            buff=0, 
            color=WHITE)

        # Number line for volume
        volume_nl = NumberLine(
            x_range=[0, 36, 6],
            length=6,
            label_direction=UP,
        ).next_to(surface_area_nl, DOWN, buff=1)

        def get_volume_nl_pos():
            return volume_nl.n2p(side_length.get_value() ** 3)

        # Arrow to show value of volume on the number line
        volume_arrow = LabeledArrow(
            "V", 
            start=get_volume_nl_pos() + UP * 2, 
            end=get_volume_nl_pos(), 
            label_position=0.7,
            label_frame=False,
            frame_fill_opacity=0,
            max_stroke_width_to_length_ratio=0, 
            buff=0, 
            color=WHITE)

        # Do some setting up
        cube.set_width(side_length.get_value())
        VGroup(cube, surface_area_nl, volume_nl, surface_area_arrow, volume_arrow).to_edge(LEFT)
        self.play(
            Create(VGroup(cube, surface_area_arrow, volume_arrow), run_time=0.5), 
            DrawBorderThenFill(VGroup(surface_area_nl, volume_nl), run_time=0.5),
        )

        # Add updaters
        surface_area_arrow.add_updater(lambda m: m.put_start_and_end_on(
            get_surface_area_nl_pos() + UP * 2, get_surface_area_nl_pos()))
        volume_arrow.add_updater(lambda m: m.put_start_and_end_on(
            get_volume_nl_pos() + UP * 2, get_volume_nl_pos()))
        cube.add_updater(lambda m: m.set_width(side_length.get_value()))
        
        # I love hardcoding
        self.play(
            Write(definition_tex),
            side_length.animate.set_value(3), 
            run_time=3
        )
        self.play(side_length.animate.set_value(2.9), run_time=1)
        self.play(side_length.animate.set_value(3), run_time=1)
        self.play(side_length.animate.set_value(2.9), run_time=1)
        self.play(side_length.animate.set_value(3), run_time=1)
        self.play(side_length.animate.set_value(2.9), run_time=1)
        self.play(side_length.animate.set_value(3), run_time=1)
        self.play(FadeOut(cube, surface_area_arrow, volume_arrow, surface_area_nl, volume_nl, definition_tex))

class SquareOptimization(ThreeDScene):
    def construct(self):
        # Cylinder
        cylinder = Cylinder(resolution=32, fill_color=BLUE, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        cylinder.rotate(PI/2, [1, 0, 0]).scale([1, 1.5, 1])

        # Slap a question mark on that cylinder
        question_tex = Tex("?").scale(5).next_to(cylinder, OUT)
        self.play(FadeIn(cylinder, question_tex))
        self.wait(4)
        self.play(FadeOut(cylinder, question_tex))

        # Create a square and shift it to the left
        square = Square(color=BLUE, fill_opacity=0.5).scale(2)
        self.play(Create(square))

        self.wait(8)
        self.play(square.animate.shift(LEFT * 4))
        self.wait()

        # Create perimeter formula next to the square
        perimeter_tex = MathTex("P", "=", "2l", "+", "2", "w").next_to(square, RIGHT * 4)
        self.play(Write(perimeter_tex), square.animate.set_stroke(RED_B))
        self.play(square.animate.set_stroke(BLUE))

        # Create perimeter formula next to the perimeter formula
        area_tex = MathTex("A", "=", "l", "w").next_to(perimeter_tex, RIGHT * 5)
        self.play(Write(area_tex), square.animate.set_fill(RED_B), run_time=1)
        self.play(square.animate.set_fill(BLUE))
        self.wait(2)

        self.play(Circumscribe(area_tex))
        self.wait(2.5)

        self.play(Circumscribe(perimeter_tex))
        self.wait(5.5)
        
        self.play(Indicate(area_tex[2]))
        self.play(Indicate(area_tex[3]))
        self.wait(7)

        # Indicate and isolate of w
        self.play(Indicate(perimeter_tex[5]))
        self.wait()

        # Display the isolation of w
        isolated_w_tex = MathTex("w", "=", R"\frac{P - 2l}{2}").next_to(perimeter_tex, DOWN, buff=0.1)
        self.play(
            TransformMatchingTex(perimeter_tex.copy(), isolated_w_tex),
            perimeter_tex.animate.shift(UP * isolated_w_tex.height * 0.5)
        )
        self.wait()

        # Indicate w's in both formulas
        self.play(
            Indicate(area_tex[3]),
            Indicate(isolated_w_tex[0])
        )
        self.wait()

        # Create area formula where w is subsituted
        substituted_area_tex = MathTex("A", "=", "l", R"\left(", R"\frac{P - 2l}{2}", R"\right)")
        substituted_area_tex.move_to(VGroup(perimeter_tex, area_tex, isolated_w_tex)).shift(DOWN)

        # Show both isolated w and area converging into the subsitution formula
        equation_group = VGroup(perimeter_tex, area_tex, isolated_w_tex)
        self.play(
            equation_group.animate.next_to(substituted_area_tex, UP * 1.5),
            TransformMatchingShapes(area_tex.copy(), substituted_area_tex[:3]),
            TransformMatchingShapes(isolated_w_tex[2].copy(), substituted_area_tex[4]),
            FadeIn(substituted_area_tex[3], substituted_area_tex[5])
        )
        self.wait()

        # The final result and circumscribe it
        final_area_tex = MathTex("A", "=", R"\frac{1}{2}", R"\left(", "lP-2l^2", R"\right)")
        final_area_tex.move_to(substituted_area_tex).shift(DOWN * 0.75)

        equation_group.add(substituted_area_tex)
        self.play(
            equation_group.animate.next_to(final_area_tex, UP),
            TransformMatchingTex(substituted_area_tex.copy(), final_area_tex)
        )
        self.wait()
        self.play(Circumscribe(final_area_tex))
        self.wait()

        # Fade out to introduce graph
        self.play(
            FadeOut(equation_group, square),  
            final_area_tex.animate.to_corner(UP + RIGHT)
        )

        # Axis for area
        axes = Axes(
            x_range=[0, 11, 1],
            y_range=[0, 11, 1],
            axis_config={"include_numbers": True, "color": BLUE},
        ).scale(0.8).to_edge(UP, buff=0.75)
        labels = axes.get_axis_labels(x_label='l', y_label='A')

        p_vt = ValueTracker(4)

        graph = always_redraw(lambda: axes.plot(
            lambda l: 1 / 2 * (l * p_vt.get_value() - 2 * l**2), 
            x_range=[0, p_vt.get_value() / 2], 
            color=WHITE)
        )

        # Numberline for constant P
        p_nl = NumberLine(
            x_range=[0, 20, 5],
            length=6,
            include_numbers=True,
            color=WHITE,
        ).next_to(axes, DOWN, buff=1)

        def get_p_nl_pos():
            return p_nl.n2p(p_vt.get_value())

        # Arrow to show value of P on the numberline
        arrow = LabeledArrow(
            "P", 
            start=get_p_nl_pos() + UP * 2, 
            end=get_p_nl_pos(), 
            label_position=0.7,
            label_frame=False,
            frame_fill_opacity=0,
            max_stroke_width_to_length_ratio=0, 
            buff=0, 
            color=WHITE)

        # Display the graph
        self.play(
            DrawBorderThenFill(axes),
            DrawBorderThenFill(p_nl),
            Create(labels),
            Create(graph),
            Create(arrow)
        )

        # Add an updater after drawing the arrow because it breaks stuff! Fun! (This was before I made Introduction)
        arrow.add_updater(lambda m: m.put_start_and_end_on(get_p_nl_pos() + UP * 2, get_p_nl_pos()))

        # Go from 16 to 4 to 9
        self.play(p_vt.animate.set_value(16), run_time=2.5)
        self.play(p_vt.animate.set_value(4), run_time=2.5)
        self.play(p_vt.animate.set_value(9), run_time=1.75)
        self.wait()

        # Fade out the graph, but keep the area formula
        self.play(
            FadeOut(axes, labels, graph, p_nl, arrow),
            final_area_tex.animate.move_to(ORIGIN).to_edge(UP)
        )

        # Group for the steps of the derivative of the area formula
        derivative_area_tex = Group(
            MathTex(R"\frac{dA}{dl}", "=", R"\frac{1}{2}", R"\left(", "P-4l", R"\right)"),
            MathTex(R"\frac{dA}{dl}", "=", R"\frac{1}{2}", R"\left(", "P-4l", R"\right)", "=0"),
            MathTex("P-4l=0"),
            MathTex(R"\frac{P}{4}", "=", "l")
        )
        derivative_area_tex.next_to(final_area_tex, DOWN, buff=1)
        
        self.play(Write(derivative_area_tex[0]))
        self.wait()

        # The first element sole purpose is to animate a =0 for the second element
        self.play(TransformMatchingTex(derivative_area_tex[0], derivative_area_tex[1]))
        self.wait(3)

        # Remove the first element and now we can align things
        derivative_area_tex.remove(derivative_area_tex[0])
        derivative_area_tex.arrange(DOWN, buff=0.5).next_to(final_area_tex, DOWN, buff=1)

        # Display the next derivative steps
        for tex in derivative_area_tex[1:]:
            self.play(Write(tex))
        self.wait(2.5)

        self.play(Circumscribe(derivative_area_tex[2]))
        self.wait(3)

        # Perimeter formula where we subsitute the result from the area formula
        perimeter_sub_tex = Group(
            MathTex("P", "=", "2", "l", "+2w"),
            MathTex("P", "=", "2", R"\left(", R"\frac{P}{4}", R"\right)", "+2w"),
            MathTex("P", "=", R"\frac{1}{2}", "P", "+2w"),
            MathTex(R"\frac{1}{2}P", "=", "2w"),
            MathTex(R"\frac{P}{4}", "=", "w")
        )
        perimeter_sub_tex.to_edge(RIGHT, buff=1).to_edge(UP)

        self.play(Group(derivative_area_tex, final_area_tex).animate.to_edge(LEFT, buff=1))
        self.wait()

        self.play(Write(perimeter_sub_tex[0]))
        self.wait()

        # Indicate l's
        self.play(Indicate(derivative_area_tex[2][2]), Indicate(perimeter_sub_tex[0][3]))

        # Animate the replacement of l to p/4 from the area formula, sole purpose of first element
        self.play(
            ReplacementTransform(derivative_area_tex[2][0].copy(), perimeter_sub_tex[1][4]),
            TransformMatchingShapes(perimeter_sub_tex[0], VGroup(perimeter_sub_tex[1][:4], perimeter_sub_tex[1][5:]))
        )
        self.wait()

        # Remove the first element and now we can align things
        perimeter_sub_tex.remove(perimeter_sub_tex[0])
        perimeter_sub_tex.arrange(DOWN, buff=0.5).to_edge(RIGHT, buff=1).to_edge(UP)

        # Display the next steps
        for tex in perimeter_sub_tex[1:]:
            self.play(Write(tex))
        self.wait()

        self.play(Circumscribe(perimeter_sub_tex[3]))
        self.wait(4)

        # Circumscribe both final area and perimeter equations
        self.play(Circumscribe(derivative_area_tex[2]), Circumscribe(perimeter_sub_tex[3]))

        # Display the final equation with the help of the area and perimeter equation
        final_tex = MathTex("l", "=", "w").to_edge(DOWN, buff=2).set_color(BLUE).scale(1.5)
        self.play(
            ReplacementTransform(derivative_area_tex[2][2].copy(), final_tex[0]),
            ReplacementTransform(perimeter_sub_tex[3][2].copy(), final_tex[2]),
            FadeIn(final_tex[1])
        )
        self.wait(3)
        self.play(FadeOut(final_area_tex, derivative_area_tex, perimeter_sub_tex, final_tex))
        self.wait(2)

def create_labled_brace(mobject, label, direction):
    """
    Creates a labeled brace around a given mobject.

    Args:
    mobject (Mobject): The Mobject to apply the brace to.
    label (str): The label to display next to the brace.
    direction (np.ndarray): A 3D vector specifying the direction of the brace. 

    Returns:
    VGroup: A VGroup containing the brace[0] and the label[1].
    """
    brace = Brace(mobject, direction=direction)
    brace_label = brace.get_tex(label)
    return VGroup(brace, brace_label)

class CylinderPrediction(ThreeDScene):
    def construct(self):
        # Cube!!
        cube = Cube(color=BLUE, fill_opacity=0.5, stroke_width=4)

        self.play(GrowFromCenter(cube))
        self.wait(9)

        # Get the faces of the cube
        faces = cube.family_members_with_points()

        # Animate the cube being unwrapped (moving faces)
        self.play(
            faces[0].animate.move_to([-4, 2, 0]),
            faces[1].animate.move_to([0, 2, 0]),
            faces[2].animate.move_to([4, 2, 0]).rotate(PI/2, [0, 1, 0]),
            faces[3].animate.move_to([-4, -2, 0]).rotate(PI/2, [0, 1, 0]),
            faces[4].animate.move_to([0, -2, 0]).rotate(PI/2, [1, 0, 0]),
            faces[5].animate.move_to([4, -2, 0]).rotate(PI/2, [1, 0, 0]),
        )
        self.wait(5)

        # Cube!! But with only strokes
        transparent_cube = Cube(color=BLUE, fill_opacity=0, stroke_width=4)
        self.play(ReplacementTransform(cube, transparent_cube))
        cube = transparent_cube

        # Red cylinder, put inside cube
        cylinder = Cylinder(resolution=32, fill_color=RED, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        cylinder.shift(UP * 7).rotate(PI/2, [1, 0, 0])
        self.play(
            cylinder.animate.move_to(cube)
        )
        self.wait()

        # Move the cublyinder to the side (haha get it?)
        self.play(Group(cylinder, cube).animate.to_edge(LEFT, buff=3).scale(1.5))
        self.wait()

        d_equal_h_tex = Group(
            MathTex("d", "=", "s"),
            MathTex("h", "=", "s"),
            MathTex("d", "=", "h"),
        ).shift(RIGHT * 3).scale(1.5)

        s_group = create_labled_brace(cylinder, "s", UP * 2)
        d_group = create_labled_brace(cylinder, "d", DOWN * 2)
        self.play(Write(s_group), Write(d_group))
        self.play(Indicate(s_group[1]), Indicate(d_group[1]))

        self.play(
            FadeIn(d_equal_h_tex[0][1]),
            ReplacementTransform(s_group[1].copy(), d_equal_h_tex[0][2]),
            ReplacementTransform(d_group[1].copy(), d_equal_h_tex[0][0])
        )
        self.wait()

        h_group = create_labled_brace(cylinder, "h", RIGHT * 2)
        self.play(Write(h_group))
        self.play(Indicate(s_group[1]), Indicate(h_group[1]))

        d_equal_h_tex[1].move_to(d_equal_h_tex[0]).shift(DOWN * 0.5)
        self.play(
            d_equal_h_tex[0].animate.shift(UP * 0.5),
            FadeIn(d_equal_h_tex[1][1]),
            ReplacementTransform(s_group[1].copy(), d_equal_h_tex[1][2]),
            ReplacementTransform(h_group[1].copy(), d_equal_h_tex[1][0])
        )
        self.wait(2)

        d_equal_h_tex[2].move_to(d_equal_h_tex[1]).shift(DOWN * 0.5)
        self.play(
            Group(d_equal_h_tex[0], d_equal_h_tex[1]).animate.shift(UP * 0.5),
            FadeIn(d_equal_h_tex[2][1]),
            TransformMatchingShapes(d_equal_h_tex[0][0].copy(), d_equal_h_tex[2][0]),
            TransformMatchingShapes(d_equal_h_tex[1][0].copy(), d_equal_h_tex[2][2])
        )
        self.wait(1.5)

        self.play(Circumscribe(d_equal_h_tex[2]))
        self.wait()
        self.play(FadeOut(cube, cylinder, s_group, d_group, h_group, d_equal_h_tex))

class MiniCoke(ThreeDScene):
    def construct(self):
        img = ImageMobject("imgs\coke.jpg")
        img.height = 5

        coke = Cylinder(resolution=32, fill_color=RED, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        coke.rotate(PI/2, [1, 0, 0]).scale([5.8 / 5, 10.3 / 5, 1]).to_edge(LEFT, buff=2.5)

        self.play(FadeIn(img))
        self.wait(5)
        self.play(
            img.animate.to_edge(RIGHT, buff=2.5),
            GrowFromCenter(coke)
        )
        self.wait()
        self.play(FadeOut(img))

        r = 2.9
        h = 10.3
        coke_tex = VGroup(
            MathTex("d", "=", R"5.8\text{ cm}"),
            MathTex("r", "=", Rf"{r}\text{{ cm}}"),
            MathTex("h", "=", Rf"{h}\text{{ cm}}")
        ).shift(RIGHT * 3).scale(1.5)

        d_group = create_labled_brace(coke, "d", DOWN * 2)
        self.play(Write(d_group))
        self.play(Write(coke_tex[0]))

        coke_tex[1].move_to(coke_tex[0]).shift(DOWN * 0.5),
        self.play(coke_tex[0].animate.shift(UP * 0.5))
        self.play(Write(coke_tex[1]))
        self.wait()

        h_group = create_labled_brace(coke, "h", RIGHT * 2)
        self.play(Write(h_group))

        coke_tex[2].move_to(coke_tex[1]).shift(DOWN * 0.5),
        self.play(Group(coke_tex[0], coke_tex[1]).animate.shift(UP * 0.5))
        self.play(Write(coke_tex[2]))
        self.wait()

        info_tex = VGroup(
            coke_tex[1],
            coke_tex[2]
        )

        self.play(
            FadeOut(VGroup(coke, d_group, h_group, coke_tex[0])),
            info_tex.animate.scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + LEFT), 
        )
        self.wait(2)

        formulas = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2")
        ).shift(UP).arrange(DOWN * 1.5).scale(1.5)

        self.play(Write(formulas))
        self.wait()

        self.play(Circumscribe(formulas[0]))
        self.wait(3)
        self.play(Circumscribe(formulas[1]))
        self.wait(3)

        self.play(
            formulas.animate.scale(0.5).arrange(DOWN, aligned_edge=LEFT).next_to(info_tex, DOWN).to_edge(LEFT)
        )
        self.wait()

        surface_tex = VGroup(
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2"),
            MathTex("=", R"2\pi", Rf"\left({r}\right)", Rf"\left({h}\right)", "+", R"2\pi", Rf"\left({r}\right)^2"),
            MathTex("=", R"77.56\pi", R"\text{ cm}^2")
        ).arrange(DOWN).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        surface_tex[1].align_to(surface_tex[0][1], LEFT)
        surface_tex[2].align_to(surface_tex[0][1], LEFT)

        self.play(Write(surface_tex[0]))
        self.wait()

        self.play(Write(surface_tex[1]))
        self.wait()

        self.play(Write(surface_tex[2]))
        self.wait(3)

        # Recurring constant
        const = "38.78"
        h_tex = VGroup(
            MathTex(R"77.56\pi", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2"),
            MathTex(Rf"{const}\pi", "=", "r", "h", "+", "r^2"),
            MathTex(Rf"\frac{{{const}-r^2}}{{r}}", "=", "h")
        ).arrange(DOWN).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        h_tex[0].move_to(surface_tex[0]).align_to(surface_tex[0], RIGHT)

        self.play(
            ReplacementTransform(surface_tex[0][1:].copy(), h_tex[0][1:], run_time=0.1),
            ReplacementTransform(surface_tex[2][1].copy(), h_tex[0][0]),
            FadeOut(surface_tex))
        self.wait()

        self.play(Write(h_tex[1:]))
        self.wait()

        temp_tex = MathTex("h", "=", Rf"\frac{{{const}-r^2}}{{r}}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(TransformMatchingTex(h_tex[2], temp_tex))
        h_tex[2] = temp_tex

        v_tex = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("V", "=", R"\pi", "r^2", R"\left(", Rf"\frac{{{const}-r^2}}{{r}}", R"\right)"),
            MathTex("=", Rf"\pi{const}r", "-", R"\pi{r^3}")
        ).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        v_tex[1].align_to(v_tex[0], LEFT).shift(DOWN * 0.1)
        v_tex[2].next_to(v_tex[1], DOWN).align_to(v_tex[1][1], LEFT)

        self.play(
            FadeOut(h_tex[:2]),
        )
        self.play(Write(v_tex[0]))
        self.wait()

        self.play(
            TransformMatchingShapes(v_tex[0], v_tex[1][:4]),
            ReplacementTransform(h_tex[2][2].copy(), v_tex[1][4:])
        )
        self.wait()

        self.play(Write(v_tex[2]))
        self.wait()

        self.play(
            v_tex[2].animate.next_to(v_tex[1][0], RIGHT, buff=0.2).align_to(v_tex[1][0], DOWN),
            FadeOut(v_tex[1][1:]),
        )
        self.wait(3)

        dv_tex = VGroup(
            MathTex(R"\frac{dV}{dr}", "=", R"\frac{d}{dr}", R"\left[", Rf"{const}{{\pi}}r", "-", R"\pi{r^3}", R"\left]"),
            MathTex(R"\frac{dV}{dr}", "=", Rf"{const}\pi", "-", R"3{\pi}r^2"),
            MathTex("0", "=", Rf"{const}\pi", "-", R"3{\pi}r^2"),
            MathTex("r", "=", Rf"\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}", "=", "3.6", R"\text{ cm}"), # Brackets lmao
        ).move_to(v_tex[1]).arrange(DOWN)

        self.play(
            ReplacementTransform(VGroup(v_tex[1][0], v_tex[2][0]), dv_tex[0][:3]),
            FadeIn(dv_tex[0][3], dv_tex[0][7]),
            ReplacementTransform(v_tex[2][1:], dv_tex[0][4:7])
        )
        self.wait()

        self.play(ReplacementTransform(dv_tex[0].copy(), dv_tex[1]))
        self.wait()
        self.play(ReplacementTransform(dv_tex[1].copy(), dv_tex[2]))
        self.wait()
        self.play(ReplacementTransform(dv_tex[2].copy(), dv_tex[3]))
        self.wait(5)

        temp_tex = MathTex("r", "=", Rf"\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}").scale(0.75).next_to(h_tex[2], UP).to_edge(LEFT)
        self.play(
            FadeOut(dv_tex[:3], v_tex[1][0]),
            ReplacementTransform(dv_tex[3][:4], temp_tex),
            FadeOut(dv_tex[3][4:])
        )
        self.wait(5)
        dv_tex[3] = temp_tex

        modify_r_tex = VGroup(
            MathTex("r", "=", R"\sqrt{", f"{const}", R"\over3", "}"),
            MathTex("r^2", "=", R"\sqrt{", f"{const}", R"\over3", "}^2"),
            MathTex("r^2", "=", "{", f"{const}", R"\over", "3", "}"),
            MathTex("3", "r^2", "=", f"{const}")
        )

        solve_h_tex = VGroup(
            MathTex("h", "=", "{", f"{const}", "-r^2" R"\over{r}}"),
            MathTex("h", "=", "{", "3r^2", "-r^2" + R"\over{r}}"),
            MathTex("h", "=", R"\frac{2r^2}{r}"),
            MathTex("h", "=", "2r"),
            MathTex("h", "=", Rf"2\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}", "=", "7.2", R"\text{ cm}")
        )

        self.play(
            TransformMatchingTex(h_tex[2].copy(), solve_h_tex[0].shift(UP)),
            TransformMatchingTex(dv_tex[3].copy(), modify_r_tex[0].next_to(solve_h_tex[0], DOWN, buff=0.5))
        )
        self.wait(7)
        modify_r_tex[1:].next_to(solve_h_tex[0], DOWN, buff=0.5)

        self.play(
            Indicate(modify_r_tex[0][3]),
            Indicate(solve_h_tex[0][3])
        )
        self.wait(5)

        self.play(TransformMatchingTex(modify_r_tex[0], modify_r_tex[1]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[1], modify_r_tex[2]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[2], modify_r_tex[3]))
        self.wait()

        solve_h_tex[1].move_to(solve_h_tex[0])
        self.play(
            ReplacementTransform(modify_r_tex[3][:2].copy(), solve_h_tex[1][3]),
            TransformMatchingShapes(solve_h_tex[0][:2], solve_h_tex[1][:3]),
            TransformMatchingShapes(solve_h_tex[0][4:], solve_h_tex[1][4:]),
            FadeOut(solve_h_tex[0][3], modify_r_tex[3]),
        )
        self.wait()

        solve_h_tex[2:].arrange(DOWN).shift(DOWN * 0.5)
        self.play(
            solve_h_tex[1].animate.next_to(solve_h_tex[2], UP),
            Write(solve_h_tex[2])
        )
        self.wait()
        self.play(Write(solve_h_tex[3]))
        self.wait()
        self.play(Write(solve_h_tex[4]))
        self.wait(4)

        temp_tex = MathTex("h", "=", Rf"2\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(
            FadeOut(solve_h_tex[1:4]),
            FadeOut(h_tex[2]),
            dv_tex[3].animate.next_to(temp_tex, UP).to_edge(LEFT),
            ReplacementTransform(solve_h_tex[4][:4], temp_tex),
            FadeOut(solve_h_tex[4][4:])
        )
        self.wait(3)
        solve_h_tex[4] = temp_tex

        percent_tex = VGroup(
            MathTex(R"{\text{Actual Volume of Cylinder}}", R"\over", R"{\text{Maximum Possible Volume of Cylinder}}"),
            MathTex("{", Rf"\pi\left({r}\right)^2\left({h}\right)", R"\over", 
                    Rf"\pi\left(\sqrt{{\frac{{{const}}}{3}}}\right)^2\left(2\sqrt{{\frac{{{const}}}{3}}}\right)", "}"),
        )

        self.play(Write(percent_tex[0]))
        self.wait(3)
        self.play(FadeTransform(percent_tex[0], percent_tex[1]))
        self.wait()

        temp_tex = MathTex(
            R"{", Rf"\pi\left({r}\right)^2\left({h}\right)", R"\over", 
            Rf"\pi\left(\sqrt{{\frac{{{const}}}{3}}}\right)^2\left(2\sqrt{{\frac{{{const}}}{3}}}\right)", "}",
            R"=93.19\%"
        )
        self.play(TransformMatchingTex(percent_tex[1], temp_tex))
        self.wait(3)
        percent_tex[1] = temp_tex
        self.play(FadeOut(percent_tex[1], info_tex, formulas, dv_tex[3], solve_h_tex[4]))
        self.wait()

class Salt(ThreeDScene):
    def construct(self):
        img = ImageMobject("imgs\salt.jpg")
        img.height = 5
        img.to_edge(RIGHT, buff=2.5)

        salt = Cylinder(resolution=32, fill_color=RED, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        salt.rotate(PI/2, [1, 0, 0]).scale([8.5 / 6, 13.5 / 6, 1]).to_edge(LEFT, buff=2.5)

        self.play(FadeIn(img))
        self.wait()
        self.play(GrowFromCenter(salt))
        self.wait()
        self.play(FadeOut(img))

        r = 4.25
        h = 13.5
        salt_tex = VGroup(
            MathTex("d", "=", R"8.5\text{ cm}"),
            MathTex("r", "=", Rf"{r}\text{{ cm}}"),
            MathTex("h", "=", Rf"{h}\text{{ cm}}")
        ).shift(RIGHT * 3).scale(1.5)

        d_group = create_labled_brace(salt, "d", DOWN * 2)
        self.play(Write(d_group))
        self.wait()
        
        self.play(Write(salt_tex[0]))

        self.wait()

        salt_tex[1].move_to(salt_tex[0]).shift(DOWN * 0.5),
        self.play(salt_tex[0].animate.shift(UP * 0.5))
        self.play(Write(salt_tex[1]))
        self.wait()

        h_group = create_labled_brace(salt, "h", RIGHT * 2)
        self.play(Write(h_group))
        self.wait()

        salt_tex[2].move_to(salt_tex[1]).shift(DOWN * 0.5),
        self.play(Group(salt_tex[0], salt_tex[1]).animate.shift(UP * 0.5))
        self.play(Write(salt_tex[2]))
        self.wait()

        info_tex = VGroup(
            salt_tex[1],
            salt_tex[2]
        )

        self.play(
            FadeOut(VGroup(salt, d_group, h_group, salt_tex[0])),
            info_tex.animate.scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + LEFT), 
        )
        self.wait()

        formulas = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2")
        ).shift(UP).arrange(DOWN * 1.5).scale(1.5)

        self.play(Write(formulas))
        self.wait()

        self.play(
            formulas.animate.scale(0.5).arrange(DOWN, aligned_edge=LEFT).next_to(info_tex, DOWN).to_edge(LEFT)
        )
        self.wait()

        surface_tex = VGroup(
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2"),
            MathTex("=", R"2\pi", Rf"\left({r}\right)", Rf"\left({h}\right)", "+", R"2\pi", Rf"\left({r}\right)^2"),
            MathTex("=", R"150.875\pi", R"\text{ cm}^2")
        ).arrange(DOWN).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        surface_tex[1].align_to(surface_tex[0][1], LEFT)
        surface_tex[2].align_to(surface_tex[0][1], LEFT)

        self.play(Write(surface_tex[0]))
        self.wait()

        self.play(Write(surface_tex[1]))
        self.wait()

        self.play(Write(surface_tex[2]))
        self.wait()

        # Recurring constant
        const = "75.4375"
        h_tex = VGroup(
            MathTex(R"150.875\pi", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2"),
            MathTex(Rf"{const}\pi", "=", "r", "h", "+", "r^2"),
            MathTex(Rf"\frac{{{const}-r^2}}{{r}}", "=", "h")
        ).arrange(DOWN).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        h_tex[0].move_to(surface_tex[0]).align_to(surface_tex[0], RIGHT)

        self.play(
            ReplacementTransform(surface_tex[0][1:].copy(), h_tex[0][1:], run_time=0.1),
            ReplacementTransform(surface_tex[2][1].copy(), h_tex[0][0]),
            FadeOut(surface_tex))
        self.wait()

        self.play(Write(h_tex[1:]))
        self.wait()

        temp_tex = MathTex("h", "=", Rf"\frac{{{const}-r^2}}{{r}}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(TransformMatchingTex(h_tex[2], temp_tex))
        h_tex[2] = temp_tex

        v_tex = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("V", "=", R"\pi", "r^2", R"\left(", Rf"\frac{{{const}-r^2}}{{r}}", R"\right)"),
            MathTex("=", Rf"\pi{const}r", "-", R"\pi{r^3}")
        ).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        v_tex[1].align_to(v_tex[0], LEFT).shift(DOWN * 0.1)
        v_tex[2].next_to(v_tex[1], DOWN).align_to(v_tex[1][1], LEFT)

        self.play(
            FadeOut(h_tex[:2]),
        )
        self.play(Write(v_tex[0]))
        self.wait()

        self.play(
            TransformMatchingShapes(v_tex[0], v_tex[1][:4]),
            ReplacementTransform(h_tex[2][2].copy(), v_tex[1][4:])
        )
        self.wait()

        self.play(Write(v_tex[2]))
        self.wait()

        self.play(
            v_tex[2].animate.next_to(v_tex[1][0], RIGHT, buff=0.2).align_to(v_tex[1][0], DOWN),
            FadeOut(v_tex[1][1:]),
        )
        self.wait()

        dv_tex = VGroup(
            MathTex(R"\frac{dV}{dr}", "=", R"\frac{d}{dr}", R"\left[", Rf"{const}{{\pi}}r", "-", R"\pi{r^3}", R"\left]"),
            MathTex(R"\frac{dV}{dr}", "=", Rf"{const}\pi", "-", R"3{\pi}r^2"),
            MathTex("0", "=", Rf"{const}\pi", "-", R"3{\pi}r^2"),
            MathTex("r", "=", Rf"\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}", "=", "5.0", R"\text{ cm}"), # Brackets lmao
        ).move_to(v_tex[1]).arrange(DOWN)

        self.play(
            ReplacementTransform(VGroup(v_tex[1][0], v_tex[2][0]), dv_tex[0][:3]),
            FadeIn(dv_tex[0][3], dv_tex[0][7]),
            ReplacementTransform(v_tex[2][1:], dv_tex[0][4:7])
        )
        self.wait()

        self.play(ReplacementTransform(dv_tex[0].copy(), dv_tex[1]))
        self.wait()
        self.play(ReplacementTransform(dv_tex[1].copy(), dv_tex[2]))
        self.wait()
        self.play(ReplacementTransform(dv_tex[2].copy(), dv_tex[3]))
        self.wait()

        temp_tex = MathTex("r", "=", Rf"\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}").scale(0.75).next_to(h_tex[2], UP).to_edge(LEFT)
        self.play(
            FadeOut(dv_tex[:3], v_tex[1][0]),
            ReplacementTransform(dv_tex[3][:4], temp_tex),
            FadeOut(dv_tex[3][4:])
        )
        self.wait()
        dv_tex[3] = temp_tex

        modify_r_tex = VGroup(
            MathTex("r", "=", R"\sqrt{", f"{const}", R"\over3", "}"),
            MathTex("r^2", "=", R"\sqrt{", f"{const}", R"\over3", "}^2"),
            MathTex("r^2", "=", "{", f"{const}", R"\over", "3", "}"),
            MathTex("3", "r^2", "=", f"{const}")
        )

        solve_h_tex = VGroup(
            MathTex("h", "=", "{", f"{const}", "-r^2" R"\over{r}}"),
            MathTex("h", "=", "{", "3r^2", "-r^2" + R"\over{r}}"),
            MathTex("h", "=", R"\frac{2r^2}{r}"),
            MathTex("h", "=", "2r"),
            MathTex("h", "=", Rf"2\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}", "=", "10.0", R"\text{ cm}")
        )

        self.play(
            TransformMatchingTex(h_tex[2].copy(), solve_h_tex[0].shift(UP)),
            TransformMatchingTex(dv_tex[3].copy(), modify_r_tex[0].next_to(solve_h_tex[0], DOWN, buff=0.5))
        )
        self.wait()
        modify_r_tex[1:].next_to(solve_h_tex[0], DOWN, buff=0.5)

        self.play(
            Indicate(modify_r_tex[0][3]),
            Indicate(solve_h_tex[0][3])
        )
        self.wait()

        self.play(TransformMatchingTex(modify_r_tex[0], modify_r_tex[1]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[1], modify_r_tex[2]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[2], modify_r_tex[3]))
        self.wait()

        solve_h_tex[1].move_to(solve_h_tex[0])
        self.play(
            ReplacementTransform(modify_r_tex[3][:2].copy(), solve_h_tex[1][3]),
            TransformMatchingShapes(solve_h_tex[0][:2], solve_h_tex[1][:3]),
            TransformMatchingShapes(solve_h_tex[0][4:], solve_h_tex[1][4:]),
            FadeOut(solve_h_tex[0][3], modify_r_tex[3]),
        )
        self.wait()

        solve_h_tex[2:].arrange(DOWN).shift(DOWN * 0.5)
        self.play(
            solve_h_tex[1].animate.next_to(solve_h_tex[2], UP),
            Write(solve_h_tex[2])
        )
        self.wait()
        self.play(Write(solve_h_tex[3]))
        self.wait()
        self.play(Write(solve_h_tex[4]))
        self.wait()

        temp_tex = MathTex("h", "=", Rf"2\sqrt{{\frac{{{const}}}{3}}}", R"\text{ cm}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(
            FadeOut(solve_h_tex[1:4]),
            FadeOut(h_tex[2]),
            dv_tex[3].animate.next_to(temp_tex, UP).to_edge(LEFT),
            ReplacementTransform(solve_h_tex[4][:4], temp_tex),
            FadeOut(solve_h_tex[4][4:])
        )
        self.wait()
        solve_h_tex[4] = temp_tex

        percent_tex = VGroup(
            MathTex(R"{\text{Actual Volume of Cylinder}}", R"\over", R"{\text{Maximum Possible Volume of Cylinder}}"),
            MathTex("{", Rf"\pi\left({r}\right)^2\left({h}\right)", R"\over", 
                    Rf"\pi\left(\sqrt{{\frac{{{const}}}{3}}}\right)^2\left(2\sqrt{{\frac{{{const}}}{3}}}\right)", "}"),
        )

        self.play(Write(percent_tex[0]))
        self.wait()
        self.play(FadeTransform(percent_tex[0], percent_tex[1]))
        self.wait()

        temp_tex = MathTex(
            R"{", Rf"\pi\left({r}\right)^2\left({h}\right)", R"\over", 
            Rf"\pi\left(\sqrt{{\frac{{{const}}}{3}}}\right)^2\left(2\sqrt{{\frac{{{const}}}{3}}}\right)", "}",
            R"=96.7\%"
        )
        self.play(TransformMatchingTex(percent_tex[1], temp_tex))
        self.wait(3)
        percent_tex[1] = temp_tex
        self.play(FadeOut(percent_tex[1], info_tex, formulas, dv_tex[3], solve_h_tex[4]))

class Proof(ThreeDScene):
    def construct(self):
        formulas = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2")
        ).shift(UP).arrange(DOWN * 1.5).scale(1.5)

        self.play(Write(formulas))
        self.wait()

        self.play(
            formulas.animate.scale(0.5).arrange(DOWN, aligned_edge=LEFT).to_corner(UP + LEFT)
        )
        self.wait()

        h_tex = VGroup(
            MathTex("S", "=", R"2\pi", "r", "h", "+", R"2\pi", "r^2"),
            MathTex("S", "-" R"2\pi", "r^2", "=", R"2\pi", "r", "h"),
            MathTex("{", "S", "-" R"2\pi", "r^2", R"\over", R"2\pi", "r", "}", "=", "h"),
            MathTex("{", R"\frac{S}{2\pi}", "-" "r^2", R"\over", "r", "}", "=", "h")
        ).arrange(DOWN)

        self.play(Write(h_tex[0]))
        self.wait()
        self.play(TransformMatchingTex(h_tex[0].copy(), h_tex[1]))
        self.wait()
        self.play(TransformMatchingTex(h_tex[1].copy(), h_tex[2]))
        self.wait()
        self.play(TransformMatchingTex(h_tex[2].copy(), h_tex[3]))
        self.wait()

        temp_tex = MathTex("h", "=", "{", R"\frac{S}{2\pi}", "-" "r^2", R"\over", "r", "}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(
            TransformMatchingTex(h_tex[3], temp_tex),
            FadeOut(h_tex[:3])
        )
        h_tex[3] = temp_tex
        self.wait()

        v_tex = VGroup(
            MathTex("V", "=", R"\pi", "r^2", "h"),
            MathTex("V", "=", R"\pi", "r^2", R"\left(", R"\frac{\frac{S}{2\pi}-r^2}{r}", R"\right)"),
            MathTex("=", R"\frac{1}{2}{\pi}Sr", "-", R"\pi{r^3}")
        ).to_corner(UP + LEFT).shift(RIGHT * 4).shift(DOWN * 2)

        v_tex[1].align_to(v_tex[0], LEFT).shift(DOWN * 0.1)
        v_tex[2].next_to(v_tex[1], DOWN).align_to(v_tex[1][1], LEFT)

        self.play(Write(v_tex[0]))
        self.wait()

        self.play(
            TransformMatchingShapes(v_tex[0], v_tex[1][:4]),
            ReplacementTransform(h_tex[3][2:].copy(), v_tex[1][4:])
        )
        self.wait()

        self.play(Write(v_tex[2]))
        self.wait()

        temp_tex = MathTex("V", "=", R"\frac{1}{2}{\pi}Sr", "-", R"\pi{r^3}").move_to(v_tex[1]).shift(UP * 0.05).align_to(v_tex[1][0], LEFT)
        self.play(
            TransformMatchingTex(v_tex[2], temp_tex),
            FadeOut(v_tex[1]),
        )
        v_tex[2] = temp_tex
        self.wait()

        dv_tex = VGroup(
            MathTex(R"\frac{dV}{dr}", "=", R"\frac{d}{dr}", R"\left[", R"\frac{1}{2}{\pi}Sr", "-", R"\pi{r^3}", R"\left]"),
            MathTex(R"\frac{dV}{dr}", "=", R"\frac{1}{2}S", "-", R"3{\pi}r^2"),
            MathTex("0", "=", R"\frac{1}{2}S", "-", R"3{\pi}r^2"),
            MathTex(R"3{\pi}r^2", "=", R"\frac{1}{2}S"),
            MathTex("r", "=", R"\sqrt{\frac{S}{6\pi}}")
        ).move_to(v_tex[1]).arrange(DOWN)

        self.play(
            ReplacementTransform(v_tex[2][0], dv_tex[0][:3]),
            FadeIn(dv_tex[0][3], dv_tex[0][7]),
            ReplacementTransform(v_tex[2][1:], dv_tex[0][4:7])
        )
        self.wait()

        self.play(TransformMatchingTex(dv_tex[0].copy(), dv_tex[1]))
        self.wait()
        self.play(TransformMatchingTex(dv_tex[1].copy(), dv_tex[2]))
        self.wait()
        self.play(TransformMatchingTex(dv_tex[2].copy(), dv_tex[3]))
        self.wait()
        self.play(TransformMatchingTex(dv_tex[3].copy(), dv_tex[4]))
        self.wait()

        temp_tex = MathTex("r", "=", R"\sqrt{\frac{S}{6\pi}}").scale(0.75).next_to(h_tex[3], UP).to_edge(LEFT)
        self.play(
            FadeOut(dv_tex[:4]),
            ReplacementTransform(dv_tex[4], temp_tex),
        )
        self.wait()
        dv_tex[4] = temp_tex

        modify_r_tex = VGroup(
            MathTex("r", "=", R"\sqrt{", "S", R"\over6\pi}", "}"),
            MathTex("r^2", "=", R"\sqrt{", "S", R"\over6\pi}", "}^2"),
            MathTex("r^2", "=", "{", "S", R"\over6\pi}", "}"),
            MathTex("3", "r^2", "=", "{", "S", R"\over2\pi}", "}")
        )

        solve_h_tex = VGroup(
            MathTex("h", "=", "{", "{", "S", R"\over2\pi}", "-r^2" R"\over{r}}"),
            MathTex("h", "=", "{", "3r^2", "-r^2" + R"\over{r}}"),
            MathTex("h", "=", R"\frac{2r^2}{r}"),
            MathTex("h", "=", "2r"),
            MathTex("h", "=", "{", "2", R"\sqrt{", "S", R"\over6\pi}", "}")
        )

        self.play(
            TransformMatchingTex(h_tex[3].copy(), solve_h_tex[0].shift(UP)),
            TransformMatchingTex(dv_tex[4].copy(), modify_r_tex[0].next_to(solve_h_tex[0], DOWN, buff=0.5))
        )
        self.wait()
        modify_r_tex[1:].next_to(solve_h_tex[0], DOWN, buff=0.5)

        self.play(
            Indicate(VGroup(modify_r_tex[0][3:5])),
            Indicate(VGroup(solve_h_tex[0][4:6]))
        )
        self.wait()

        self.play(TransformMatchingTex(modify_r_tex[0], modify_r_tex[1]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[1], modify_r_tex[2]))
        self.wait()
        self.play(TransformMatchingTex(modify_r_tex[2], modify_r_tex[3]))
        self.wait()

        solve_h_tex[1].move_to(solve_h_tex[0])
        self.play(
            ReplacementTransform(modify_r_tex[3][:2].copy(), solve_h_tex[1][3]),
            TransformMatchingShapes(solve_h_tex[0][:2], solve_h_tex[1][:4]),
            TransformMatchingShapes(solve_h_tex[0][6:], solve_h_tex[1][4:]),
            FadeOut(solve_h_tex[0][4:6], modify_r_tex[3]),
        )
        self.wait()

        solve_h_tex[2:].arrange(DOWN).shift(DOWN * 0.5)
        self.play(
            solve_h_tex[1].animate.next_to(solve_h_tex[2], UP),
            Write(solve_h_tex[2])
        )
        self.wait()
        self.play(Write(solve_h_tex[3]))
        self.wait()
        self.play(Write(solve_h_tex[4]))
        self.wait()

        temp_tex = MathTex("h", "=", "2", R"\sqrt{", "S", R"\over6\pi}", "}").scale(0.75).to_corner(DOWN + LEFT)
        self.play(
            FadeOut(solve_h_tex[1:4]),
            dv_tex[4].animate.next_to(temp_tex, UP).to_edge(LEFT),
            ReplacementTransform(VGroup(solve_h_tex[4], h_tex[3]), temp_tex),
        )
        self.wait()
        solve_h_tex[4] = temp_tex

        final_tex = VGroup(
            MathTex("r", "=", R"\sqrt{\frac{S}{6\pi}}"),
            MathTex("h", "=", "2", R"\sqrt{", "S", R"\over6\pi}", "}"),
            MathTex("h", "=", "2r")
        ).arrange(DOWN)

        self.play(Write(final_tex))
        self.wait(6)
        self.play(FadeOut(final_tex, formulas, dv_tex[4], solve_h_tex[4]))
        self.wait(1.5)

        # Prediction again
        cube = Cube(color=BLUE, fill_opacity=0, stroke_width=4)
        self.play(Create(cube))
        self.wait(0.5)

        cylinder = Cylinder(resolution=32, fill_color=RED, checkerboard_colors=False, 
        fill_opacity=0.5, stroke_width=0, show_ends=True)
        cylinder.shift(UP * 7).rotate(PI/2, [1, 0, 0])
        self.play(cylinder.animate.move_to(cube))
        self.wait(2)

        self.play(Group(cylinder, cube).animate.to_edge(LEFT, buff=3).scale(1.5))

        temp_tex = MathTex("s=h=d=2r").scale(1.5).to_edge(RIGHT, buff=2)
        self.play(Write(temp_tex))

        self.wait(2)
        self.play(FadeOut(cube, cylinder, temp_tex))

class ConcludingQuestion(Scene):
    def construct(self):
            self.wait(2)

            question_tex = Paragraph(
            "If you were the manufacturer of \n" 
            "these cans, would you want your \n"
            "cans to be volume-optimized? \n"
            "Why or why not? ",
            font_size=40, alignment='center').to_edge(UP, buff=1.5)

            self.play(Write(question_tex, run_time=5))
            self.wait()

            answer_tex = Paragraph("Probably Not.", font_size=40, alignment='center').next_to(question_tex, DOWN, buff=1.5)
            self.play(Write(answer_tex))
            self.wait(24)

            self.play(FadeOut(question_tex, answer_tex))
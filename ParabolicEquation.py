from manim import *

config.tex_template.add_to_preamble(
    r"\usepackage{helvet}"
    r"\renewcommand{\familydefault}{\sfdefault}"
    r"\usepackage{sansmath}"
    r"\sansmath"
)

class Scene1(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        eq1 = Tex(
            r"$x^2 - 6x - 2y = -10$", 
            substrings_to_isolate=["x", "y"]
        )
        eq2 = Tex(
            r"$x^2 - 6x + 10 = 2y$", 
            substrings_to_isolate=["x", "y"]
        )
        eq3 = Tex(
            r"$y = \LARGE \frac{x^2 - 6x + 10}{2}$", 
            substrings_to_isolate=["x", "y"]
        )
        
        # 3. Apply the colors to both equations using a loop
        for eq in [eq1, eq2, eq3]:
            eq.set_color(BLACK)
            eq.set_color_by_tex("x", GREEN)
            eq.set_color_by_tex("y", RED)
            eq.scale(1.5) # Scale them equally
            
        # 4. Group them and arrange them vertically (eq2 below eq1)
        # 'buff' sets the spacing distance between the two lines
        equations = VGroup(eq1, eq2, eq3).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        
        # 5. Play the animations sequentially
        self.play(Write(eq1))
        self.wait(1)
        
        self.play(Write(eq2))
        self.wait(2)

        self.play(Write(eq3))
        self.wait(3)

        self.play(
            equations.animate.scale(0.6).to_corner(UL, buff=0.8),
            run_time=2
        )
        self.wait(2)


        # ==========================================
        # CREATE AND POSITION THE GRAPH GRID & AXES
        # ==========================================
        number_plane_scaled = NumberPlane(
            x_range=(0, 31, 1),
            y_range=(0, 31, 1),
            x_length=8,
            y_length=8,
            background_line_style={
                "stroke_color": LIGHT_GRAY,
                "stroke_width": 1,
                "stroke_opacity": 1
            },
            axis_config={
                "stroke_color": BLACK,
                "stroke_width": 3,
                "include_tip": True,
                "tip_width": 0.4,
                "tip_length": 0.3,
            },
            x_axis_config={
                "line_to_number_buff": 0.1, # Increases spacing away from axis lines
                "label_direction": DOWN
            },
            y_axis_config={
                "label_direction": LEFT,     # Forces Y labels strictly to the left of the axis
            }
        )#move_to(RIGHT*3)

        # Scale down slightly if needed and align to right screen edge
        number_plane_scaled.scale(0.9)
        number_plane_scaled.to_edge(RIGHT, buff=0.6)

        number_plane_scaled.add_coordinates(
            font_size = 14,     
            color = BLACK      
        )

        # self.add(number_plane_scaled)

        self.play(
            Write(number_plane_scaled),
            run_time=4
        )
        self.wait(5)

        # ==========================================
        # CREATE AND POSITION THE PLUS SYMBOL / TABLE
        # ==========================================
        line_length = 4.0
        half_length = line_length / 2.0
        
        # Left-to-right horizontal line
        horiz_line = Line(
            start=[-half_length, line_length - 1, 0], 
            end=[half_length, line_length - 1, 0], 
            stroke_width=3, 
            color=BLACK
        )
        
        # Top-to-bottom vertical line
        vert_line = Line(
            start=[0, line_length, 0], 
            end=[0, -line_length, 0], 
            stroke_width=3, 
            color=BLACK
        )
        
        crosshair = VGroup(horiz_line, vert_line)
        
        # Position the entire crosshair structure BELOW the equations, aligned to their left edge
        crosshair.next_to(equations, DOWN, aligned_edge=LEFT)

        # ==========================================
        # ANIMATE DRAWING THE T SHAPE
        # ==========================================
        # Draw the horizontal line first
        self.play(Create(horiz_line), run_time=1.2)
        self.wait(0.2)
        
        # Draw the vertical line cutting directly through its midpoint
        self.play(Create(vert_line), run_time=1.2)
        self.wait(2)

        # ==========================================
        # ADD HEADERS IN TOP SECTIONS
        # ==========================================
        # Create text matching your font and colors
        label_x = Tex(r"$x$", color=GREEN).scale(0.8)
        label_y = Tex(r"$y$", color=RED).scale(0.8)
        
        # Position 'x' above the horizontal line, shifted into the top-left area
        label_x.next_to(horiz_line, UP, buff=0.2)
        label_x.shift(LEFT * 1.0)
        
        # Position 'y' above the horizontal line, shifted into the top-right area
        label_y.next_to(horiz_line, UP, buff=0.2)
        label_y.shift(RIGHT * 1.0)

        # 2. NumberPlane Axis Labels
        # Uses plane_coordinate_to_point or get_axis_labels for precise alignment
        plane_label_x = Tex(r"$x$", color=GREEN).scale(0.8)
        plane_label_y = Tex(r"$y$", color=RED).scale(0.8)

        # Position 'x' label at the end of the X axis tip
        plane_label_x.next_to(
            number_plane_scaled.get_x_axis().get_end(), RIGHT
        )
        # Position 'y' label above the Y axis tip
        plane_label_y.next_to(
            number_plane_scaled.get_y_axis().get_end(), UP
        )

        # 3. Write all headers simultaneously across both table and grid
        self.play(
            Write(label_x), 
            Write(label_y),
            Write(plane_label_x),
            Write(plane_label_y),
            run_time=1.0
        )
        self.wait(2)

        # ==========================================
        # ADD MULTIPLE ROWS OF (X, Y) VALUES
        # ==========================================
        # List of (x, y) pairs to display sequentially
        data_points = [
            (0, 5),
            (1, 2.5),
            (2, 1),
            (3, 0.5),
            (4, 1),
            (5, 2.5),
            (6, 5)
        ]

        # Lists to keep track of created text objects for positioning the next row
        x_val_mobjects = []
        y_val_mobjects = []
        # Store dots if you want to draw a curve through them later
        plotted_dots = []

        for i, (x_val, y_val) in enumerate(data_points):
            # Create LaTeX text for x and y
            val_x = Tex(rf"${x_val}$", color=GREEN).scale(0.8)
            val_y = Tex(rf"${y_val}$", color=RED).scale(0.8)

            if i == 0:
                # First row positions directly below the horizontal line
                val_x.next_to(horiz_line, DOWN, buff=0.2).match_x(label_x)
                val_y.next_to(horiz_line, DOWN, buff=0.2).match_x(label_y)
            else:
                # Subsequent rows position below the previous row's numbers
                val_x.next_to(x_val_mobjects[-1], DOWN, buff=0.2)
                val_y.next_to(y_val_mobjects[-1], DOWN, buff=0.2)

            # Keep track of created objects
            x_val_mobjects.append(val_x)
            y_val_mobjects.append(val_y)

            # Create corresponding point on the NumberPlane
            point_location = number_plane_scaled.c2p(x_val, y_val)
            dot = Dot(point=point_location, color=BLUE, radius=0.08)
            plotted_dots.append(dot)

            # Animate x value
            self.play(Write(val_x), run_time=0.6)
            
            # Wait 1 second before revealing the corresponding y value
            self.wait(1)
            
            # Animate y value
            self.play(Write(val_y), Create(dot), run_time=0.6)
            
            # Brief pause before moving to the next row
            self.wait(0.5)

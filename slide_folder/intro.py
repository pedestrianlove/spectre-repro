from manim import *

def intro(self):
    # ========== Animated Attack Visualization ==========
    section_title = Text("Spectre v1 Attack", font_size=36, color=YELLOW).to_edge(UP)
    self.play(Write(section_title))
    self.next_slide()
    
    # Memory layout as background
    array1_box = Rectangle(width=2, height=1.2, color=GREEN, fill_opacity=0.2).shift(LEFT * 4.5 + UP * 1.5)
    array1_label = Text("array1[16]", font_size=16, color=GREEN).next_to(array1_box, UP, buff=0.1)
    
    padding = Rectangle(width=2, height=0.3, color=PURPLE, fill_opacity=0.1).shift(LEFT * 4.5 + UP * 0.1)
    
    secret_box = Rectangle(width=2, height=0.5, color=GOLD, fill_opacity=0.3).shift(LEFT * 4.5 + DOWN * 0.6)
    secret_label = Text("secret", font_size=14, color=GOLD).next_to(secret_box, LEFT, buff=0.2)
    
    array2_box = Rectangle(width=2, height=2.5, color=RED, fill_opacity=0.15).shift(RIGHT * 4.5 + DOWN * 0.2)
    array2_label = Text("array2[256*512]", font_size=16, color=RED).next_to(array2_box, UP, buff=0.1)
    array2_note = Text("(probe array)", font_size=12, color=GRAY).next_to(array2_label, DOWN, buff=0.05)
    
    memory_layout = VGroup(array1_box, array1_label, padding, secret_box, secret_label, 
                           array2_box, array2_label, array2_note)
    self.play(Create(memory_layout))
    self.next_slide()
    
    # Victim function code
    victim_code = Code(
        code_string="""if (x < array1_size)
  temp &= array2[array1[x] * 512];""",
        language="c",
        background="window",
        add_line_numbers=False
    ).scale(0.6).shift(UP * 2.2 + LEFT * 0.5)
    self.play(Create(victim_code))
    self.next_slide()
    
    # Flush operation animation
    flush_text = Text("Flush array2 & array1_size", font_size=16, color=BLUE).shift(DOWN * 2.8)
    self.play(Write(flush_text))
    self.play(array2_box.animate.set_fill(opacity=0.05), run_time=0.5)
    self.next_slide()
    
    # Training iterations
    iteration_label = Text("Training (5 valid : 1 malicious)", font_size=18, color=ORANGE).shift(UP * 0.5)
    self.play(Write(iteration_label))
    
    # Animate training sequence
    for round in range(2):
        for i in range(6):
            if i < 5:
                # Valid access - read from array1
                index = i
                color = GREEN
                label_text = f"Valid: x={index}"
            else:
                # Malicious access - read secret
                color = RED
                label_text = "Malicious: x → secret"
            
            access_label = Text(label_text, font_size=14, color=color).shift(DOWN * 0.5)
            self.play(Write(access_label), run_time=0.3)
            
            # Show data flow
            if i < 5:
                # Normal path: array1 → array2
                dot1 = Dot(array1_box.get_right(), color=color)
                self.play(Create(dot1), run_time=0.2)
                self.play(dot1.animate.move_to(array2_box.get_left()), run_time=0.4)
                self.play(FadeOut(dot1), array2_box.animate.set_fill(opacity=0.15), run_time=0.2)
            else:
                # Malicious path: secret → array2 (speculative)
                dot1 = Dot(secret_box.get_right(), color=color)
                self.play(Create(dot1), run_time=0.2)
                self.play(dot1.animate.move_to(array2_box.get_left()), run_time=0.4)
                # Highlight cached location
                cache_highlight = Rectangle(width=0.3, height=0.3, color=YELLOW, 
                                           fill_opacity=0.5).move_to(array2_box.get_top() + DOWN * 0.5)
                self.play(Create(cache_highlight), FadeOut(dot1), run_time=0.2)
                self.play(FadeOut(cache_highlight), run_time=0.3)
            
            self.play(FadeOut(access_label), run_time=0.2)
    
    self.play(FadeOut(iteration_label))
    
    # Show result
    result_text = Text("Secret byte cached in array2!", font_size=18, color=YELLOW).shift(DOWN * 0.5)
    self.play(Write(result_text))
    self.play(array2_box.animate.set_fill(color=YELLOW, opacity=0.3), run_time=0.5)
    self.next_slide()
    
    self.play(FadeOut(flush_text), FadeOut(result_text))
    self.next_slide()
    
    # Clear for next section
    self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ========== Timing Analysis & Statistical Scoring ==========
    section_title2 = Text("Timing Analysis & Statistical Scoring", font_size=36, color=YELLOW).to_edge(UP)
    self.play(Write(section_title2))
    self.next_slide()
    
    timing_title = Text("How to extract the secret byte:", font_size=24).shift(UP * 2.5)
    self.play(Write(timing_title))
    
    # Show the timing loop
    timing_text = Text("For each possible byte value (0-255):", font_size=22, color=BLUE).shift(UP * 1.8)
    self.play(Write(timing_text))
    self.next_slide()
    
    timing_step1 = Text("1. Read array2[i * 512] and measure time", font_size=20).shift(UP * 1.1)
    timing_code = Code(
        code_string="""time1 = __rdtscp(&junk);
junk = *addr;  // Read memory
time2 = __rdtscp(&junk) - time1;""",
        language="c",
        background="window",
        add_line_numbers=False
    ).scale(0.65).next_to(timing_step1, DOWN, buff=0.2)
    self.play(Write(timing_step1), Create(timing_code))
    self.next_slide()
    
    timing_step2 = Text("2. If time ≤ 80 cycles → Cache hit!", font_size=20, color=GREEN).shift(DOWN * 0.3)
    timing_step3 = Text("3. Increment score for that byte value", font_size=20, color=ORANGE).shift(DOWN * 0.9)
    self.play(Write(timing_step2), Write(timing_step3))
    self.next_slide()
    
    # Visualization of timing differences
    graph_label = Text("Timing Comparison:", font_size=20).shift(DOWN * 1.6)
    self.play(Write(graph_label))
    
    # Create bars showing cache hit vs miss
    cache_hit_label = Text("Cache Hit", font_size=16, color=GREEN).shift(DOWN * 2.2 + LEFT * 2.5)
    cache_hit_bar = Rectangle(width=0.6, height=0.8, color=GREEN, fill_opacity=0.7).next_to(cache_hit_label, DOWN, buff=0.1)
    cache_hit_time = Text("~40 cycles", font_size=14).next_to(cache_hit_bar, DOWN, buff=0.05)
    
    cache_miss_label = Text("Cache Miss", font_size=16, color=RED).shift(DOWN * 2.2 + RIGHT * 2.5)
    cache_miss_bar = Rectangle(width=0.6, height=2.5, color=RED, fill_opacity=0.7).next_to(cache_miss_label, DOWN, buff=0.1)
    cache_miss_time = Text("~200+ cycles", font_size=14).next_to(cache_miss_bar, DOWN, buff=0.05)
    
    self.play(
        Write(cache_hit_label), Create(cache_hit_bar), Write(cache_hit_time),
        Write(cache_miss_label), Create(cache_miss_bar), Write(cache_miss_time)
    )
    self.next_slide()
    
    self.play(*[FadeOut(mob) for mob in self.mobjects])
    
    # Continue with statistical scoring in same section
    stat_title = Text("Timing Analysis & Statistical Scoring", font_size=36, color=YELLOW).to_edge(UP)
    self.play(Write(stat_title))
    
    repeat_text = Text("Repeat 999 times for statistical confidence", font_size=22, color=BLUE).shift(UP * 2.2)
    self.play(Write(repeat_text))
    self.next_slide()
    
    score_text = Text("Scoring System:", font_size=24).shift(UP * 1.4)
    self.play(Write(score_text))
    
    score_detail = Text("results[byte_value]++ for each cache hit", font_size=20, color=GREEN).shift(UP * 0.8)
    self.play(Write(score_detail))
    self.next_slide()
    
    # Show example scores
    example_title = Text("Example Result:", font_size=22).shift(UP * 0.2)
    self.play(Write(example_title))
    
    # Create a simple bar chart
    bars_group = VGroup()
    for i in range(10):
        height = 0.2 if i not in [4] else 1.8  # byte 'T' (0x54) is the secret
        bar = Rectangle(width=0.4, height=height, 
                       color=RED if i == 4 else BLUE,
                       fill_opacity=0.6).shift(LEFT * 2.5 + RIGHT * i * 0.5 + DOWN * 1.3)
        bars_group.add(bar)
    
    self.play(Create(bars_group))
    
    winner_arrow = Arrow(bars_group[4].get_top(), bars_group[4].get_top() + UP * 0.5, color=GOLD)
    winner_text = Text("'T' (0x54)", font_size=20, color=GOLD).next_to(winner_arrow, UP)
    winner_score = Text("Score: 847", font_size=16, color=GREEN).next_to(winner_text, DOWN, buff=0.05)
    self.play(Create(winner_arrow), Write(winner_text), Write(winner_score))
    self.next_slide()
    
    success_text = Text("Success criterion: best ≥ 2 × runner-up + 5", 
                       font_size=18, color=ORANGE).shift(DOWN * 2.5)
    self.play(Write(success_text))
    self.next_slide()
    
    self.play(*[FadeOut(mob) for mob in self.mobjects])


from manim import *

def intro(self):
    # # ========== Attack Setup Workflow ==========
    # section_title = Text("Spectre v1 Attack Setup", font_size=36, color=YELLOW).to_edge(UP)
    # self.play(Write(section_title))
    # self.next_slide()
    
    # LEFT SIDE - Text content
    left_content = VGroup()
    
    # 1. Memory Layout
    step1_title = Text("1. Memory Layout", font_size=22, color=GREEN)
    arrays = VGroup(
        Text("array1[160] (16 valid)", font_size=16),
        Text("array2[256*512] (probe)", font_size=16),
        Text("unused1/2[64] (padding)", font_size=16),
        Text("secret (out-of-bounds)", font_size=16)
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    
    step1_group = VGroup(step1_title, arrays).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    left_content.add(step1_group)
    
    # 2. Cache Preparation
    step2_title = Text("2. Cache Preparation", font_size=22, color=BLUE)
    cache_steps = VGroup(
        Text("Flush array2[i*512]", font_size=16),
        Text("  for i in 0..255", font_size=16),
        Text("Flush array1_size", font_size=16),
        Text("→ Force speculation", font_size=16)
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
    
    step2_group = VGroup(step2_title, cache_steps).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
    left_content.add(step2_group)
    
    # 3. Victim Function & Training
    step3_title = Text("3. Victim Function & Training", font_size=22, color=ORANGE)
    victim_code = Code(
        code_string="""if (x < array1_size)
  temp &= array2[array1[x] * 512];""",
        language="c",
        background="window",
        add_line_numbers=False
    ).scale(0.55)
    training = Text("Train 5:1 (valid:malicious)", font_size=15, color=GRAY)
    
    step3_group = VGroup(step3_title, victim_code, training).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    left_content.add(step3_group)
    
    # Arrange all left content vertically
    left_content.arrange(DOWN, aligned_edge=LEFT, buff=0.5).to_edge(LEFT, buff=0.8).shift(UP * 0.3)
    
    self.play(Write(left_content))
    self.next_slide()
    
    # RIGHT SIDE - Visual diagram
    # Memory layout diagram
    mem_diagram = VGroup(
        Rectangle(width=2.5, height=0.6, color=GREEN, fill_opacity=0.3),
        Text("array1", font_size=14).shift(UP * 1.5),
        Rectangle(width=2.5, height=0.6, color=RED, fill_opacity=0.3).shift(DOWN * 0.7),
        Text("array2", font_size=14).shift(DOWN * 0.7),
        Rectangle(width=2.5, height=0.4, color=PURPLE, fill_opacity=0.2).shift(DOWN * 1.6),
        Text("padding", font_size=12).shift(DOWN * 1.6),
        Rectangle(width=2.5, height=0.5, color=GOLD, fill_opacity=0.3).shift(DOWN * 2.4),
        Text("secret", font_size=14).shift(DOWN * 2.4)
    ).shift(UP * 1.5)
    
    # Training pattern
    pattern_title = Text("Training Pattern:", font_size=16).shift(DOWN * 0.2)
    boxes = VGroup()
    for i in range(12):
        color = GREEN if i % 6 != 5 else RED
        box = Rectangle(width=0.35, height=0.35, color=color, fill_opacity=0.6).shift(
            LEFT * 0.9 + RIGHT * (i % 6) * 0.4 + DOWN * 1.0 + DOWN * (i // 6) * 0.4
        )
        boxes.add(box)
    
    legend = VGroup(
        Text("■ Valid", font_size=12, color=GREEN),
        Text("■ Malicious", font_size=12, color=RED)
    ).arrange(RIGHT, buff=0.3).shift(DOWN * 2.2)
    
    right_content = VGroup(mem_diagram, pattern_title, boxes, legend).to_edge(RIGHT, buff=0.8)
    
    self.play(Create(right_content))
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


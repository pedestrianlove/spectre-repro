from manim import *

def intro(self):
    # Setup LaTeX preambles.
    definition_template = TexTemplate()
    definition_template.add_to_preamble(r"\usepackage{amsthm}")
    definition_template.add_to_preamble(r"\newtheorem*{definition}{Definition}")
    definition_template.add_to_preamble(r"\newtheorem*{theorem}{Theorem}")

    # Contraction definition
    contraction_def = Tex(r"""
        Let $X$ be a metric space, with metric $d$. If $\phi$ maps $X$ into $X$ and if there is a number $c<1$ such that
        \begin{equation*}
            d(\phi(x), \phi(y)) \leq c \cdot d(x, y)
        \end{equation*}
        for all $x,y\in X$, then $\phi$ is said to be a contraction of $X$ into $X$.
    """, tex_template=definition_template,tex_environment="definition").scale(0.75)
    self.play(Write(contraction_def))
    self.next_slide()
    self.play(FadeOut(contraction_def))

    # Contraction theorem
    contraction_theorem = Tex(r"""
        If $X$ is a complete metric space, and if $\phi$ is a contraction of $X$ into X, then there exists one and only one $x\in X$ such that $\phi (x) = x$.
    """, tex_template=definition_template, tex_environment="theorem").scale(0.75)
    self.play(Write(contraction_theorem))
    self.next_slide()
    self.play(FadeOut(contraction_theorem))

    # Proof Intro
    title = Text("Actually, the mechanism is pretty simple.")
    self.play(FadeIn(title))
    self.next_slide()
    self.play(FadeOut(title))


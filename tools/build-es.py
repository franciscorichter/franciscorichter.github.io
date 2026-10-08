#!/usr/bin/env python3
"""Build es/index.html, the Spanish page, from index.html.

index.html is the only source. This script applies the translation table below to it,
points its relative links one level up (es/ is a subfolder), and marks ES as the current
language. Every English phrase in the table must occur in index.html: when one does not,
the script stops and names it, because the English text changed and the Spanish has to be
updated with it. Run it after every edit to index.html:

    python3 tools/build-es.py

Paper titles, authors, journals, course and book titles stay in their original language.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "index.html"
OUT = ROOT / "es" / "index.html"

T = [
    # head
    ('<html lang="en">', '<html lang="es">'),
    ('content="Francisco Richter Mendoza works on statistical inference for systems we only see in part: species diversification from trees of living species, causal regularization, and applications in astronomy, ecology, public health and education. Università della Svizzera italiana, Lugano."',
     'content="Francisco Richter Mendoza trabaja en inferencia estadística para sistemas que solo vemos en parte: la diversificación de especies a partir de árboles de especies vivas, la regularización causal y aplicaciones en astronomía, ecología, salud pública y educación. Università della Svizzera italiana, Lugano."'),
    # language switch
    ('<p class="langs" aria-label="Language"><a href="./" lang="en" hreflang="en" aria-current="true">EN</a><a href="es/" lang="es" hreflang="es">ES</a></p>',
     '<p class="langs" aria-label="Idioma"><a href="../" lang="en" hreflang="en">EN</a><a href="./" lang="es" hreflang="es" aria-current="true">ES</a></p>'),
    # tree figure
    ('<title id="tree-title">A simulated birth-death tree: lineages that survive to the present, and faded lineages that went extinct</title>',
     '<title id="tree-title">Un árbol de nacimiento y muerte simulado: los linajes que sobreviven hasta el presente y, más tenues, los que se extinguieron</title>'),
    ('aria-label="Adjust the simulation"', 'aria-label="Ajustar la simulación"'),
    ('aria-label="What the tree shows"', 'aria-label="Qué muestra el árbol"'),
    ('>Everything that lived</button>', '>Todo lo que vivió</button>'),
    ('>What survives</button>', '>Lo que sobrevive</button>'),
    ('>What is sampled</button>', '>Lo que se muestrea</button>'),
    ('>Speciation λ</label>', '>Especiación λ</label>'),
    ('>Extinction μ</label>', '>Extinción μ</label>'),
    ('>Diversity dependence β<sub>N</sub></label>', '>Dependencia de la diversidad β<sub>N</sub></label>'),
    ('>Crown age</label>', '>Edad de la corona</label>'),
    ('>Sampling ρ</label>', '>Muestreo ρ</label>'),
    ('>New tree</button>', '>Nuevo árbol</button>'),
    ('>Open the full simulator</a>', '>Abrir el simulador completo</a>'),
    # intro
    ('<p class="lede">Scientific collaborator and lecturer at the Faculty of Informatics, <a href="https://www.usi.ch/en">Università della Svizzera italiana</a>, Lugano.</p>',
     '<p class="lede">Colaborador científico y profesor en la Facultad de Informática de la <a href="https://www.usi.ch/it">Università della Svizzera italiana</a>, Lugano.</p>'),
    ('<p>PhD, University of Groningen (2021), with Ernst Wit and Rampal Etienne. Mathematical engineer, Universidad Técnica Federico Santa María, Valparaíso. Earlier work at ESO and in industry.</p>',
     '<p>Doctor por la Universidad de Groningen (2021), con Ernst Wit y Rampal Etienne. Ingeniero civil matemático, Universidad Técnica Federico Santa María, Valparaíso. Antes trabajé en ESO y en la industria.</p>'),
    ('aria-label="Sections"', 'aria-label="Secciones"'),
    ('<a href="#research">Research</a>', '<a href="#research">Investigación</a>'),
    ('<a href="#teaching">Teaching</a>', '<a href="#teaching">Docencia</a>'),
    ('<a href="#consulting">Consulting</a>', '<a href="#consulting">Consultoría</a>'),
    ('<a href="#contact">Contact</a>', '<a href="#contact">Contacto</a>'),
    # research
    ('<h2>Research</h2>', '<h2>Investigación</h2>'),
    ('<h3>Evolutionary biology</h3>', '<h3>Biología evolutiva</h3>'),
    ('<p>Statistical: fitting models of speciation and extinction to trees of living species by simulating the lineages the tree is missing, and working out what such trees can and cannot tell us.</p>',
     '<p>En lo estadístico: ajustar modelos de especiación y extinción a árboles de especies vivas simulando los linajes que le faltan al árbol, y precisar qué pueden y qué no pueden decirnos esos árboles.</p>'),
    ("<p>Biological: whether diversity limits itself, whether a lineage's age or distinctiveness changes its fate, and whether diversification rates are inherited.</p>",
     '<p>En lo biológico: si la diversidad se limita a sí misma, si la edad o la singularidad de un linaje cambian su destino, y si las tasas de diversificación se heredan.</p>'),
    ('<h3>Robust and causal regularization</h3>', '<h3>Regularización robusta y causal</h3>'),
    ("<p>With Ernst Wit: which relationships still hold when conditions change, in data where the conditions were not recorded. Applied to learning outcomes in Peru's national assessment (Conference on Complex Systems, 2026) and to problems in social and network science.</p>",
     '<p>Con Ernst Wit: qué relaciones se mantienen cuando cambian las condiciones, en datos donde las condiciones no quedaron registradas. Aplicado a los aprendizajes en la evaluación nacional del Perú (Conference on Complex Systems, 2026) y a problemas de ciencias sociales y de redes.</p>'),
    ('<h3>Other systems</h3>', '<h3>Otros sistemas</h3>'),
    ('<p>Phylogenies of stellar chemical abundances, microbiome interaction networks, and injury mortality in Chile.</p>',
     '<p>Filogenias de abundancias químicas estelares, redes de interacción del microbioma y mortalidad por lesiones en Chile.</p>'),
    ('id="publications">Publications</h3>', 'id="publications">Publicaciones</h3>'),
    ('id="talks">Talks</h3>', 'id="talks">Charlas</h3>'),
    ('; invited</span>', '; invitado</span>'),
    ('; session organiser</span>', '; organizador de sesión</span>'),
    # teaching
    ('<h2>Teaching</h2>', '<h2>Docencia</h2>'),
    ("<p class=\"lede\">I teach from primary school to PhD level: courses at USI, thesis supervision, workshops in schools, and my own children's education at home. I write the textbooks for my courses, and lately I am turning their concepts into animations.</p>",
     '<p class="lede">Enseño desde la educación básica hasta el doctorado: cursos en la USI, dirección de tesis, talleres en colegios y la educación de mis hijos en casa. Escribo los libros de texto de mis cursos y últimamente estoy convirtiendo sus conceptos en animaciones.</p>'),
    ('<h3>Now, autumn 2026</h3>', '<h3>Ahora, semestre de otoño 2026</h3>'),
    ('</a> and <a href="https://search.usi.ch/en/courses/35275101/numerical-computing">', '</a> y <a href="https://search.usi.ch/en/courses/35275101/numerical-computing">'),
    ('<h3>Earlier courses</h3>', '<h3>Cursos anteriores</h3>'),
    ('<p>Calculus 1, Probability and Statistics, Ordinary Differential Equations, Introduction to Data Science and Analysis of Social Networks.</p>',
     '<p>Cálculo 1, Probabilidad y Estadística, Ecuaciones Diferenciales Ordinarias, Introducción a la Ciencia de Datos y Análisis de Redes Sociales.</p>'),
    ('<h3>Thesis supervision</h3>', '<h3>Dirección de tesis</h3>'),
    ('<h3>Textbooks</h3>', '<h3>Libros de texto</h3>'),
    ('<p>Written for my courses: ', '<p>Escritos para mis cursos: '),
    ('<i>Irreducible Inference</i>, on statistical inference and modelling.</p>', '<i>Irreducible Inference</i>, sobre inferencia y modelación estadística.</p>'),
    ('<h3>Outreach</h3>', '<h3>Divulgación</h3>'),
    ('<p>Supervision of <a href="https://www.liceolugano1.ti.ch/studi/lavoro-di-maturita-lam">', '<p>Dirección de <a href="https://www.liceolugano1.ti.ch/studi/lavoro-di-maturita-lam">'),
    ('</a> with the Faculty of Informatics; workshops at <a href="https://www.satw.ch/en/tecdays">', '</a> con la Facultad de Informática; talleres en <a href="https://www.satw.ch/en/tecdays">'),
    ('</a> and at a <i>giornata autogestita</i>; classes at <a href="https://www.liceolugano1.ti.ch/">', '</a> y en una <i>giornata autogestita</i>; clases en el <a href="https://www.liceolugano1.ti.ch/">'),
    ('<h3>Schools and AI</h3>', '<h3>Escuela e IA</h3>'),
    ('<p>My children are homeschooled, and I build their learning material with current AI tools. From that work: curriculum-aligned learning games for Chilean primary and secondary school, at <a href="https://juegos.whitebox.cl/">',
     '<p>Mis hijos estudian en casa, y construyo su material de aprendizaje con herramientas actuales de IA. De ese trabajo salen juegos de aprendizaje alineados con el currículo chileno de enseñanza básica y media, en <a href="https://juegos.whitebox.cl/">'),
    ('<h3>Animation</h3>', '<h3>Animación</h3>'),
    ('<p>Animated explainers for the concepts in my courses, starting with <a href="https://www.stochasticmethods.com/">',
     '<p>Explicaciones animadas de los conceptos de mis cursos, empezando por <a href="https://www.stochasticmethods.com/">'),
    # consulting
    ('<h2>Consulting</h2>', '<h2>Consultoría</h2>'),
    ('<p class="lede">I am an engineer before I am a doctor, and I work more and more with small businesses, start-ups and projects outside academia. These are some of the organisations and projects I am part of now.</p>',
     '<p class="lede">Antes de ser doctor, soy ingeniero, y colaboro cada vez más con pequeñas empresas, start-ups y proyectos fuera de la academia. Estas son algunas de las organizaciones y proyectos en los que participo hoy.</p>'),
    ('<h3>Organisations I work with</h3>', '<h3>Organizaciones con las que trabajo</h3>'),
    ('<h3>Ongoing projects</h3>', '<h3>Proyectos en curso</h3>'),
    # contact
    ('<h2>Contact</h2>', '<h2>Contacto</h2>'),
    ('<p>Write to me at <a href="mailto:richtf@usi.ch">richtf@usi.ch</a> or <a href="mailto:franciscorichter@gmail.com">franciscorichter@gmail.com</a>. I work at the Faculty of Informatics, Università della Svizzera italiana, in Lugano. My code is on <a href="https://github.com/franciscorichter">GitHub</a>, and I am also on <a href="https://www.linkedin.com/in/franciscorichter/">LinkedIn</a>.</p>',
     '<p>Escríbeme a <a href="mailto:richtf@usi.ch">richtf@usi.ch</a> o a <a href="mailto:franciscorichter@gmail.com">franciscorichter@gmail.com</a>. Trabajo en la Facultad de Informática de la Università della Svizzera italiana, en Lugano. Mi código está en <a href="https://github.com/franciscorichter">GitHub</a>, y también estoy en <a href="https://www.linkedin.com/in/franciscorichter/">LinkedIn</a>.</p>'),
    ('>Your email</label>', '>Tu correo</label>'),
    ('>Subject</label>', '>Asunto</label>'),
    ('>Message</label>', '>Mensaje</label>'),
    ('>Send</button>', '>Enviar</button>'),
]

# Relative paths that point into the site, rewritten one level up for es/.
LOCAL = r'(assets|images|files|media|liceo-probability|tools)/'


def main():
    html = SRC.read_text(encoding="utf-8")
    missing = [en for en, _ in T if en not in html]
    if missing:
        print("index.html no longer contains these phrases; update the table in tools/build-es.py:", file=sys.stderr)
        for en in missing:
            print("  -", en[:110], file=sys.stderr)
        sys.exit(1)
    for en, es in T:
        html = html.replace(en, es)
    html = re.sub(r'((?:src|href|srcset|poster)=")' + LOCAL, r'\1../\2/', html)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}: {len(T)} phrases translated")


if __name__ == "__main__":
    main()

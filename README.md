# franciscorichter.github.io

Personal academic site of Francisco Richter Mendoza, served by GitHub Pages at
<https://franciscorichter.github.io>, in English and Spanish. Plain static HTML and CSS
(`.nojekyll` switches Jekyll off); the only generated file is the Spanish page.

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole site: about, research, publications, talks, teaching, consulting, contact |
| `es/index.html` | The Spanish page, **generated** from `index.html` by `tools/build-es.py`; never edit it by hand |
| `images/logos/` | Logos of the institutions and projects under Consulting, each as `<name>` and `<name>-dark` for the two colour schemes |
| `assets/site.css` | Styles. Colour tokens at the top, light and dark mode |
| `assets/site.js` | The tree's grow-and-fade on load, and the "show only what survives" toggle |
| `tools/build-es.py` | Translation table and builder of `es/index.html` |
| `tools/make_tree.py` | Simulates the birth–death tree in the header and writes it into `index.html` |
| `files/Resume/` | CV PDFs linked from the contact section (`resume.pdf`, `resume_es.pdf`) |
| `liceo-probability/` | Interactive probability-paradoxes page for students at the Liceo di Lugano |
| `images/`, `files/` | Older assets, kept so existing links keep working |

## The header tree

A constant-rate birth–death process (speciation 1.0, extinction 0.55) simulated
forward for a fixed time with a fixed seed. Lineages with no descendant alive at
the present are drawn faded: they are what a tree built from living species never
sees. To change the tree, edit `SEED` (or the rates) in `tools/make_tree.py` and run

```sh
python3 tools/make_tree.py            # rewrites the SVG between the tree markers
python3 tools/make_tree.py --search   # lists seeds with a readable balance
```

## Spanish page

`index.html` is the only source. After any edit to it, rebuild the Spanish page:

```sh
python3 tools/build-es.py
```

The script applies its translation table and stops, naming the phrase, when an English
sentence in the table no longer occurs in `index.html`: translate the new wording in the
table and run it again. Paper titles, authors, journals, course and book titles are not
translated. The messages written by `assets/site.js` (tree status, contact form) have their
Spanish text in that file, chosen by `<html lang>`.

## CV

`files/Resume/resume.pdf` is built from the canonical CV source in `~/System/Resume`
with the academic profile:

```sh
cd ~/System/Resume && ./make-cv.sh A <this repo>/files/Resume/resume
```

## Preview locally

```sh
python3 -m http.server 8765   # then open http://localhost:8765/
```

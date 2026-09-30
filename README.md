# franciscorichter.github.io

Personal academic site of Francisco Richter Mendoza, served by GitHub Pages at
<https://franciscorichter.github.io>. Plain static HTML and CSS, no build step
(`.nojekyll` switches Jekyll off).

## Layout

| Path | What it is |
|---|---|
| `index.html` | The whole site: about, research, publications, talks, teaching, contact |
| `assets/site.css` | Styles. Colour tokens at the top, light and dark mode |
| `assets/site.js` | The tree's grow-and-fade on load, and the "show only what survives" toggle |
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

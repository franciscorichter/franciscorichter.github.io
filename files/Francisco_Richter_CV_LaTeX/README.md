# Francisco Richter CV - LaTeX Source

This directory contains the LaTeX source files for Francisco Richter's CV.

## Files Structure

```
Francisco_Richter_CV_LaTeX/
├── resume.tex          # Main LaTeX file
├── russell.cls         # Custom CV class file
├── cv/                 # CV content directory
│   ├── education.tex
│   ├── experience.tex
│   ├── activities.tex
│   ├── publications.tex
│   ├── outreach.tex
│   ├── references.bib  # Bibliography file
│   └── [other sections]
└── README.md          # This file
```

## Compilation Instructions

### Requirements
- XeLaTeX (required for font support)
- Biber (for bibliography processing)
- Standard LaTeX packages

### Compilation Steps

1. **First compilation:**
   ```bash
   xelatex resume.tex
   ```

2. **Process bibliography:**
   ```bash
   biber resume
   ```

3. **Final compilation:**
   ```bash
   xelatex resume.tex
   ```

### Alternative (one-line compilation):
```bash
xelatex resume.tex && biber resume && xelatex resume.tex
```

## Output
The compilation will generate `resume.pdf` - the final CV document.

## Notes
- This CV uses the custom `russell` class for styling
- Hyperlinks are enabled throughout the document
- The bibliography includes DOIs and URLs for publications
- All workshop and media links are clickable

## Customization
- Edit individual section files in the `cv/` directory
- Modify `resume.tex` to include/exclude sections
- Update `references.bib` for publications and references

For questions or issues, contact Francisco Richter at richtf@usi.ch


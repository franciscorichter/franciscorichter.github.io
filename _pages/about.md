---
permalink: /
title: ""
excerpt: "A Journey in Data Science, Predictive Stochastic Modeling, and Statistical Network Sciences"
author_profile: true
redirect_from:
  - /about/
  - /about.html
---

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />

  <title>Francisco Richter‑Mendoza – Mathematical Engineering</title>

  <!-- ✦ Smart‑minimal CSS ✦ -->
  <style>
  :root{
    /* Colour tokens */
    --bg: #ffffff;
    --fg: #0f0f0f;
    --accent: #0066ff;
    --accent-light: #eaf2ff;

    /* Type & rhythm */
    --f-sans: -apple-system,system-ui,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
    --f-serif: "Georgia","Times New Roman",serif;
    --step-0: clamp(1rem, 0.9rem + 0.3vw, 1.125rem);  /* body text */
    --step-2: clamp(2.2rem, 1.7rem + 1.5vw, 3rem);    /* h1 */
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0f0f0f; --fg:#f5f5f5;
      --accent:#66aaff; --accent-light:#112244;
    }
  }

  /* Layout reset ---------------------------------------------------------- */
  *,*::before,*::after{box-sizing:border-box;}
  html,body{margin:0;padding:0;height:100%;}
  body{font:var(--step-0)/1.6 var(--f-sans);background:var(--bg);color:var(--fg);display:flex;flex-direction:column;}

  /* Header --------------------------------------------------------------- */
  header{padding:1.5rem 1rem;margin:0 auto;max-width:52rem;width:100%;}
  h1{font-size:var(--step-2);font-family:var(--f-serif);margin:0.5rem 0;}
  header p{margin:0;font-style:italic;color:var(--accent);}
  nav{margin-top:1rem;font-size:0.9rem;}
  nav a{margin-right:1.25rem;text-decoration:none;color:inherit;position:relative;}
  nav a::after{content:"";display:block;height:2px;width:0;background:var(--accent);transition:width .25s;}
  nav a:hover::after{width:100%;}

  /* Sections ------------------------------------------------------------- */
  section{padding:3rem 1rem;border-top:1px solid var(--accent-light);max-width:52rem;margin:0 auto;}
  section:first-of-type{border-top:none;padding-top:0;}

  h2{margin:0 0 1rem;font-family:var(--f-serif);font-size:1.5rem;}
  ul{padding-left:1.25rem;}
  a{color:var(--accent);}
  a:hover{color:var(--fg);background:var(--accent);}

  /* Tiny enhancements ---------------------------------------------------- */
  .pillars li{margin-bottom:1rem;}
  .contact{margin-top:2rem;}
  .contact a{font-weight:600;}

  /* Progressive disclosure: fade‑in as you scroll (no JS) ---------------- */
  @supports (animation-timeline: view()){
    [data-fade]{opacity:0;view-timeline-name: --reveal;animation-timeline: --reveal;animation-range: entry 5% cover 30%;animation: fade .8s ease-out forwards;}
    @keyframes fade{to{opacity:1;transform:none}}
    [data-fade]{transform:translateY(24px);}
  }
  </style>
</head>

<body>

<header>
  <h1 data-fade>Solving Complex Problems<br>with Mathematical Engineering</h1>
  <p data-fade>A lightweight, data‑driven approach to innovation</p>

  <nav aria-label="Quick links" data-fade>
    <a href="#intro">About me</a>
    <a href="#pillars">My&nbsp;approach</a>
    <a href="#collab">Collaborations</a>
    <a href="#contact">Contact</a>
  </nav>
</header>

<main>
  <!-- — Intro ----------------------------------------------------------- -->
  <section id="intro" data-fade>
    <p>
      I’m <strong>Francisco&nbsp;Richter‑Mendoza</strong>, a
      <a href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/files/CV.pdf" target="_blank" rel="noopener">postdoctoral researcher & mathematical engineer</a>
      at the
      <a href="https://www.ci.inf.usi.ch/research/statslab/people/" target="_blank" rel="noopener">Statistical Computing Laboratory</a>
      (Università della Svizzera italiana).
      My work develops new tools in data science, predictive stochastic modelling, and statistical network science to tackle real‑world complexity.
    </p>
  </section>

  <!-- — Pillars --------------------------------------------------------- -->
  <section id="pillars" class="pillars" data-fade>
    <h2>My&nbsp;Approach</h2>
    <ul>
      <li><strong>Teaching&nbsp;</strong>— engaging UG & PG students in data science, networks, and statistical methods; supervising MSc theses in Computational Science and AI.</li>
      <li><strong>Research&nbsp;</strong>— advancing methodologies for diversification dynamics & environmental data imputation; building bridges between Chile and Switzerland.</li>
      <li><strong>Applied Mathematics&nbsp;</strong>— translating rigorous theory into actionable solutions that deliver impact.</li>
    </ul>
  </section>

  <!-- — Collaborations -------------------------------------------------- -->
  <section id="collab" data-fade>
    <h2>Inspirations & Collaborations</h2>
    <p>
      From outstanding mentors to cross‑disciplinary teams, collaborative inquiry is the engine of my research,
      enriching every project with multiple perspectives and skill‑sets.
    </p>
  </section>

  <!-- — Contact --------------------------------------------------------- -->
  <section id="contact" class="contact" data-fade>
    <p>
      Curious about potential projects or joint research?  
      <a href="mailto:richtf@usi.ch">Let’s start the conversation →</a>
    </p>
  </section>
</main>

</body>
</html>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF‑8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Francisco Richter‑Mendoza</title>
  <style>
    :root {
      --bg:   #121212;
      --fg:   #eee;
      --muted:#aaa;
      --acc:  #65aaff;
      --gap:  1.5rem;
      --side: 240px;
      --fw:   500;
      --fs‑h1:2.25rem;
      --fs‑h2:1.25rem;
      --ff‑sans:system-ui,‑apple‑system,Segoe UI,Roboto,Arial,sans-serif;
      --ff‑serif:Georgia,serif;
    }
    body {
      margin:0;
      display:grid;
      grid-template-areas:
        "header header"
        "sidebar main";
      grid-template-columns: var(--side) 1fr;
      min-height:100vh;
      background:var(--bg);
      color:var(--fg);
      font-family: var(--ff‑sans);
      line-height:1.6;
    }
    header {
      grid-area: header;
      background: #1e1e1e;
      padding: var(--gap);
      display:flex;
      align-items:center;
      justify-content: space-between;
    }
    header nav a {
      color: var(--fg);
      text-decoration: none;
      font-weight: var(--fw);
      margin-left: var(--gap);
      position: relative;
    }
    header nav a::after {
      content:"";
      position:absolute;
      left:0; bottom:-2px;
      width:0; height:2px;
      background: var(--acc);
      transition: width .3s;
    }
    header nav a:hover::after {
      width:100%;
    }

    .sidebar {
      grid-area: sidebar;
      background:#1a1a1a;
      padding:var(--gap);
      border-right:1px solid #333;
      text-align:center;
    }
    .sidebar img {
      width:100px; height:100px;
      border-radius:50%;
      object-fit:cover;
      margin-bottom: var(--gap);
    }
    .sidebar h2 {
      margin:0; font-size:1.125rem;
    }
    .sidebar p {
      margin:.25rem 0 .75rem;
      font-size:.875rem;
      color: var(--muted);
    }
    .sidebar a {
      display:block;
      margin: .5rem 0;
      font-size:.9rem;
      color: var(--acc);
      text-decoration:none;
    }
    .sidebar a:hover {
      text-decoration:underline;
    }

    main {
      grid-area: main;
      padding: calc(var(--gap)*1.5) var(--gap);
      max-width: 700px;
      margin: 0 auto;
    }
    h1 {
      font-family: var(--ff‑serif);
      font-size: var(--fs‑h1);
      margin:0 0 .5rem;
    }
    .lead {
      font-size:1rem;
      color: var(--acc);
      margin:0 0 2rem;
    }
    h2 {
      font-size: var(--fs‑h2);
      margin-top:2.5rem;
      font-family: var(--ff‑serif);
    }
    ul {
      padding-left:1.25rem;
      margin:0;
    }
    ul li {
      margin-bottom: .75rem;
    }
    a {
      color: var(--acc);
    }
    a:hover {
      text-decoration:underline;
    }
    .contact {
      margin-top:2rem;
      font-weight: var(--fw);
    }
  </style>
</head>
<body>

  <header>
    <div><strong>Francisco Richter‑Mendoza</strong></div>
    <nav>
      <a href="#intro">About</a>
      <a href="#pillars">Approach</a>
      <a href="#collab">Collab’s</a>
      <a href="#contact">Contact</a>
    </nav>
  </header>

  <aside class="sidebar">
    <!-- replace src with your logo or photo -->
    <img src="/assets/img/profile.jpg" alt="Francisco Richter">
    <h2>Mathematical Engineer</h2>
    <p>🔹 Lugano, Switzerland</p>
    <a href="mailto:richtf@usi.ch">✉ Email</a>
    <a href="https://linkedin.com/in/…">in LinkedIn</a>
    <a href="https://github.com/…">🐙 GitHub</a>
    <a href="https://orcid.org/…">ORCID</a>
  </aside>

  <main>
    <h1>Solving Complex Problems with Mathematical Engineering</h1>
    <p class="lead">A lightweight, data‑driven approach to innovation</p>

    <section id="intro">
      <p>
        I’m <strong>Francisco Richter‑Mendoza</strong>, a 
        <a href="…CV.pdf" target="_blank" rel="noopener">postdoctoral researcher & mathematical engineer</a>
        at the 
        <a href="…statslab/people/" target="_blank" rel="noopener">Statistical Computing Laboratory</a>
        (Università della Svizzera italiana). My work develops new tools in data science, predictive stochastic modelling, and statistical network science to tackle real‑world complexity.
      </p>
    </section>

    <section id="pillars">
      <h2>My Approach</h2>
      <ul>
        <li><strong>Teaching</strong> — Engaging UG & PG students in data science, networks, and statistical methods; supervising MSc theses.</li>
        <li><strong>Research</strong> — Advancing methodologies for diversification dynamics & environmental data imputation; bridging Chile & Switzerland.</li>
        <li><strong>Applied Mathematics</strong> — Transforming theory into real‑world solutions that make an impact.</li>
      </ul>
    </section>

    <section id="collab">
      <h2>Inspirations & Collaborations</h2>
      <p>
        I’ve been lucky to work with brilliant mentors and multidisciplinary teams—every project thrives on diverse perspectives.
      </p>
    </section>

    <section id="contact" class="contact">
      Curious about collaborating?  
      <a href="mailto:richtf@usi.ch">Let’s chat →</a>
    </section>
  </main>

</body>
</html>

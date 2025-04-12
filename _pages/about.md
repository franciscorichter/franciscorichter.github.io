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
  <meta charset="UTF-8" />
  <title>Particle System + Personal Intro</title>
  
  <!-- p5.js library (hosted by cdn.jsdelivr.net) -->
  <script src="https://cdn.jsdelivr.net/npm/p5@1.4.0/lib/p5.min.js"></script>
</head>

<body>

<!-- ------------------------------ 
     Your Jekyll/HTML Content 
------------------------------ -->
<div class="hero">
  <h1>Solving Complex Problems with Mathematical Engineering</h1>
  <p class="lead">
    Empowering innovation through data-driven approaches, predictive modeling, and advanced statistical network analysis.
  </p>
</div>

<div class="introduction">
  <p>
    I’m <strong>Francisco Richter-Mendoza</strong>, a 
    <a href="https://raw.githubusercontent.com/franciscorichter/franciscorichter.github.io/master/files/CV.pdf" target="_blank">
      postdoctoral researcher and mathematical engineer
    </a> 
    at the 
    <a href="https://www.ci.inf.usi.ch/research/statslab/people/" target="_blank">
      Statistical Computing Laboratory
    </a> 
    at Università della Svizzera italiana. My work centers on developing innovative methods in data science, predictive stochastic modeling, and statistical network sciences to address complex real-world problems.
  </p>
</div>

<div class="pillars">
  <h2>My Approach</h2>
  <p>My work is built upon three core pillars:</p>
  <ul>
    <li>
      <strong>Teaching</strong>: Engaging undergraduate and graduate students with courses in data science, network analysis, and statistical methods. I also supervise master’s theses for the Master in Computational Science and the Master in Artificial Intelligence programs—blending pedagogy with cutting-edge research.
    </li>
    <li>
      <strong>Research</strong>: Developing advanced statistical methodologies to tackle complex systems, with a focus on diversification dynamics and environmental data imputation. I actively foster interdisciplinary collaborations, particularly between Chile and Switzerland.
    </li>
    <li>
      <strong>Applied Mathematics</strong>: Applying robust statistical techniques to solve practical challenges, effectively transforming theoretical mathematical concepts into innovative, real-world solutions.
    </li>
  </ul>
</div>

<div class="experience">
  <h2>Inspirations & Collaborations</h2>
  <p>
    I am fortunate to have worked with inspiring mentors across various fields whose guidance has significantly shaped my work. Collaborating with students and colleagues from diverse backgrounds enriches our multidisciplinary, international projects.
  </p>
</div>

<div class="contact">
  <p>
    For collaborations or further information, feel free to 
    <a href="mailto:richtf@usi.ch">reach out via email</a>.
  </p>
</div>

<!-- ------------------------------ 
     p5.js Particle System Canvas 
------------------------------ -->
<!-- You can style this with CSS or add inline styles as needed. -->
<div id="particle-canvas-container" style="position:relative; z-index:-1;">
  <!-- The canvas from p5.js will be placed here automatically. -->
</div>

<script>
// ---------------------------------------------------------
// Configuration & Variables
// ---------------------------------------------------------
let particles = [];
const numParticles = 150;    // Number of particles
const maxSpeed = 2;          // Max velocity
const particleSize = 5;      // Base size for particles
const connectionDistance = 120; 
let colorShift = 0;          
let repulsionMode = false;   
let lastFrameTimes = [];     
let fpsUpdateInterval = 10;  
let useQuadtree = true;      
let quadtree;                
let lastFrameCount = 0;      
let frameRateVal = 0;        

// ---------------------------------------------------------
// p5.js Setup Function
// ---------------------------------------------------------
function setup() {
  // Create canvas that fills the window
  let canvas = createCanvas(windowWidth, windowHeight);
  
  // Optionally attach the canvas to a specific div
  canvas.parent('particle-canvas-container');
  
  // Use HSB color mode for easier hue manipulation
  colorMode(HSB, 360, 100, 100, 1);
  
  // Initialize the particles
  for (let i = 0; i < numParticles; i++) {
    particles.push(new Particle());
  }
  
  textSize(16);
  textAlign(LEFT, TOP);

  // Initialize quadtree
  quadtree = new QuadTree(new Boundary(width/2, height/2, width/2, height/2), 4);
}

// ---------------------------------------------------------
// p5.js Draw Function (called every frame)
// ---------------------------------------------------------
function draw() {
  // Calculate a rough FPS every fpsUpdateInterval frames
  if (frameCount % fpsUpdateInterval === 0) {
    const currentTime = millis();
    if (lastFrameCount > 0) {
      const elapsed = currentTime - lastFrameTimes[lastFrameTimes.length - 1];
      frameRateVal = (fpsUpdateInterval / (elapsed / 1000)).toFixed(1);
    }
    lastFrameTimes.push(currentTime);
    if (lastFrameTimes.length > 10) lastFrameTimes.shift();
    lastFrameCount = frameCount;
  }
  
  // A translucent background to create a trailing effect
  background(0, 0, 0, 0.05);
  
  // Slightly shift global color each frame
  colorShift = (colorShift + 0.2) % 360;
  
  // Rebuild quadtree if using it
  if (useQuadtree) {
    quadtree = new QuadTree(new Boundary(width/2, height/2, width/2, height/2), 4);
    for (let p of particles) {
      quadtree.insert(p);
    }
  }
  
  // Update and render particles, and connect close neighbors
  for (let i = 0; i < particles.length; i++) {
    particles[i].update();
    particles[i].display();
    
    if (useQuadtree) {
      // Efficient neighbor lookup
      let range = new Circle(particles[i].pos.x, particles[i].pos.y, connectionDistance);
      let neighbors = [];
      quadtree.query(range, neighbors);
      
      for (let neighbor of neighbors) {
        if (neighbor === particles[i] || particles.indexOf(neighbor) <= i) continue;
        let d = dist(particles[i].pos.x, particles[i].pos.y, neighbor.pos.x, neighbor.pos.y);
        if (d < connectionDistance) {
          drawConnection(particles[i], neighbor, d);
        }
      }
    } else {
      // Brute force approach
      for (let j = i + 1; j < particles.length; j++) {
        let d = dist(particles[i].pos.x, particles[i].pos.y, particles[j].pos.x, particles[j].pos.y);
        if (d < connectionDistance) {
          drawConnection(particles[i], particles[j], d);
        }
      }
    }
  }
  
  displayUI();
}

// ---------------------------------------------------------
// Draw connection line between two particles
// ---------------------------------------------------------
function drawConnection(p1, p2, distance) {
  let alpha = map(distance, 0, connectionDistance, 1, 0);
  let sw = map(distance, 0, connectionDistance, 2, 0.1);
  strokeWeight(sw);

  let connectionHue = (p1.hue + colorShift) % 360;
  stroke(connectionHue, 80, 100, alpha);

  line(p1.pos.x, p1.pos.y, p2.pos.x, p2.pos.y);
}

// ---------------------------------------------------------
// Display UI (instructions and stats)
// ---------------------------------------------------------
function displayUI() {
  noStroke();
  fill(0, 0, 0, 0.5);
  rect(10, 10, 320, 110, 10);

  fill(255);
  text("Click and drag: " + (repulsionMode ? "Repel" : "Attract") + " particles", 20, 20);
  text("Press 'R' to toggle attract/repel mode", 20, 45);
  text("Press 'A' to add particles, 'D' to remove", 20, 70);
  text("Particles: " + particles.length + " | FPS: " + frameRateVal, 20, 95);
}

// ---------------------------------------------------------
// Particle Class
// ---------------------------------------------------------
class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(random(-maxSpeed, maxSpeed), random(-maxSpeed, maxSpeed));
    this.acc = createVector(0, 0);
    this.hue = random(360);
    this.baseSize = random(particleSize * 0.5, particleSize * 1.5);
    this.size = this.baseSize;
    this.pulseSpeed = random(0.02, 0.06);
    this.pulseOffset = random(TWO_PI);
  }

  update() {
    // Attract/repel toward mouse if pressed
    if (mouseIsPressed) {
      let mousePos = createVector(mouseX, mouseY);
      let dir = p5.Vector.sub(mousePos, this.pos);
      let distance = dir.mag();
      if (distance > 5) {
        dir.normalize();
        if (repulsionMode) {
          dir.mult(-1); // reverse if repelling
        }
        let strength = constrain(1 / (distance * 0.03), 0, 0.8);
        dir.mult(strength);
        this.acc = dir;
      }
    } else {
      this.acc.set(0, 0);
    }

    // Add small random acceleration for organic feel
    this.acc.add(p5.Vector.random2D().mult(0.01));

    // Update velocity, position
    this.vel.add(this.acc);
    this.vel.limit(maxSpeed);
    this.pos.add(this.vel);

    // Dampening
    this.vel.mult(0.99);

    // Wrap around edges
    if (this.pos.x < 0) this.pos.x = width;
    if (this.pos.x > width) this.pos.x = 0;
    if (this.pos.y < 0) this.pos.y = height;
    if (this.pos.y > height) this.pos.y = 0;

    // Pulsing size
    this.size = this.baseSize + sin(frameCount * this.pulseSpeed + this.pulseOffset) * (this.baseSize * 0.3);

    // Gradually shift hue
    this.hue = (this.hue + 0.1) % 360;
  }

  display() {
    // Glowing layers
    for (let i = 3; i > 0; i--) {
      let alpha = map(i, 3, 1, 0.1, 0.8);
      let size = this.size * map(i, 3, 1, 2, 1);
      noStroke();
      fill(this.hue, 80, 100, alpha);
      ellipse(this.pos.x, this.pos.y, size);
    }
    
    // Core
    fill(this.hue, 80, 100, 1);
    ellipse(this.pos.x, this.pos.y, this.size * 0.7);
  }
}

// ---------------------------------------------------------
// Spatial Partitioning Classes
// ---------------------------------------------------------
class Boundary {
  constructor(x, y, w, h) {
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }
  
  contains(point) {
    return (
      point.pos.x >= this.x - this.w &&
      point.pos.x < this.x + this.w &&
      point.pos.y >= this.y - this.h &&
      point.pos.y < this.y + this.h
    );
  }
  
  intersects(range) {
    return !(
      range.x - range.r > this.x + this.w ||
      range.x + range.r < this.x - this.w ||
      range.y - range.r > this.y + this.h ||
      range.y + range.r < this.y - this.h
    );
  }
}

class Circle {
  constructor(x, y, r) {
    this.x = x;
    this.y = y;
    this.r = r;
  }
}

class QuadTree {
  constructor(boundary, capacity) {
    this.boundary = boundary;
    this.capacity = capacity;
    this.points = [];
    this.divided = false;
  }
  
  subdivide() {
    let x = this.boundary.x;
    let y = this.boundary.y;
    let w = this.boundary.w / 2;
    let h = this.boundary.h / 2;
    
    let ne = new Boundary(x + w, y - h, w, h);
    this.northeast = new QuadTree(ne, this.capacity);
    
    let nw = new Boundary(x - w, y - h, w, h);
    this.northwest = new QuadTree(nw, this.capacity);
    
    let se = new Boundary(x + w, y + h, w, h);
    this.southeast = new QuadTree(se, this.capacity);
    
    let sw = new Boundary(x - w, y + h, w, h);
    this.southwest = new QuadTree(sw, this.capacity);
    
    this.divided = true;
  }
  
  insert(point) {
    if (!this.boundary.contains(point)) {
      return false;
    }
    if (this.points.length < this.capacity) {
      this.points.push(point);
      return true;
    }
    if (!this.divided) {
      this.subdivide();
    }
    
    return (
      this.northeast.insert(point) ||
      this.northwest.insert(point) ||
      this.southeast.insert(point) ||
      this.southwest.insert(point)
    );
  }
  
  query(range, found) {
    if (!found) found = [];
    if (!this.boundary.intersects(range)) {
      return found;
    }
    for (let p of this.points) {
      let d = dist(range.x, range.y, p.pos.x, p.pos.y);
      if (d < range.r) {
        found.push(p);
      }
    }
    if (this.divided) {
      this.northeast.query(range, found);
      this.northwest.query(range, found);
      this.southeast.query(range, found);
      this.southwest.query(range, found);
    }
    return found;
  }
}

// ---------------------------------------------------------
// Handle Window Resizing
// ---------------------------------------------------------
function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}

// ---------------------------------------------------------
// Handle Keyboard Input
// ---------------------------------------------------------
function keyPressed() {
  // Toggle repulsion/attraction
  if (key === 'r' || key === 'R') {
    repulsionMode = !repulsionMode;
  }
  
  // Add 10 particles
  if (key === 'a' || key === 'A') {
    for (let i = 0; i < 10; i++) {
      particles.push(new Particle());
    }
  }
  
  // Remove 10 particles
  if ((key === 'd' || key === 'D') && particles.length > 10) {
    for (let i = 0; i < 10; i++) {
      particles.pop();
    }
  }
  
  // Toggle quadtree usage
  if (key === 'q' || key === 'Q') {
    useQuadtree = !useQuadtree;
  }
  
  // Clear all and reset
  if (key === ' ') {
    particles = [];
    for (let i = 0; i < numParticles; i++) {
      particles.push(new Particle());
    }
  }
  
  return false; // Prevent default browser behavior
}
</script>

</body>
</html>

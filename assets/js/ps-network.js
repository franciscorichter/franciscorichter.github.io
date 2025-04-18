document.addEventListener('DOMContentLoaded', function() {
  // Cargar p5.js dinámicamente
  var script = document.createElement('script');
  script.src = 'https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js';
  script.onload = function()  {
    // Una vez cargado p5.js, iniciar el sketch
    new p5(function(p) {
      let nodes = [];
      let edges = [];
      
      p.setup = function() {
        let container = document.getElementById('network');
        if (!container) return;
        
        let canvas = p.createCanvas(300, 300);
        canvas.parent(container);
        
        // Crear nodos
        for (let i = 0; i < 12; i++) {
          let angle = (i / 12) * p.TWO_PI;
          let radius = p.random(50, 120);
          let x = p.cos(angle) * radius + 150;
          let y = p.sin(angle) * radius + 150;
          
          nodes.push({
            x: x,
            y: y,
            size: p.random(6, 12),
            vx: 0,
            vy: 0
          });
        }
        
        // Crear conexiones
        for (let i = 0; i < nodes.length; i++) {
          let connections = p.floor(p.random(2, 4));
          for (let j = 0; j < connections; j++) {
            let target = p.floor(p.random(nodes.length));
            if (target !== i) {
              edges.push({
                from: i,
                to: target,
                opacity: p.random(0.2, 0.5)
              });
            }
          }
        }
      };
      
      p.draw = function() {
        p.clear();
        
        // Actualizar nodos
        for (let i = 0; i < nodes.length; i++) {
          nodes[i].vx = nodes[i].vx * 0.9 + p.random(-0.5, 0.5) * 0.2;
          nodes[i].vy = nodes[i].vy * 0.9 + p.random(-0.5, 0.5) * 0.2;
          
          if (nodes[i].x + nodes[i].vx < 0 || nodes[i].x + nodes[i].vx > 300) nodes[i].vx *= -1;
          if (nodes[i].y + nodes[i].vy < 0 || nodes[i].y + nodes[i].vy > 300) nodes[i].vy *= -1;
          
          nodes[i].x += nodes[i].vx;
          nodes[i].y += nodes[i].vy;
        }
        
        // Dibujar conexiones
        for (let i = 0; i < edges.length; i++) {
          let from = nodes[edges[i].from];
          let to = nodes[edges[i].to];
          
          p.stroke(200, 200, 200, edges[i].opacity * 255);
          p.strokeWeight(1);
          p.line(from.x, from.y, to.x, to.y);
        }
        
        // Dibujar nodos
        for (let i = 0; i < nodes.length; i++) {
          p.noStroke();
          p.fill(170, 170, 170, 200);
          p.ellipse(nodes[i].x, nodes[i].y, nodes[i].size, nodes[i].size);
        }
      };
    });
  };
  document.head.appendChild(script);
});


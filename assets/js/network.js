document.addEventListener('DOMContentLoaded', function() {
    const network = document.getElementById('network');
    
    // Create a more sophisticated network
    const nodeCount = 12;
    const nodes = [];
    
    // Create nodes
    for (let i = 0; i < nodeCount; i++) {
        const node = document.createElement('div');
        node.className = 'node';
        
        // Vary node sizes for more visual interest
        const size = Math.random() * 6 + 8; // Between 8px and 14px
        node.style.width = `${size}px`;
        node.style.height = `${size}px`;
        
        // Position nodes in a more natural network pattern
        const angle = (i / nodeCount) * Math.PI * 2;
        const radius = Math.random() * 100 + 50;
        const x = Math.cos(angle) * radius + 150;
        const y = Math.sin(angle) * radius + 150;
        
        node.style.left = `${x}px`;
        node.style.top = `${y}px`;
        
        // Add subtle opacity variation
        node.style.opacity = Math.random() * 0.5 + 0.5;
        
        network.appendChild(node);
        nodes.push({
            element: node,
            x: x,
            y: y,
            vx: 0,
            vy: 0
        });
    }
    
    // Create edges (connections between nodes)
    for (let i = 0; i < nodeCount; i++) {
        // Connect each node to 2-3 other nodes
        const connections = Math.floor(Math.random() * 2) + 2;
        
        for (let j = 0; j < connections; j++) {
            // Connect to a random node
            const targetIndex = Math.floor(Math.random() * nodeCount);
            if (targetIndex !== i) {
                const edge = document.createElement('div');
                edge.className = 'edge';
                
                const sourceX = parseFloat(nodes[i].element.style.left);
                const sourceY = parseFloat(nodes[i].element.style.top);
                const targetX = parseFloat(nodes[targetIndex].element.style.left);
                const targetY = parseFloat(nodes[targetIndex].element.style.top);
                
                // Calculate distance and angle
                const dx = targetX - sourceX;
                const dy = targetY - sourceY;
                const distance = Math.sqrt(dx * dx + dy * dy);
                const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                
                // Position and rotate the edge
                edge.style.width = `${distance}px`;
                edge.style.left = `${sourceX + 5}px`; // Adjust for node center
                edge.style.top = `${sourceY + 5}px`; // Adjust for node center
                edge.style.transform = `rotate(${angle}deg)`;
                
                // Add subtle opacity variation
                edge.style.opacity = Math.random() * 0.3 + 0.2;
                
                network.appendChild(edge);
            }
        }
    }
    
    // Add subtle animation to nodes
    setInterval(() => {
        nodes.forEach(node => {
            // Add small random movement
            const currentX = parseFloat(node.element.style.left);
            const currentY = parseFloat(node.element.style.top);
            
            // Calculate new position with subtle movement
            node.vx = node.vx * 0.9 + (Math.random() - 0.5) * 0.5;
            node.vy = node.vy * 0.9 + (Math.random() - 0.5) * 0.5;
            
            // Keep nodes within bounds
            if (currentX + node.vx < 0 || currentX + node.vx > 300) node.vx *= -1;
            if (currentY + node.vy < 0 || currentY + node.vy > 300) node.vy *= -1;
            
            // Apply movement
            node.element.style.left = (currentX + node.vx) + 'px';
            node.element.style.top = (currentY + node.vy) + 'px';
        });
        
        // Update edges
        const edges = document.querySelectorAll('.edge');
        edges.forEach(edge => {
            // Find connected nodes (this is simplified)
            const edgeLeft = parseFloat(edge.style.left) - 5; // Adjust for earlier offset
            const edgeTop = parseFloat(edge.style.top) - 5; // Adjust for earlier offset
            
            // Find closest node as source
            let sourceNode = null;
            let minDistance = Infinity;
            
            nodes.forEach(node => {
                const nodeX = parseFloat(node.element.style.left);
                const nodeY = parseFloat(node.element.style.top);
                const distance = Math.sqrt((nodeX - edgeLeft) ** 2 + (nodeY - edgeTop) ** 2);
                
                if (distance < minDistance) {
                    minDistance = distance;
                    sourceNode = node;
                }
            });
            
            if (sourceNode) {
                // Find target node based on angle
                const angle = parseFloat(edge.style.transform.replace('rotate(', '').replace('deg)', '')) * Math.PI / 180;
                const length = parseFloat(edge.style.width);
                const targetX = edgeLeft + Math.cos(angle) * length;
                const targetY = edgeTop + Math.sin(angle) * length;
                
                // Find closest node to target position
                let targetNode = null;
                minDistance = Infinity;
                
                nodes.forEach(node => {
                    const nodeX = parseFloat(node.element.style.left);
                    const nodeY = parseFloat(node.element.style.top);
                    const distance = Math.sqrt((nodeX - targetX) ** 2 + (nodeY - targetY) ** 2);
                    
                    if (distance < minDistance && node !== sourceNode) {
                        minDistance = distance;
                        targetNode = node;
                    }
                });
                
                if (targetNode) {
                    // Update edge position and rotation
                    const sourceX = parseFloat(sourceNode.element.style.left);
                    const sourceY = parseFloat(sourceNode.element.style.top);
                    const targetX = parseFloat(targetNode.element.style.left);
                    const targetY = parseFloat(targetNode.element.style.top);
                    
                    const dx = targetX - sourceX;
                    const dy = targetY - sourceY;
                    const distance = Math.sqrt(dx * dx + dy * dy);
                    const angle = Math.atan2(dy, dx) * 180 / Math.PI;
                    
                    edge.style.width = `${distance}px`;
                    edge.style.left = `${sourceX + 5}px`; // Center of node
                    edge.style.top = `${sourceY + 5}px`; // Center of node
                    edge.style.transform = `rotate(${angle}deg)`;
                }
            }
        });
    }, 50);
});

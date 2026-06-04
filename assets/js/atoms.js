/**
 * atoms.js
 * A custom physics-based HTML5 canvas particle connector ("moving atoms") animation.
 * Automatically adapts particle colors by parsing active CSS theme custom properties.
 */
class AtomParticles {
  constructor(canvasContainer, options = {}) {
    if (!canvasContainer) return;
    this.container = canvasContainer;
    this.canvas = document.createElement('canvas');
    this.canvas.className = 'atoms-canvas';
    this.canvas.style.position = 'absolute';
    this.canvas.style.top = '0';
    this.canvas.style.left = '0';
    this.canvas.style.width = '100%';
    this.canvas.style.height = '100%';
    this.canvas.style.pointerEvents = 'none';
    this.canvas.style.zIndex = '1';
    this.container.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');

    this.particles = [];
    this.density = options.density || 16000; // px^2 per particle
    this.maxParticles = options.maxParticles || 65;
    this.minParticles = options.minParticles || 15;
    this.speedFactor = options.speed || 0.45;
    this.lineDist = options.lineDist || 115;
    this.colorVar = options.colorVar || '--accent-teal';
    this.fallbackColor = options.fallbackColor || '#22d3ee';

    this.resize = this.resize.bind(this);
    this.animate = this.animate.bind(this);

    window.addEventListener('resize', this.resize);
    this.resize();
    this.initParticles();
    this.animate();
  }

  resize() {
    const rect = this.container.getBoundingClientRect();
    this.width = rect.width;
    this.height = rect.height;
    
    // Scale canvas pixels for high-DPI displays
    const dpr = window.devicePixelRatio || 1;
    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.ctx.resetTransform();
    this.ctx.scale(dpr, dpr);
    
    // Adjust particle count dynamically based on the current dimensions
    const targetCount = Math.min(
      this.maxParticles,
      Math.max(this.minParticles, Math.floor((this.width * this.height) / this.density))
    );
    
    if (this.particles.length < targetCount) {
      while (this.particles.length < targetCount) {
        this.particles.push(this.createParticle(true));
      }
    } else if (this.particles.length > targetCount) {
      this.particles.length = targetCount;
    }
  }

  createParticle(randomPos = false) {
    return {
      x: randomPos ? Math.random() * this.width : (Math.random() > 0.5 ? 0 : this.width),
      y: randomPos ? Math.random() * this.height : (Math.random() > 0.5 ? 0 : this.height),
      vx: (Math.random() * 2 - 1) * this.speedFactor,
      vy: (Math.random() * 2 - 1) * this.speedFactor,
      radius: Math.random() * 1.5 + 1.2
    };
  }

  initParticles() {
    const count = Math.min(
      this.maxParticles,
      Math.max(this.minParticles, Math.floor((this.width * this.height) / this.density))
    );
    this.particles = [];
    for (let i = 0; i < count; i++) {
      this.particles.push(this.createParticle(true));
    }
  }

  getRGBColor() {
    const computed = getComputedStyle(document.documentElement);
    let val = computed.getPropertyValue(this.colorVar).trim();
    if (!val) val = this.fallbackColor;

    // Hex format (#ffffff or #fff)
    if (val.startsWith('#')) {
      const hex = val.slice(1);
      let r, g, b;
      if (hex.length === 3) {
        r = parseInt(hex[0] + hex[0], 16);
        g = parseInt(hex[1] + hex[1], 16);
        b = parseInt(hex[2] + hex[2], 16);
      } else {
        r = parseInt(hex.slice(0, 2), 16);
        g = parseInt(hex.slice(2, 4), 16);
        b = parseInt(hex.slice(4, 6), 16);
      }
      return `${r}, ${g}, ${b}`;
    }

    // RGB/RGBA format already
    if (val.startsWith('rgb')) {
      const match = val.match(/\d+\s*,\s*\d+\s*,\s*\d+/);
      if (match) return match[0];
    }

    return '34, 211, 238'; // fallback cyan
  }

  animate() {
    // Clear canvas
    this.ctx.clearRect(0, 0, this.width, this.height);

    const rgb = this.getRGBColor();

    // Update and draw particles
    for (let p of this.particles) {
      p.x += p.vx;
      p.y += p.vy;

      // Bounce off walls
      if (p.x < 0 || p.x > this.width) p.vx *= -1;
      if (p.y < 0 || p.y > this.height) p.vy *= -1;

      // Keep inside bounds
      if (p.x < 0) p.x = 0;
      if (p.x > this.width) p.x = this.width;
      if (p.y < 0) p.y = 0;
      if (p.y > this.height) p.y = this.height;

      // Draw particle circle
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(${rgb}, 0.22)`;
      this.ctx.fill();
    }

    // Draw lines connecting close particles
    for (let i = 0; i < this.particles.length; i++) {
      const p1 = this.particles[i];
      for (let j = i + 1; j < this.particles.length; j++) {
        const p2 = this.particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const dist = Math.sqrt(dx * dx + dy * dy);

        if (dist < this.lineDist) {
          const alpha = (1 - dist / this.lineDist) * 0.14;
          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.strokeStyle = `rgba(${rgb}, ${alpha})`;
          this.ctx.lineWidth = 0.8;
          this.ctx.stroke();
        }
      }
    }

    requestAnimationFrame(this.animate);
  }
}

// Auto-init on DOMContentLoaded
document.addEventListener('DOMContentLoaded', () => {
  // Testimonials background canvas
  const testimonialsSec = document.getElementById('testimonials');
  if (testimonialsSec) {
    new AtomParticles(testimonialsSec, {
      density: 15000,
      maxParticles: 55,
      speed: 0.4,
      lineDist: 110,
      colorVar: '--accent-teal',
      fallbackColor: '#22d3ee'
    });
  }

  // Credentials Horizontal Strip background canvas
  const credentialsStrip = document.querySelector('.credentials-strip');
  if (credentialsStrip) {
    new AtomParticles(credentialsStrip, {
      density: 10000,
      maxParticles: 35,
      speed: 0.35,
      lineDist: 100,
      colorVar: '--accent-terracotta',
      fallbackColor: '#e2876f'
    });
  }
});

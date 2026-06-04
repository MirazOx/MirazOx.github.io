/**
 * atoms.js
 * A custom physics-based HTML5 canvas particle animation.
 * Replicates the gentle rising water bubble / twinkling star style from the mentors page,
 * while dynamically adapting particle colors using active CSS theme custom properties.
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
    this.density = options.density || 9000; // px^2 per particle
    this.maxParticles = options.maxParticles || 150;
    this.minParticles = options.minParticles || 30;
    this.colorVar = options.colorVar || '--accent-teal';
    this.fallbackColor = options.fallbackColor || '#22d3ee';

    this.resize = this.resize.bind(this);
    this.animate = this.animate.bind(this);

    window.addEventListener('resize', this.resize);
    this.resize();
    this.animate();
  }

  resize() {
    const rect = this.container.getBoundingClientRect();
    this.width = rect.width;
    this.height = rect.height;
    
    // Scale canvas pixels for high-DPI displays
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    this.canvas.width = this.width * dpr;
    this.canvas.height = this.height * dpr;
    this.canvas.style.width = this.width + 'px';
    this.canvas.style.height = this.height + 'px';
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
      x: Math.random() * this.width,
      y: randomPos ? Math.random() * this.height : this.height + 4,
      r: Math.random() * 1.8 + 0.5,
      baseA: Math.random() * 0.45 + 0.15,
      a: Math.random(),
      tw: Math.random() * 0.025 + 0.005,   // twinkle/fade speed
      dir: Math.random() < 0.5 ? 1 : -1,
      vy: -(Math.random() * 0.22 + 0.05),  // gentle upward drift
      vx: (Math.random() - 0.5) * 0.12     // slight horizontal sway
    };
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
    this.ctx.clearRect(0, 0, this.width, this.height);

    const rgb = this.getRGBColor();
    const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    for (let p of this.particles) {
      // Update opacity / twinkle
      p.a += p.tw * p.dir;
      if (p.a > 1) {
        p.a = 1; 
        p.dir = -1;
      } else if (p.a < 0.1) {
        p.a = 0.1; 
        p.dir = 1;
      }

      // Update positions (unless prefers-reduced-motion is active)
      if (!reduce) {
        p.x += p.vx;
        p.y += p.vy;

        // Loop when going out of top bounds
        if (p.y < -4) {
          p.y = this.height + 4;
          p.x = Math.random() * this.width;
        }

        // Wrap horizontal positioning
        if (p.x < -4) {
          p.x = this.width + 4;
        } else if (p.x > this.width + 4) {
          p.x = -4;
        }
      }

      // Draw particle bubble
      const alpha = p.baseA * p.a;
      this.ctx.beginPath();
      this.ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
      this.ctx.fillStyle = `rgba(${rgb}, ${alpha})`;
      this.ctx.fill();
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
      density: 9500,
      maxParticles: 100,
      colorVar: '--accent-teal',
      fallbackColor: '#22d3ee'
    });
  }

  // Credentials Horizontal Strip background canvas
  const credentialsStrip = document.querySelector('.credentials-strip');
  if (credentialsStrip) {
    new AtomParticles(credentialsStrip, {
      density: 8000,
      maxParticles: 50,
      colorVar: '--accent-terracotta',
      fallbackColor: '#e2876f'
    });
  }
});

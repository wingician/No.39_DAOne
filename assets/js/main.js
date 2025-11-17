// 平滑滚动
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// 导航栏滚动效果
let lastScroll = 0;
const header = document.querySelector('.main-header');

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    
    if (currentScroll <= 0) {
        header.style.boxShadow = '0 4px 20px rgba(124, 58, 237, 0.2)';
    } else {
        header.style.boxShadow = '0 4px 30px rgba(124, 58, 237, 0.4)';
    }
    
    lastScroll = currentScroll;
});

// 卡片进入视口动画
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// 观察所有卡片元素
document.querySelectorAll('.world-card, .theory-card, .timeline-item, .contribute-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(30px)';
    card.style.transition = 'all 0.6s ease-out';
    observer.observe(card);
});

// 魔法粒子效果（可选）
function createMagicParticle() {
    const particle = document.createElement('div');
    particle.className = 'magic-particle';
    particle.style.cssText = `
        position: fixed;
        width: 3px;
        height: 3px;
        background: radial-gradient(circle, var(--secondary-color), transparent);
        border-radius: 50%;
        pointer-events: none;
        z-index: 9999;
        opacity: 0;
        animation: float 3s ease-in-out forwards;
    `;
    
    particle.style.left = Math.random() * window.innerWidth + 'px';
    particle.style.top = window.innerHeight + 'px';
    
    document.body.appendChild(particle);
    
    setTimeout(() => particle.remove(), 3000);
}

// 添加粒子动画CSS
const style = document.createElement('style');
style.textContent = `
    @keyframes float {
        0% {
            transform: translateY(0) translateX(0);
            opacity: 0;
        }
        10% {
            opacity: 1;
        }
        90% {
            opacity: 1;
        }
        100% {
            transform: translateY(-${window.innerHeight}px) translateX(${Math.random() * 200 - 100}px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// 定期创建粒子（降低频率以提升性能）
setInterval(createMagicParticle, 2000);

// 添加鼠标跟随光晕效果
let mouseX = 0, mouseY = 0;
let glowX = 0, glowY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
});

function animateGlow() {
    glowX += (mouseX - glowX) * 0.1;
    glowY += (mouseY - glowY) * 0.1;
    
    document.documentElement.style.setProperty('--mouse-x', glowX + 'px');
    document.documentElement.style.setProperty('--mouse-y', glowY + 'px');
    
    requestAnimationFrame(animateGlow);
}

animateGlow();

// 页面加载完成后的淡入效果
window.addEventListener('load', () => {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease-in';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

console.log('%c欢迎来到翼术师世界！', 'color: #7c3aed; font-size: 20px; font-weight: bold;');
console.log('%c身无彩凤双飞翼，心有灵犀一点通', 'color: #2dd4bf; font-size: 14px; font-style: italic;');

// 搜索功能
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.querySelector('.nav-search input');
    const searchButton = document.querySelector('.nav-search button');
    
    // 搜索按钮点击事件
    searchButton.addEventListener('click', function(e) {
        e.preventDefault();
        performSearch();
    });
    
    // 回车键搜索
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            performSearch();
        }
    });
    
    // 模拟搜索功能
    function performSearch() {
        const query = searchInput.value.trim();
        if (query) {
            alert(`搜索功能：您搜索了 "${query}"`);
            // 这里可以添加实际的搜索逻辑
        }
    }
    
    // 导航菜单交互
    const navLinks = document.querySelectorAll('.nav-menu a');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            // 移除所有激活状态
            navLinks.forEach(l => l.classList.remove('active'));
            // 添加当前激活状态
            this.classList.add('active');
        });
    });
    
    // 登录/注册按钮功能
    const loginBtn = document.querySelector('.login-btn');
    const registerBtn = document.querySelector('.register-btn');
    
    loginBtn.addEventListener('click', function() {
        alert('登录功能将在完整版本中实现');
    });
    
    registerBtn.addEventListener('click', function() {
        alert('注册功能将在完整版本中实现');
    });
    
    // 视频卡片点击事件
    const videoCards = document.querySelectorAll('.video-card');
    videoCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // 防止点击内部链接时触发卡片点击事件
            if (e.target.tagName !== 'A') {
                const title = this.querySelector('h3').textContent;
                alert(`播放视频：${title}`);
            }
        });
    });
    
    // 模拟轮播图功能
    let currentIndex = 0;
    const bannerImages = [
        'https://via.placeholder.com/1200x400/FF6B9D/FFFFFF?text=Bilibili+Banner+1',
        'https://via.placeholder.com/1200x400/7ED321/FFFFFF?text=Bilibili+Banner+2',
        'https://via.placeholder.com/1200x400/F5A623/FFFFFF?text=Bilibili+Banner+3'
    ];
    
    // 自动轮播功能
    function autoSlide() {
        currentIndex = (currentIndex + 1) % bannerImages.length;
        const bannerImg = document.querySelector('.banner img');
        bannerImg.src = bannerImages[currentIndex];
    }
    
    // 每5秒自动切换
    setInterval(autoSlide, 5000);
});

// 页面滚动时的头部效果
window.addEventListener('scroll', function() {
    const header = document.querySelector('.header');
    if (window.scrollY > 50) {
        header.style.boxShadow = '0 4px 12px rgba(0,0,0,0.1)';
        header.style.background = 'rgba(255, 255, 255, 0.95)';
        header.style.backdropFilter = 'blur(10px)';
    } else {
        header.style.boxShadow = '0 2px 4px rgba(0,0,0,0.08)';
        header.style.background = '#fff';
        header.style.backdropFilter = 'none';
    }
});
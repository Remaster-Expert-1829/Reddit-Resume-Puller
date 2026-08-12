document.addEventListener('DOMContentLoaded', () => {
    const grid = document.getElementById('posts-grid');
    const loader = document.getElementById('loader');
    
    // Modal elements
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('zoomed-image');
    const closeBtn = document.querySelector('.modal-close');
    const modalBackdrop = document.querySelector('.modal-backdrop');

    let allPosts = [];

    // Fetch data with cache busting to prevent stale data
    fetch('http://127.0.0.1:8000/data.json?v=' + new Date().getTime(), { cache: 'no-store' })
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.json();
        })
        .then(data => {
            loader.style.display = 'none';
            allPosts = data;
            
            // Display total posts
            const postCountEl = document.getElementById('post-count');
            if (postCountEl) {
                postCountEl.textContent = `Showing ${data.length} Resumes`;
            }

            // Initialize sort event listener
            const sortSelect = document.getElementById('sort-select');
            if (sortSelect) {
                sortSelect.addEventListener('change', (e) => {
                    applySort(e.target.value);
                });
            }

            // Refresh Data Button Logic
            const refreshBtn = document.getElementById('refresh-btn');
            if (refreshBtn) {
                refreshBtn.addEventListener('click', async () => {
                    refreshBtn.disabled = true;
                    refreshBtn.classList.add('loading');
                    refreshBtn.innerHTML = '<span class="refresh-icon">↻</span> Refreshing...';
                    
                    try {
                        // Explicitly call the backend on port 8000, allowing this frontend to run on VS Code Live Server
                        const res = await fetch('http://127.0.0.1:8000/api/refresh', { method: 'POST' });
                        const result = await res.json();
                        
                        if (result.status === 'success') {
                            // Re-fetch data.json
                            const dataRes = await fetch('data.json?v=' + new Date().getTime(), { cache: 'no-store' });
                            const newData = await dataRes.json();
                            
                            allPosts = newData;
                            const postCountEl = document.getElementById('post-count');
                            if (postCountEl) {
                                postCountEl.textContent = `Showing ${newData.length} Resumes`;
                            }
                            
                            const sortSelect = document.getElementById('sort-select');
                            applySort(sortSelect ? sortSelect.value : 'random');
                            
                            refreshBtn.innerHTML = '<span class="refresh-icon">✓</span> Updated!';
                        } else {
                            alert('Error refreshing data: ' + result.message);
                            refreshBtn.innerHTML = '<span class="refresh-icon">↻</span> Refresh Data';
                        }
                    } catch (error) {
                        console.error(error);
                        alert('Server error. Make sure you are running server.py instead of http.server');
                        refreshBtn.innerHTML = '<span class="refresh-icon">↻</span> Refresh Data';
                    }
                    
                    setTimeout(() => {
                        refreshBtn.disabled = false;
                        refreshBtn.classList.remove('loading');
                        refreshBtn.innerHTML = '<span class="refresh-icon">↻</span> Refresh Data';
                    }, 3000);
                });
            }

            applySort('random');
        })
        .catch(error => {
            loader.textContent = 'Failed to load data. Make sure you are running a local server (e.g. Live Server).';
            console.error('Error fetching data:', error);
        });

    function applySort(sortType) {
        let sorted = [...allPosts];
        if (sortType === 'random') {
            for (let i = sorted.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [sorted[i], sorted[j]] = [sorted[j], sorted[i]];
            }
        } else if (sortType === 'most') {
            sorted.sort((a, b) => (b.upvotes || 0) - (a.upvotes || 0));
        } else if (sortType === 'least') {
            sorted.sort((a, b) => (a.upvotes || 0) - (b.upvotes || 0));
        } else if (sortType === 'most_comments') {
            sorted.sort((a, b) => (b.comments || 0) - (a.comments || 0));
        } else if (sortType === 'least_comments') {
            sorted.sort((a, b) => (a.comments || 0) - (b.comments || 0));
        }
        
        grid.innerHTML = '';
        renderPosts(sorted);
    }

    function renderPosts(posts) {
        posts.forEach(post => {
            const card = document.createElement('article');
            card.className = 'post-card';

            // Glow effect tracking
            card.addEventListener('mousemove', e => {
                const rect = card.getBoundingClientRect();
                const x = e.clientX - rect.left;
                const y = e.clientY - rect.top;
                card.style.setProperty('--mouse-x', `${x}px`);
                card.style.setProperty('--mouse-y', `${y}px`);
            });

            const header = document.createElement('div');
            header.className = 'card-header';
            
            const tagsContainer = document.createElement('div');
            tagsContainer.className = 'tags-container';

            const tag = document.createElement('span');
            tag.className = 'subreddit-tag';
            tag.textContent = `r/${post.subreddit}`;
            tagsContainer.appendChild(tag);

            const upvotesTag = document.createElement('span');
            upvotesTag.className = 'upvotes-tag';
            upvotesTag.innerHTML = `&#8679; ${post.upvotes || 0}`;
            tagsContainer.appendChild(upvotesTag);

            const commentsTag = document.createElement('span');
            commentsTag.className = 'comments-tag';
            commentsTag.innerHTML = `&#128172; ${post.comments || 0}`;
            tagsContainer.appendChild(commentsTag);

            header.appendChild(tagsContainer);

            const title = document.createElement('h2');
            title.className = 'post-title';
            const link = document.createElement('a');
            link.href = post.link;
            link.target = '_blank';
            link.rel = 'noopener noreferrer';
            
            // Limit title length if it's too long
            const decodedTitle = decodeHTMLEntities(post.title);
            link.textContent = decodedTitle;
            title.appendChild(link);

            const imagesContainer = document.createElement('div');
            imagesContainer.className = 'images-container';
            
            if (post.images && post.images.length > 0) {
                if (post.images.length > 1) {
                    imagesContainer.classList.add('multi');
                }
                
                // Only show up to 2 images in thumbnail to keep it neat
                const imagesToShow = post.images.slice(0, 2);
                
                imagesToShow.forEach(imgUrl => {
                    const img = document.createElement('img');
                    img.src = imgUrl;
                    img.className = 'thumbnail';
                    img.loading = 'lazy';
                    img.alt = "Resume Image";
                    
                    img.addEventListener('click', () => openModal(imgUrl));
                    
                    imagesContainer.appendChild(img);
                });
            }

            card.appendChild(header);
            card.appendChild(title);
            card.appendChild(imagesContainer);
            grid.appendChild(card);
        });
    }

    function decodeHTMLEntities(text) {
        const textArea = document.createElement('textarea');
        textArea.innerHTML = text;
        return textArea.value;
    }

    // Modal functionality
    let currentScale = 1;
    let translateX = 0;
    let translateY = 0;
    let isPointerDown = false;
    let pointerMoved = false;
    let startX = 0;
    let startY = 0;

    function updateTransform() {
        modalImg.style.transform = `translate(${translateX}px, ${translateY}px) scale(${currentScale})`;
    }

    function resetZoom() {
        currentScale = 1;
        translateX = 0;
        translateY = 0;
        updateTransform();
    }

    function openModal(imgSrc) {
        modalImg.src = imgSrc;
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent scrolling
        resetZoom();
        modalImg.style.cursor = 'zoom-in';
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = '';
        setTimeout(() => { 
            modalImg.src = ''; 
            resetZoom();
        }, 300); // Clear after transition
    }

    closeBtn.addEventListener('click', closeModal);
    modalBackdrop.addEventListener('click', closeModal);

    // Zoom and Pan Logic
    modalImg.addEventListener('wheel', (e) => {
        e.preventDefault();
        const zoomFactor = 1.1;
        if (e.deltaY < 0) {
            currentScale *= zoomFactor;
        } else {
            currentScale /= zoomFactor;
        }
        currentScale = Math.max(0.5, Math.min(currentScale, 10)); // bounds
        updateTransform();
        modalImg.style.cursor = currentScale > 1 ? 'grab' : 'zoom-in';
    });

    modalImg.addEventListener('contextmenu', (e) => {
        e.preventDefault(); // Prevent context menu for right click zoom out
    });

    modalImg.addEventListener('pointerdown', (e) => {
        isPointerDown = true;
        pointerMoved = false;
        startX = e.clientX - translateX;
        startY = e.clientY - translateY;
        if (currentScale > 1) {
            modalImg.style.cursor = 'grabbing';
        }
        e.preventDefault(); // prevents default image dragging behavior
    });

    window.addEventListener('pointermove', (e) => {
        if (!isPointerDown) return;
        
        // Check if actually moved to distinguish from click
        if (Math.abs(e.clientX - startX - translateX) > 2 || Math.abs(e.clientY - startY - translateY) > 2) {
            pointerMoved = true;
            translateX = e.clientX - startX;
            translateY = e.clientY - startY;
            updateTransform();
        }
    });

    window.addEventListener('pointerup', (e) => {
        if (isPointerDown) {
            isPointerDown = false;
            modalImg.style.cursor = currentScale > 1 ? 'grab' : 'zoom-in';
            
            // Handle clicks if not significantly moved
            if (!pointerMoved && e.target === modalImg) {
                if (e.button === 0) { // left click
                    currentScale *= 1.5;
                } else if (e.button === 2) { // right click
                    currentScale /= 1.5;
                }
                currentScale = Math.max(0.5, Math.min(currentScale, 10));
                updateTransform();
                modalImg.style.cursor = currentScale > 1 ? 'grab' : 'zoom-in';
            }
        }
    });
    
    // Close on Escape key
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
});

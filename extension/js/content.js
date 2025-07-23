console.log("Social Compatibility Analyzer: Content script loaded and active.");

// --- Global Variables ---
let hoverTimer = null;
let hoverCard = null;
let currentTargetElement = null;

// The URL for our local backend API
const API_ENDPOINT = "http://127.0.0.1:8000/analyze";

// --- Core Functions ---

/**
 * Creates the hover-card element and appends it to the body.
 * This function is only called once.
 */
function createHoverCard() {
    if (document.getElementById('sca-hover-card-unique')) return;

    hoverCard = document.createElement('div');
    hoverCard.id = 'sca-hover-card-unique';
    hoverCard.className = 'sca-hover-card';
    document.body.appendChild(hoverCard);
    console.log("SCA: Hover card created and added to the page.");
}

/**
 * Updates the content of the hover-card.
 * @param {object} data - The data to display. Can be a loading state or the final report.
 */
function updateHoverCardContent(data) {
    if (!hoverCard) return;

    let content = '';
    if (data.loading) {
        content = '<div class="sca-spinner"></div>';
    } else if (data.error) {
        content = `<div class="sca-header"><span class="sca-title">Error</span></div><div class="sca-body"><p style="color: #f56565;">${data.error}</p></div>`;
    } else {
        content = `
            <div class="sca-header">
                <span class="sca-title">Compatibility</span>
                <span class="sca-score">${data.final_score}%</span>
            </div>
            <div class="sca-body">
                <div class="sca-body-title">Shared Interests</div>
                <ul class="sca-interests-list">
                    ${data.shared_interests.length > 0 ? data.shared_interests.map(interest => `<li class="sca-interest-tag">${interest}</li>`).join('') : '<li>None found</li>'}
                </ul>
            </div>
        `;
    }
    hoverCard.innerHTML = content;
}


/**
 * Shows the hover-card at a specific position.
 * @param {number} top - The top position in pixels.
 * @param {number} left - The left position in pixels.
 */
function showHoverCard(top, left) {
    if (!hoverCard) return;
    hoverCard.style.top = `${top}px`;
    hoverCard.style.left = `${left}px`;
    hoverCard.classList.add('visible');
}

/**
 * Hides the hover-card.
 */
function hideHoverCard() {
    if (!hoverCard) return;
    hoverCard.classList.remove('visible');
}

/**
 * Fetches the compatibility report from the backend API.
 * @param {string} targetUserId - The Twitter handle of the user being hovered over.
 */
async function fetchCompatibilityReport(targetUserId) {
    console.log(`SCA: Fetching report for user: ${targetUserId}`);
    try {
        // For the MVP, user_a_id is a placeholder. In a real app, this would be the logged-in user's ID.
        const requestBody = {
            user_a_id: "loggedInUser", 
            user_b_id: targetUserId
        };

        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(requestBody),
        });

        if (!response.ok) {
            throw new Error(`API returned status ${response.status}`);
        }

        const data = await response.json();
        console.log("SCA: Report received:", data);
        updateHoverCardContent(data);

    } catch (error) {
        console.error("SCA: Error fetching compatibility report:", error);
        updateHoverCardContent({ error: error.message });
    }
}


// --- Event Listeners ---

document.addEventListener('mouseover', (event) => {
    console.log("SCA: Mouse over event detected", event.target);
    
    // Try multiple selectors to find user profile links
    let target = null;
    let userId = null;
    
    // Selector 1: Traditional Twitter user name links
    target = event.target.closest('div[data-testid="User-Name"] a[role="link"]');
    if (target) {
        console.log("SCA: Found target with User-Name selector", target);
        const path = new URL(target.href).pathname;
        userId = path.substring(1);
        console.log("SCA: Extracted userId from User-Name:", userId);
    }
    
    // Selector 2: Profile pictures and avatars
    if (!target) {
        target = event.target.closest('a[role="link"][href^="/"]');
        if (target && target.href.includes('twitter.com') || target.href.includes('x.com')) {
            const path = new URL(target.href).pathname;
            const pathParts = path.split('/').filter(p => p);
            if (pathParts.length === 1 && !['home', 'explore', 'notifications', 'messages', 'bookmarks', 'lists', 'profile', 'settings'].includes(pathParts[0])) {
                userId = pathParts[0];
                console.log("SCA: Found target with general selector, userId:", userId);
            }
        }
    }
    
    // Selector 3: Any link that looks like a user profile
    if (!target) {
        const allLinks = event.target.closest('a[href*="/"]');
        if (allLinks) {
            const href = allLinks.href;
            if ((href.includes('twitter.com') || href.includes('x.com')) && !href.includes('/status/') && !href.includes('/search')) {
                try {
                    const path = new URL(href).pathname;
                    const pathParts = path.split('/').filter(p => p);
                    if (pathParts.length === 1 && pathParts[0].length > 0) {
                        target = allLinks;
                        userId = pathParts[0];
                        console.log("SCA: Found target with fallback selector, userId:", userId);
                    }
                } catch (e) {
                    console.log("SCA: Error parsing URL:", e);
                }
            }
        }
    }

    if (target && userId && userId.length > 0) {
        // Don't re-trigger if we are already hovering over the same element
        if (target === currentTargetElement) return;
        
        currentTargetElement = target;
        console.log(`SCA: Hover detected on user: @${userId}`);

        // Clear any existing timer
        clearTimeout(hoverTimer);

        // Set a timer to show the card after a short delay
        hoverTimer = setTimeout(() => {
            console.log("SCA: Hover timer expired. Showing card.");
            const rect = target.getBoundingClientRect();
            showHoverCard(rect.bottom + window.scrollY + 5, rect.left + window.scrollX);
            updateHoverCardContent({ loading: true });
            fetchCompatibilityReport(userId);
        }, 700); // 700ms delay
    } else {
        console.log("SCA: No valid user profile link found");
    }
});

document.addEventListener('mouseout', (event) => {
    // If the mouse leaves the target element, clear the timer and hide the card
    if (event.target === currentTargetElement) {
        console.log("SCA: Mouse out detected, hiding card");
        clearTimeout(hoverTimer);
        hideHoverCard();
        currentTargetElement = null;
    }
});

// Add a click listener for testing
document.addEventListener('click', (event) => {
    console.log("SCA: Click detected for testing", event.target);
    
    // Test the same logic as hover
    let target = event.target.closest('div[data-testid="User-Name"] a[role="link"]');
    if (!target) {
        target = event.target.closest('a[role="link"][href^="/"]');
    }
    
    if (target && (target.href.includes('twitter.com') || target.href.includes('x.com'))) {
        const path = new URL(target.href).pathname;
        const userId = path.substring(1).split('/')[0];
        if (userId) {
            console.log(`SCA: CLICK TEST - Would show card for user: @${userId}`);
            // Show the card immediately for testing
            const rect = target.getBoundingClientRect();
            showHoverCard(rect.bottom + window.scrollY + 5, rect.left + window.scrollX);
            updateHoverCardContent({ loading: true });
            fetchCompatibilityReport(userId);
        }
    }
});

// --- Initialization ---
// Ensure the card is created once the page is fully loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', createHoverCard);
} else {
    createHoverCard();
}

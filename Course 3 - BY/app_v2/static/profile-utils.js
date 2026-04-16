/**
 * BeatRec Profile Utilities
 * Shared functions for profile name management across all pages
 */

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

/**
 * Get profile name from URL parameter or localStorage
 * Priority: 1) URL param, 2) localStorage, 3) default 'Profile-1'
 * @returns {string} Profile name
 */
function getProfileName() {
  const urlParams = new URLSearchParams(window.location.search);
  const profileFromUrl = urlParams.get('profile');
  if (profileFromUrl) {
    return decodeURIComponent(profileFromUrl);
  }
  const profile = localStorage.getItem('beatrec_profile');
  if (profile) {
    const data = JSON.parse(profile);
    return data.name || 'Profile-1';
  }
  return 'Profile-1';
}

/**
 * Display profile name in page subtitle
 * @param {string} stepInfo - Step information (e.g., 'Step 2 of 5')
 * @param {string} subtitleElementId - ID of subtitle element (default: 'page-subtitle')
 */
function displayProfileName(stepInfo, subtitleElementId = 'page-subtitle') {
  const name = getProfileName();
  const subtitle = document.getElementById(subtitleElementId);
  if (subtitle) {
    subtitle.innerHTML = `<span style="opacity:0.6">${escapeHtml(name)}</span> · ${stepInfo}`;
  }
}

/**
 * Save profile data to localStorage and profiles array
 * @param {Object} profileData - Profile data to save (ratings, preferences, genres, etc.)
 */
function saveProfileData(profileData) {
  const name = getProfileName();
  
  // Merge with existing profile data
  const existingProfile = localStorage.getItem('beatrec_profile');
  const mergedProfile = existingProfile ? { ...JSON.parse(existingProfile), ...profileData } : { name, ...profileData };
  
  // Save to localStorage
  localStorage.setItem('beatrec_profile', JSON.stringify(mergedProfile));
  
  // Also save to profiles array
  const profiles = JSON.parse(localStorage.getItem('beatrec_profiles') || '[]');
  const profileIndex = profiles.findIndex(p => p.name === name);
  if (profileIndex >= 0) {
    profiles[profileIndex] = { ...profiles[profileIndex], ...profileData };
    localStorage.setItem('beatrec_profiles', JSON.stringify(profiles));
  }
}

/**
 * Navigate to another page with profile name in URL
 * @param {string} path - Target path (e.g., '/rate-songs')
 */
function navigateWithProfile(path) {
  const name = getProfileName();
  window.location.href = `${path}?profile=${encodeURIComponent(name)}`;
}

/**
 * Get current step info from URL or default
 * @returns {Object} Step information { current, total }
 */
function getCurrentStep() {
  const path = window.location.pathname;
  if (path.includes('/welcome') || path === '/') return { current: 1, total: 5 };
  if (path.includes('/select-genres')) return { current: 2, total: 5 };
  if (path.includes('/rate-songs')) return { current: 3, total: 5 };
  if (path.includes('/preferences')) return { current: 4, total: 5 };
  if (path.includes('/recommendations')) return { current: 5, total: 5 };
  return { current: 1, total: 5 };
}

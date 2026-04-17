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
 * Get the URL subpath prefix (e.g., '/beatrec' or '')
 * Uses window.BEATREC_SUBPATH if available, otherwise detects from current URL
 * @returns {string} Subpath prefix (e.g., '/beatrec' or '')
 */
function getSubpath() {
  // Check if subpath is defined in window object (injected by Flask)
  if (window.BEATREC_SUBPATH !== undefined) {
    return window.BEATREC_SUBPATH ? '/' + window.BEATREC_SUBPATH : '';
  }
  
  // Fallback: detect from current URL pathname
  // If we're at /beatrec/select-genres, extract 'beatrec'
  const pathParts = window.location.pathname.split('/').filter(p => p);
  if (pathParts.length > 1 && !pathParts[0].startsWith('select') && !pathParts[0].startsWith('rate') && !pathParts[0].startsWith('preferences') && !pathParts[0].startsWith('recommendations') && !pathParts[0].startsWith('feedback') && !pathParts[0].startsWith('welcome') && !pathParts[0].startsWith('admin')) {
    return '/' + pathParts[0];
  }
  return '';
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

  // DEBUG: Log what we're saving
  console.log('[BeatRec Debug] === saveProfileData() called ===');
  console.log('[BeatRec Debug] Profile name:', name);
  console.log('[BeatRec Debug] Data to save:', JSON.stringify(profileData, null, 2));

  // Merge with existing profile data
  const existingProfile = localStorage.getItem('beatrec_profile');
  const mergedProfile = existingProfile ? { ...JSON.parse(existingProfile), ...profileData } : { name, ...profileData };

  // Save to localStorage
  localStorage.setItem('beatrec_profile', JSON.stringify(mergedProfile));
  console.log('[BeatRec Debug] Saved to beatrec_profile:', localStorage.getItem('beatrec_profile'));

  // Also save to profiles array
  const profiles = JSON.parse(localStorage.getItem('beatrec_profiles') || '[]');
  const profileIndex = profiles.findIndex(p => p.name === name);
  if (profileIndex >= 0) {
    profiles[profileIndex] = { ...profiles[profileIndex], ...profileData };
    localStorage.setItem('beatrec_profiles', JSON.stringify(profiles));
    console.log('[BeatRec Debug] Updated profile in profiles array');
  } else {
    console.log('[BeatRec Debug] Profile not found in profiles array, skipping array update');
  }
  console.log('[BeatRec Debug] ================================');
}

/**
 * Navigate to another page with profile name in URL
 * @param {string} path - Target path (e.g., '/rate-songs')
 */
function navigateWithProfile(path) {
  const subpath = getSubpath();
  const name = getProfileName();
  window.location.href = `${subpath}${path}?profile=${encodeURIComponent(name)}`;
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

/**
 * Liked Songs Management
 * Save and retrieve liked songs from localStorage
 */

/**
 * Get liked songs from localStorage
 * @returns {Array} Array of track_ids that user has liked
 */
function getLikedSongs() {
  const liked = localStorage.getItem('beatrec_liked_songs');
  return liked ? JSON.parse(liked) : [];
}

/**
 * Check if a song is liked
 * @param {string} trackId - Track ID to check
 * @returns {boolean} True if song is liked
 */
function isSongLiked(trackId) {
  const likedSongs = getLikedSongs();
  return likedSongs.includes(trackId);
}

/**
 * Toggle like status for a song
 * @param {string} trackId - Track ID to toggle
 * @param {Object} songData - Song data to store (optional)
 * @returns {Object} { liked: boolean, count: number } - New status and total count
 */
function toggleLikeSong(trackId, songData = null) {
  const likedSongs = getLikedSongs();
  const index = likedSongs.indexOf(trackId);
  
  if (index > -1) {
    // Unlike: remove from list
    likedSongs.splice(index, 1);
  } else {
    // Like: add to list (max 50)
    if (likedSongs.length >= 50) {
      return { liked: true, count: 50, limitReached: true };
    }
    likedSongs.push(trackId);
  }
  
  localStorage.setItem('beatrec_liked_songs', JSON.stringify(likedSongs));
  
  // Also sync with beatrec_profile
  const profile = JSON.parse(localStorage.getItem('beatrec_profile') || '{}');
  profile.likedSongs = likedSongs;
  localStorage.setItem('beatrec_profile', JSON.stringify(profile));
  
  return { 
    liked: index === -1, 
    count: likedSongs.length, 
    limitReached: likedSongs.length >= 50 
  };
}

/**
 * Get count of liked songs
 * @returns {number} Number of liked songs
 */
function getLikedSongsCount() {
  return getLikedSongs().length;
}

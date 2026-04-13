const DEMO_PROFILES = {
  loris: {
    name: 'Loris',
    genres: ['Rock', 'Electronic'],
    popularity: 3,
    valence: 0.45,
    energy: 0.82,
    decade: '2000s',
  },
  catherine: {
    name: 'Catherine',
    genres: ['Pop', 'R&B / Soul'],
    popularity: 9,
    valence: 0.82,
    energy: 0.88,
    decade: '2020s',
  },
};

const GENRES = [
  { name: 'Rock', icon: '🎸', color: 'rgba(255,80,80,0.15)' },
  { name: 'Hip-Hop', icon: '🎤', color: 'rgba(120,80,255,0.15)' },
  { name: 'Electronic', icon: '🎹', color: 'rgba(29,185,84,0.15)' },
  { name: 'Jazz', icon: '🎷', color: 'rgba(255,180,30,0.15)' },
  { name: 'Pop', icon: '💃', color: 'rgba(255,100,180,0.15)' },
  { name: 'Classical', icon: '🎻', color: 'rgba(80,180,255,0.15)' },
  { name: 'Country', icon: '🤠', color: 'rgba(255,140,40,0.15)' },
  { name: 'R&B / Soul', icon: '🎶', color: 'rgba(200,80,255,0.15)' },
];

const DECADES = ['1970s', '1980s', '1990s', '2000s', '2010s', '2020s'];

const SAMPLE_RATINGS = [
  { title: 'Midnight Run', artist: 'Neon Atlas' },
  { title: 'Ocean Drive', artist: 'Velvet Echo' },
  { title: 'Daydream Pulse', artist: 'Luna City' },
  { title: 'City Lights', artist: 'Nova Bloom' },
  { title: 'Afterglow', artist: 'Stereo Drift' },
];

let state = {
  name: '',
  selectedGenres1: [],
  selectedGenres2: [],
  selectedGenres3: [],
  ratings: [0, 0, 0, 0, 0],
  valence: 0.5,
  energy: 0.5,
  popularity: 5,
  decade: '2020s',
  recommendations: [],
  thumbs: {},
  ratingTracks: [],
  currentTrackIndex: -1,
  isPlaying: false,
};

const xypad = document.getElementById('xypad');
const xypadWrap = document.getElementById('xypad-wrap');
let xypadDragging = false;

function showPage(pageId) {
  document.querySelectorAll('.page').forEach(page => page.classList.remove('active'));
  const page = document.getElementById(pageId);
  if (page) page.classList.add('active');
}

function renderGenreGrid(container, selectedGenres) {
  const grid = document.getElementById(container);
  if (!grid) return;
  grid.innerHTML = '';
  GENRES.forEach(genre => {
    const card = document.createElement('button');
    card.type = 'button';
    card.className = 'genre-card' + (selectedGenres.includes(genre.name) ? ' active' : '');
    card.innerHTML = `<div class="genre-dot" style="background:${genre.color}">${genre.icon}</div><span class="genre-name">${genre.name}</span>`;
    card.onclick = () => toggleGenre(genre.name, container);
    grid.appendChild(card);
  });
}

function toggleGenre(genre, container) {
  let listName = 'selectedGenres1';
  if (container === 'genre-grid-page3') listName = 'selectedGenres3';
  const list = state[listName];
  const idx = list.indexOf(genre);
  if (idx === -1) list.push(genre);
  else list.splice(idx, 1);
  renderGenreGrid(container, state[listName]);
}

function renderRatingCards() {
  const container = document.getElementById('rating-list');
  if (!container) return;
  container.innerHTML = '';
  const tracks = state.ratingTracks.length ? state.ratingTracks : SAMPLE_RATINGS;
  tracks.forEach((song, index) => {
    const card = document.createElement('div');
    card.className = 'rating-card';
    card.innerHTML = `
      <div class="rating-title">${song.title} · ${song.artist}</div>
      <div class="rating-actions">
        ${song.preview_url ? `<button type="button" class="preview-btn" onclick="playRatingPreview('${song.preview_url.replace(/'/g, "\\'")}')">▶️ Preview</button>` : ''}
        <div class="rating-stars" id="rating-stars-${index}"></div>
      </div>
    `;
    container.appendChild(card);
    const stars = card.querySelector('.rating-stars');
    for (let i = 1; i <= 5; i++) {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = 'star-btn' + (state.ratings[index] >= i ? ' active' : '');
      button.innerText = '★';
      button.onclick = () => setRating(index, i);
      stars.appendChild(button);
    }
  });
}

function playRatingPreview(previewUrl) {
  const audio = document.getElementById('audio-player');
  if (!audio) return;
  if (audio.src !== previewUrl) {
    audio.src = previewUrl;
    audio.load();
  }
  audio.play().catch(() => {});
  state.isPlaying = true;
  state.currentTrackIndex = -1;
  updateUI();
}

function loadRatingTracks() {
  const genresParam = state.selectedGenres1.length > 0 ? state.selectedGenres1.join(',') : '';
  const url = genresParam ? `/api/sample-rating-songs?genres=${genresParam}` : '/api/sample-rating-songs';
  
  fetch(url)
    .then(response => response.json())
    .then(data => {
      state.ratingTracks = (data.tracks || []).slice(0, 5);
      if (!state.ratingTracks.length) {
        state.ratingTracks = SAMPLE_RATINGS;
      }
      renderRatingCards();
    })
    .catch(() => {
      state.ratingTracks = SAMPLE_RATINGS;
      renderRatingCards();
    });
}

function setRating(trackIndex, value) {
  state.ratings[trackIndex] = value;
  renderRatingCards();
}

function loadDemoProfile(key) {
  const profile = DEMO_PROFILES[key];
  if (!profile) return;
  state.name = profile.name;
  state.selectedGenres1 = [...profile.genres];
  state.selectedGenres2 = [...profile.genres];
  state.popularity = profile.popularity;
  state.valence = profile.valence;
  state.energy = profile.energy;
  state.decade = profile.decade;
  document.getElementById('inp-name').value = profile.name;
  document.getElementById('sl-pop').value = profile.popularity;
  updatePop(profile.popularity);
  updateMoodLabels();
  renderGenreGrid('genre-grid-page1', state.selectedGenres1);
  renderGenreGrid('genre-grid-page2', state.selectedGenres2);
  renderDecadeChips();
  closeDemoPopup();
}

function openDemoPopup() {
  const modal = document.getElementById('demo-modal');
  if (modal) modal.classList.add('show');
}

function closeDemoPopup() {
  const modal = document.getElementById('demo-modal');
  if (modal) modal.classList.remove('show');
}

function triggerProfileImport() {
  document.getElementById('profile-file-input').click();
}

function importProfileFile(event) {
  const file = event.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const parsed = JSON.parse(reader.result);
      state.name = parsed.name || state.name;
      state.selectedGenres1 = parsed.genres || state.selectedGenres1;
      state.selectedGenres2 = parsed.genres || state.selectedGenres2;
      state.popularity = parsed.popularity || state.popularity;
      state.valence = parsed.valence ?? state.valence;
      state.energy = parsed.energy ?? state.energy;
      state.decade = parsed.decade || state.decade;
      document.getElementById('inp-name').value = state.name;
      document.getElementById('sl-pop').value = state.popularity;
      updatePop(state.popularity);
      updateMoodLabels();
      renderGenreGrid('genre-grid-page1', state.selectedGenres1);
      renderGenreGrid('genre-grid-page2', state.selectedGenres2);
      renderDecadeChips();
    } catch (error) {
      alert('Unable to import profile. Make sure the file is valid JSON.');
    }
  };
  reader.readAsText(file);
  event.target.value = '';
}

function handlePage1Continue() {
  state.name = document.getElementById('inp-name').value.trim() || 'Listener';
  if (!state.selectedGenres1.length) {
    alert('Please select at least one genre before continuing.');
    return;
  }
  state.selectedGenres2 = state.selectedGenres1.slice();
  loadRatingTracks();
  showPage('page-rating');
}

function handlePage2Continue() {
  state.selectedGenres3 = state.selectedGenres1.slice();
  renderGenreGrid('genre-grid-page3', state.selectedGenres3);
  renderDecadeChips();
  showPage('page-finetune');
}

function handlePage3Continue() {
  const genres = state.selectedGenres3.length ? state.selectedGenres3 : state.selectedGenres1;
  const payload = {
    name: state.name,
    mood: getMoodLabel(),
    valence: state.valence,
    energy: state.energy,
    popularity: state.popularity,
    selected_genres: genres,
    decade: state.decade,
    ratings: state.ratings,
  };
  fetchRecommendations(payload);
}

function fetchRecommendations(payload) {
  const button = document.querySelector('#page-inputs .btn-primary');
  if (button) button.disabled = true;
  fetch('/api/recommend', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  })
    .then(response => {
      if (!response.ok) throw new Error('Server error');
      return response.json();
    })
    .then(data => {
      state.recommendations = data.recommendations || [];
      state.thumbs = {};
      renderResults(data);
      showPage('page-results');
    })
    .catch(error => {
      console.error(error);
      alert('Unable to fetch recommendations. Please try again.');
    })
    .finally(() => { if (button) button.disabled = false; });
}

function renderDecadeChips() {
  const container = document.getElementById('decade-row');
  container.innerHTML = '';
  DECADES.forEach(decade => {
    const chip = document.createElement('button');
    chip.type = 'button';
    chip.className = 'chip' + (state.decade === decade ? ' active' : '');
    chip.textContent = decade;
    chip.onclick = () => {
      state.decade = decade;
      renderDecadeChips();
    };
    container.appendChild(chip);
  });
}

function updatePop(value) {
  state.popularity = Number(value);
  const labels = {
    1:'Deep Underground', 2:'Underground', 3:'Indie', 4:'Niche', 5:'Mid-Stream',
    6:'Rising', 7:'Popular', 8:'Trending', 9:'Mainstream', 10:'Chart-Topper'
  };
  document.getElementById('pop-label').textContent = labels[state.popularity] || 'Mid-Stream';
  const pct = ((state.popularity - 1) / 9) * 100;
  document.getElementById('sl-pop').style.background =
    `linear-gradient(to right, rgba(29,185,84,0.85) ${pct}%, rgba(255,255,255,0.12) ${pct}%)`;
}

function getMoodLabel() {
  if (state.valence >= 0.7 && state.energy >= 0.7) return 'Euphoric';
  if (state.valence >= 0.7 && state.energy < 0.7) return 'Relaxed';
  if (state.valence < 0.4 && state.energy >= 0.7) return 'Angry';
  if (state.valence < 0.4 && state.energy < 0.4) return 'Sad';
  return 'Neutral';
}

function updateMoodLabels() {
  document.getElementById('mood-name').textContent = getMoodLabel();
  document.getElementById('mood-desc').textContent = `Valence ${Math.round(state.valence * 100)}% · Energy ${Math.round(state.energy * 100)}%`;
}

function drawXYPad() {
  if (!xypad) return;
  const ctx = xypad.getContext('2d');
  const size = xypad.width;
  const PAD = size;
  ctx.clearRect(0, 0, PAD, PAD);

  const zoneColors = [
    ['#c0392b','#e67e22','#f39c12'],
    ['#8e44ad','#7f8c8d','#27ae60'],
    ['#2c3e50','#2980b9','#1abc9c'],
  ];
  const W = PAD / 3;
  const H = PAD / 3;
  for (let r = 0; r < 3; r++) {
    for (let c = 0; c < 3; c++) {
      ctx.fillStyle = zoneColors[r][c];
      ctx.globalAlpha = 0.72;
      ctx.fillRect(c * W, r * H, W, H);
    }
  }
  ctx.globalAlpha = 1;

  const gH = ctx.createLinearGradient(0, 0, PAD, 0);
  gH.addColorStop(0, 'rgba(0,0,0,0.18)');
  gH.addColorStop(0.5, 'rgba(0,0,0,0)');
  gH.addColorStop(1, 'rgba(255,255,255,0.08)');
  ctx.fillStyle = gH;
  ctx.fillRect(0, 0, PAD, PAD);

  ctx.strokeStyle = 'rgba(255,255,255,0.22)';
  ctx.lineWidth = 1;
  [1, 2].forEach(i => {
    ctx.beginPath(); ctx.moveTo(i * W, 0); ctx.lineTo(i * W, PAD); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(0, i * H); ctx.lineTo(PAD, i * H); ctx.stroke();
  });

  const dotX = state.valence * PAD;
  const dotY = (1 - state.energy) * PAD;
  ctx.strokeStyle = 'rgba(255,255,255,0.28)';
  ctx.setLineDash([3, 4]);
  ctx.beginPath(); ctx.moveTo(dotX, 0); ctx.lineTo(dotX, PAD); ctx.stroke();
  ctx.beginPath(); ctx.moveTo(0, dotY); ctx.lineTo(PAD, dotY); ctx.stroke();
  ctx.setLineDash([]);

  const glow = ctx.createRadialGradient(dotX, dotY, 0, dotX, dotY, 22);
  glow.addColorStop(0, 'rgba(255,255,255,0.45)');
  glow.addColorStop(1, 'rgba(255,255,255,0)');
  ctx.beginPath(); ctx.arc(dotX, dotY, 22, 0, Math.PI * 2); ctx.fillStyle = glow; ctx.fill();

  ctx.beginPath(); ctx.arc(dotX + 2, dotY + 2, 13, 0, Math.PI * 2);
  ctx.fillStyle = 'rgba(0,0,0,0.22)'; ctx.fill();

  ctx.beginPath(); ctx.arc(dotX, dotY, 13, 0, Math.PI * 2);
  ctx.fillStyle = '#fff'; ctx.shadowColor = 'rgba(0,0,0,0.25)'; ctx.shadowBlur = 5;
  ctx.fill(); ctx.shadowBlur = 0;

  ctx.beginPath(); ctx.arc(dotX, dotY, 7, 0, Math.PI * 2);
  ctx.fillStyle = '#1DB954'; ctx.fill();
}

function updateMoodFromPointer(clientX, clientY) {
  const rect = xypad.getBoundingClientRect();
  const x = Math.max(0, Math.min(rect.width, clientX - rect.left));
  const y = Math.max(0, Math.min(rect.height, clientY - rect.top));
  state.valence = x / rect.width;
  state.energy = 1 - y / rect.height;
  updateMoodLabels();
  drawXYPad();
}

xypadWrap.addEventListener('mousedown', (event) => {
  xypadDragging = true;
  updateMoodFromPointer(event.clientX, event.clientY);
});

document.addEventListener('mousemove', (event) => {
  if (!xypadDragging) return;
  updateMoodFromPointer(event.clientX, event.clientY);
});

document.addEventListener('mouseup', () => { xypadDragging = false; });

xypadWrap.addEventListener('touchstart', (event) => {
  event.preventDefault();
  xypadDragging = true;
  updateMoodFromPointer(event.touches[0].clientX, event.touches[0].clientY);
}, { passive: false });

document.addEventListener('touchmove', (event) => {
  if (!xypadDragging) return;
  updateMoodFromPointer(event.touches[0].clientX, event.touches[0].clientY);
});

document.addEventListener('touchend', () => { xypadDragging = false; });

function renderResults(data) {
  document.getElementById('rec-username').textContent = `Hey, ${data.name || state.name}!`;
  document.getElementById('rec-tag-mood').textContent = data.mood || getMoodLabel();
  document.getElementById('rec-tag-genre').textContent = (state.selectedGenres2.length ? state.selectedGenres2 : state.selectedGenres1).slice(0, 2).join(' · ') || 'Mixed';
  document.getElementById('rec-tag-ve').textContent = `V:${Math.round(state.valence * 100)} E:${Math.round(state.energy * 100)}`;
  document.getElementById('results-count').textContent = `${data.recommendations?.length || 0} recommendations`;

  const grid = document.getElementById('results-grid');
  grid.innerHTML = '';
  (data.recommendations || []).forEach((track, index) => {
    const card = document.createElement('div');
    card.className = 'result-card' + (state.currentTrackIndex === index ? ' playing' : '');
    card.onclick = () => playTrack(index);
    card.innerHTML = `
      <div class="result-top">
        <div class="result-meta">
          <div class="result-title">${track.title}</div>
          <div class="result-artist">${track.artist}</div>
        </div>
        <div class="result-badge">${track.genre || 'Recommended'}</div>
      </div>
      <div class="result-detail">
        <span>${track.duration || '0:30'}</span>
        <span>${track.match || ''}</span>
      </div>
      <div class="result-actions">
        <button type="button" class="result-action-btn like" id="thumb-like-${index}" onclick="event.stopPropagation(); setThumb(index, 'like', track.preview_url)">👍 Like</button>
        <button type="button" class="result-action-btn dislike" id="thumb-dislike-${index}" onclick="event.stopPropagation(); setThumb(index, 'dislike', track.preview_url)">👎 Dislike</button>
      </div>
    `;
    grid.appendChild(card);
  });
  
  updateAudioControls();
}

// Audio control functions
function playTrack(index) {
  if (!state.recommendations || !state.recommendations[index]) return;
  
  const track = state.recommendations[index];
  const audio = document.getElementById('audio-player');
  
  if (state.currentTrackIndex === index && state.isPlaying) {
    // Pause current track
    audio.pause();
    state.isPlaying = false;
  } else {
    // Play new track
    if (track.preview_url) {
      audio.src = track.preview_url;
      audio.load();
      audio.play().catch(err => console.log('Audio play failed:', err));
      state.currentTrackIndex = index;
      state.isPlaying = true;
    }
  }
  
  updateUI();
}

function updateAudioControls() {
  const audio = document.getElementById('audio-player');
  const controls = document.getElementById('audio-controls');
  const info = document.getElementById('audio-info');
  const progressTrack = document.getElementById('audio-progress-track');
  const progressFill = document.getElementById('audio-progress-fill');
  const currentTimeLabel = document.getElementById('audio-current');
  const totalTimeLabel = document.getElementById('audio-total');
  const playBtn = document.getElementById('audio-play');

  const hasAudioSource = audio && audio.src;
  if ((state.currentTrackIndex >= 0 && state.recommendations && state.recommendations[state.currentTrackIndex]) || hasAudioSource) {
    const track = state.currentTrackIndex >= 0 && state.recommendations ? state.recommendations[state.currentTrackIndex] : null;
    info.textContent = track ? `${track.title} - ${track.artist}` : 'Preview track';
    controls.style.display = 'block';
    playBtn.textContent = state.isPlaying ? '⏸️' : '▶️';

    audio.onloadedmetadata = () => {
      totalTimeLabel.textContent = formatTime(audio.duration || 30);
      updateAudioProgress();
    };
    audio.ontimeupdate = () => {
      updateAudioProgress();
    };
    audio.onended = () => {
      state.isPlaying = false;
      updateUI();
    };
    audio.onerror = () => {
      console.log('Audio error for track:', track ? track.title : 'preview');
      state.isPlaying = false;
      updateUI();
    };

    if (progressTrack) {
      progressTrack.onclick = seekAudio;
    }
  } else {
    controls.style.display = 'none';
  }
}

function togglePlay() {
  const audio = document.getElementById('audio-player');
  if (state.isPlaying) {
    audio.pause();
    state.isPlaying = false;
  } else {
    audio.play().catch(err => console.log('Audio play failed:', err));
    state.isPlaying = true;
  }
  updateUI();
}

function nextTrack() {
  if (!state.recommendations || !state.recommendations.length) return;
  const nextIndex = (state.currentTrackIndex + 1) % state.recommendations.length;
  playTrack(nextIndex);
}

function prevTrack() {
  if (!state.recommendations || !state.recommendations.length) return;
  const prevIndex = state.currentTrackIndex > 0 ? state.currentTrackIndex - 1 : state.recommendations.length - 1;
  playTrack(prevIndex);
}

function seekAudio(event) {
  const audio = document.getElementById('audio-player');
  const progressTrack = document.getElementById('audio-progress-track');
  if (!audio || !progressTrack || !audio.duration) return;
  const rect = progressTrack.getBoundingClientRect();
  const percent = Math.max(0, Math.min(1, (event.clientX - rect.left) / rect.width));
  audio.currentTime = percent * audio.duration;
  updateAudioProgress();
}

function updateAudioProgress() {
  const audio = document.getElementById('audio-player');
  const progressFill = document.getElementById('audio-progress-fill');
  const currentTimeLabel = document.getElementById('audio-current');
  if (!audio || !progressFill || !currentTimeLabel) return;
  const percent = audio.duration ? (audio.currentTime / audio.duration) * 100 : 0;
  progressFill.style.width = `${percent}%`;
  currentTimeLabel.textContent = formatTime(audio.currentTime);
}

function formatTime(seconds) {
  if (!seconds || Number.isNaN(seconds)) return '0:00';
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60).toString().padStart(2, '0');
  return `${m}:${s}`;
}

function updateUI() {
  // Update playing state classes
  document.querySelectorAll('.result-card').forEach((card, index) => {
    card.classList.toggle('playing', index === state.currentTrackIndex && state.isPlaying);
  });
  
  // Update audio controls
  updateAudioControls();
}

function setThumb(index, type, previewUrl) {
  if (state.thumbs[index] === type) {
    delete state.thumbs[index];
  } else {
    state.thumbs[index] = type;
  }
  document.querySelectorAll(`#results-grid .result-action-btn`).forEach(btn => btn.classList.remove('active'));
  const selectedButton = document.getElementById(`thumb-${type}-${index}`);
  if (selectedButton) selectedButton.classList.add('active');
}

function playPreview(url) {
  const player = document.getElementById('preview-audio');
  if (!player) return;
  if (player.src !== url) {
    player.src = url;
  }
  player.play().catch(() => {});
}

function init() {
  renderGenreGrid('genre-grid-page1', state.selectedGenres1);
  renderGenreGrid('genre-grid-page2', state.selectedGenres2);
  renderDecadeChips();
  updatePop(state.popularity);
  updateMoodLabels();
  drawXYPad();
  document.getElementById('audio-prev')?.addEventListener('click', prevTrack);
  document.getElementById('audio-play')?.addEventListener('click', togglePlay);
  document.getElementById('audio-next')?.addEventListener('click', nextTrack);
}

document.addEventListener('DOMContentLoaded', init);

let currentAlgorithm = 'hybrid';
let currentGame = 'lotto';
let chartInstance = null;

function selectAlgorithm(algo) {
    currentAlgorithm = algo;
    
    // Update UI
    document.querySelectorAll('.btn').forEach(btn => btn.classList.remove('active'));
    document.getElementById(`btn-${algo}`).classList.add('active');
}

function changeGame() {
    currentGame = document.getElementById('game-select').value;
    // Clear current results
    document.getElementById('main-balls').innerHTML = '';
    document.getElementById('special-balls').innerHTML = '';
    document.getElementById('explanation').textContent = '';
    
    // Reload stats
    loadStats();
    
    // Show note for Lotto and Keno
    const noteBox = document.getElementById('game-note');
    if (currentGame === 'lotto') {
        noteBox.textContent = "ℹ️ Note: Lotto statistics are based on data from October 2011 onwards (start of 45-number game) to ensure accuracy.";
        noteBox.style.display = 'block';
    } else if (currentGame === 'keno') {
        noteBox.textContent = "ℹ️ Note: Keno statistics are based on data from 2008 onwards (start of 70-number game).";
        noteBox.style.display = 'block';
    } else {
        noteBox.style.display = 'none';
    }
}

async function generatePrediction() {
    const mainContainer = document.getElementById('main-balls');
    const specialContainer = document.getElementById('special-balls');
    const explanationBox = document.getElementById('explanation');
    
    mainContainer.innerHTML = '<div class="ball placeholder">...</div>';
    specialContainer.innerHTML = '';
    explanationBox.textContent = 'Calculating...';
    
    try {
        const response = await fetch(`/api/predict/${currentGame}/${currentAlgorithm}`);
        if (!response.ok) throw new Error('Prediction failed');
        
        const data = await response.json();
        console.log('Prediction Data:', data); // DEBUG
        
        displayBalls(data.numbers, data.special_numbers, data.special_label, data.constellation);
        explanationBox.textContent = data.explanation;
        
    } catch (error) {
        console.error('Error:', error);
        mainContainer.innerHTML = '<div style="color: red">Error generating prediction</div>';
        explanationBox.textContent = '';
    }
}

function displayBalls(numbers, specialNumbers, specialLabel, constellation) {
    const mainContainer = document.getElementById('main-balls');
    const specialContainer = document.getElementById('special-balls');
    
    mainContainer.innerHTML = '';
    specialContainer.innerHTML = '';
    
    // Main numbers
    numbers.forEach((num, index) => {
        const ball = document.createElement('div');
        ball.className = 'ball';
        ball.textContent = num;
        ball.style.animationDelay = `${index * 0.1}s`;
        mainContainer.appendChild(ball);
    });
    
    // Special numbers or Constellation
    if ((specialNumbers && specialNumbers.length > 0) || constellation) {
        const targetContainer = document.getElementById('special-balls');
        targetContainer.innerHTML = ''; 
        
        const label = document.createElement('div');
        label.className = 'special-label';
        label.textContent = specialLabel || 'Special';
        targetContainer.appendChild(label);
        
        const ballsWrapper = document.createElement('div');
        ballsWrapper.className = 'ball-group'; 
        
        if (specialNumbers && specialNumbers.length > 0) {
            specialNumbers.forEach((num, index) => {
                const ball = document.createElement('div');
                ball.className = 'ball special';
                if (specialLabel === 'Bonus') {
                    ball.classList.add('bonus-ball');
                }
                ball.textContent = num;
                ball.style.animationDelay = `${(numbers.length + index) * 0.1}s`;
                ballsWrapper.appendChild(ball);
            });
        }
        
        if (constellation) {
            const iconDiv = document.createElement('div');
            iconDiv.className = 'constellation-icon';
            iconDiv.textContent = getConstellationIcon(constellation);
            iconDiv.title = constellation; // Tooltip
            ballsWrapper.appendChild(iconDiv);
        }
        
        targetContainer.appendChild(ballsWrapper);
    }
}

function getConstellationIcon(name) {
    const icons = {
        'Ram': '♈', 'Aries': '♈',
        'Stier': '♉', 'Taurus': '♉',
        'Tweelingen': '♊', 'Gemini': '♊',
        'Kreeft': '♋', 'Cancer': '♋',
        'Leeuw': '♌', 'Leo': '♌',
        'Maagd': '♍', 'Virgo': '♍',
        'Weegschaal': '♎', 'Libra': '♎',
        'Schorpioen': '♏', 'Scorpio': '♏',
        'Boogschutter': '♐', 'Sagittarius': '♐',
        'Steenbok': '♑', 'Capricorn': '♑',
        'Waterman': '♒', 'Aquarius': '♒',
        'Vissen': '♓', 'Pisces': '♓'
    };
    // Handle potential extra whitespace or case
    const cleanName = name.trim();
    return icons[cleanName] || '✨';
}

async function loadStats() {
    try {
        const response = await fetch(`/api/stats/${currentGame}`);
        if (!response.ok) return;
        
        const data = await response.json();
        renderChart(data.frequency);
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

function renderChart(freqData) {
    const ctx = document.getElementById('freqChart').getContext('2d');
    
    // Sort by number
    const sortedKeys = Object.keys(freqData).sort((a, b) => parseInt(a) - parseInt(b));
    const values = sortedKeys.map(k => freqData[k]);
    
    if (chartInstance) {
        chartInstance.destroy();
    }
    
    chartInstance = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: sortedKeys,
            datasets: [{
                label: 'Frequency',
                data: values,
                backgroundColor: 'rgba(56, 189, 248, 0.6)',
                borderColor: '#38bdf8',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(255, 255, 255, 0.1)'
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        color: '#94a3b8'
                    }
                }
            }
        }
    });
}

// Initial load
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
});

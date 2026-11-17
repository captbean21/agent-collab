/**
 * EnemyManager - Handles enemy entities, spawning, and wave difficulty scaling.
 */
class EnemyManager {
  constructor() {
    this.enemies = [];
    this.difficultyConfig = {
      speedMultiplierPerWave: 0.10, // +10% per wave
      healthMultiplierPerWave: 0.05, // +5% per wave
      scoreMultiplierPerWave: 0.10  // +10% per wave
    };
  }

  // Spawns a new enemy at the specified position with difficulty scaling
  spawnEnemy(x, y, type = 'basic', wave = 1) {
    const baseConfig = {
      basic: { hp: 1, speed: 50, radius: 10, damage: 10, scoreValue: 100, shape: 'circle' },
      fast: { hp: 1, speed: 100, radius: 5, damage: 5, scoreValue: 200, shape: 'circle' },
      tank: { hp: 5, speed: 25, radius: 20, damage: 20, scoreValue: 500, shape: 'circle' }
    };

    const typeConfig = baseConfig[type] || baseConfig.basic;
    
    // Apply difficulty scaling (capped at wave 100)
    const waveMult = Math.min(wave - 1, 99);
    const speed = typeConfig.speed * (1 + (this.difficultyConfig.speedMultiplierPerWave * waveMult));
    const health = typeConfig.hp * (1 + (this.difficultyConfig.healthMultiplierPerWave * waveMult));
    const scoreValue = Math.floor(typeConfig.scoreValue * (1 + (this.difficultyConfig.scoreMultiplierPerWave * waveMult)));

    const enemy = {
      id: Math.random().toString(36).substr(2, 9),
      x,
      y,
      type,
      ...typeConfig,
      speed,
      health,
      scoreValue,
      markedForRemoval: false
    };

    this.enemies.push(enemy);
    return enemy;
  }

  // Returns enemy type pool based on wave number
  getTypesForWave(wave) {
    if (wave === 1) return ['basic'];
    if (wave === 2) return ['basic', 'fast'];
    return ['basic', 'fast', 'tank'];
  }

  // Spawns a wave of enemies with mixed types
  spawnWave(count, centerX, centerY, wave) {
    const types = this.getTypesForWave(wave);
    const waveEnemies = [];
    
    for (let i = 0; i < count; i++) {
      const type = types[i % types.length];
      const angle = (i / count) * Math.PI * 2;
      const x = centerX + Math.cos(angle) * 50;
      const y = centerY + Math.sin(angle) * 50;
      waveEnemies.push(this.spawnEnemy(x, y, type, wave));
    }
    return waveEnemies;
  }

  // Updates enemy positions and AI state
  update(deltaTime, targetX, targetY) {
    for (const enemy of this.enemies) {
      if (targetX !== undefined && targetY !== undefined) {
        const dx = targetX - enemy.x;
        const dy = targetY - enemy.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 0) {
          enemy.x += (dx / dist) * enemy.speed * deltaTime;
          enemy.y += (dy / dist) * enemy.speed * deltaTime;
        }
      }
    }
  }

  // Removes destroyed enemies
  cleanup() {
    this.enemies = this.enemies.filter(e => e.health > 0 && !e.markedForRemoval);
  }

  // Returns all active enemies
  getEnemies() {
    return this.enemies;
  }
}

export { EnemyManager };

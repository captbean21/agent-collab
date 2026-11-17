/**
 * EnemyManager interface
 * Responsible for managing enemy entities, spawning, and basic movement.
 */
class EnemyManager {
  constructor() {
    this.enemies = [];
  }

  // Spawns a new enemy at the specified position
  spawnEnemy(x, y, type = 'basic') {
    const config = {
      basic: { hp: 1, speed: 50, radius: 10, damage: 10, scoreValue: 100, shape: 'circle' },
      fast: { hp: 1, speed: 100, radius: 5, damage: 5, scoreValue: 200, shape: 'circle' },
      tank: { hp: 5, speed: 25, radius: 20, damage: 20, scoreValue: 500, shape: 'circle' }
    };

    const typeConfig = config[type] || config.basic;
    const enemy = {
      id: Math.random().toString(36).substr(2, 9),
      x,
      y,
      type,
      ...typeConfig,
      health: typeConfig.hp,
      markedForRemoval: false
    };

    this.enemies.push(enemy);
    return enemy;
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

  // Spawns a wave of enemies
  spawnWave(count, type, centerX, centerY) {
    const wave = [];
    for (let i = 0; i < count; i++) {
      const angle = (i / count) * Math.PI * 2;
      const x = centerX + Math.cos(angle) * 50;
      const y = centerY + Math.sin(angle) * 50;
      wave.push(this.spawnEnemy(x, y, type));
    }
    return wave;
  }

  // Returns all active enemies
  getEnemies() {
    return this.enemies;
  }
}

export { EnemyManager };

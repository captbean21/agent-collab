/**
 * GameController - Integration Layer
 * Integrates Player, EnemyManager, CollisionManager, AudioManager, and BulletManager into the main game loop.
 */
import { audioManager } from './audio.js';

class GameController {
  constructor(player, enemyManager, collisionManager, bulletManager, audioManagerInstance = null) {
    this.player = player;
    this.enemyManager = enemyManager;
    this.collisionManager = collisionManager;
    this.bulletManager = bulletManager;
    this.audioManager = audioManagerInstance || audioManager;
    this.score = 0;
    this.lives = 3;
    this.wave = 1;
    this.isGameOver = false;
  }

  // Fires a bullet if possible
  fire(currentTime) {
    const bullet = this.bulletManager.fire(
      this.player.x,
      this.player.y,
      this.player.vx ?? 0,
      this.player.vy ?? 0,
      currentTime
    );
    if (bullet) {
      this.audioManager.playShoot();
    }
    return bullet;
  }

  // Orchestrates the core game loop logic
  update(deltaTime, currentTime) {
    if (this.isGameOver) return;

    // 1. Audio: Update engine pitch based on player speed
    const speedRatio = Math.min(this.player.speed / (this.player.maxSpeed || 500), 1);
    this.audioManager.setEnginePitch(speedRatio);

    // 2. Update entities
    this.enemyManager.update(deltaTime, this.player.x, this.player.y);
    this.bulletManager.update(deltaTime, currentTime);

    // 3. Detect collisions
    this.collisionManager.colliders = [
      this.player, 
      ...this.enemyManager.getEnemies(),
      ...this.bulletManager.getBullets()
    ];
    const collisions = this.collisionManager.update();
    
    for (const [a, b] of collisions) {
      this.handleCollision(a, b);
    }

    // 4. Cleanup destroyed/inactive entities
    this.enemyManager.cleanup();
    this.bulletManager.cleanup();

    // 5. Wave management
    if (this.enemyManager.getEnemies().length === 0) {
      this.wave++;
      this.enemyManager.spawnWave(this.wave * 2, 400, 300, this.wave);
      this.audioManager.playWaveComplete();
    }

    // 6. Game Over conditions
    if (this.lives <= 0) {
      this.isGameOver = true;
      this.audioManager.playGameOver();
    }
  }

  // Resolves interaction between entities
  handleCollision(a, b) {
    // Identify player (by reference)
    const player = (a === this.player) ? a : (b === this.player) ? b : null;
    
    // Identify bullet (has createdAt) and enemy (has health)
    const bullet = (a.createdAt !== undefined) ? a : (b.createdAt !== undefined) ? b : null;
    const enemy = (a.health !== undefined) ? a : (b.health !== undefined) ? b : null;

    if (bullet && enemy && !bullet.markedForRemoval && !enemy.markedForRemoval) {
      // Bullet hits enemy
      bullet.markedForRemoval = true;
      enemy.health -= bullet.damage;
      if (enemy.health <= 0) {
        enemy.markedForRemoval = true;
        this.score += enemy.scoreValue;
        this.audioManager.playScore(enemy.scoreValue);
        this.audioManager.playEnemyDestroyed(enemy.type);
      }
    } else if (player && enemy && !enemy.markedForRemoval) {
      // Player hits enemy
      this.lives--;
      this.audioManager.playPlayerHit();
      enemy.markedForRemoval = true;
    }
  }

  // Returns current game state
  getState() {
    return {
      score: this.score,
      lives: this.lives,
      wave: this.wave,
      isGameOver: this.isGameOver,
      bullets: this.bulletManager ? this.bulletManager.getBullets().length : 0
    };
  }
}

export { GameController };

/**
 * GameController - Integration Layer
 * Integrates Player, EnemyManager, CollisionManager, AudioManager, and BulletManager into the main game loop.
 */
import { audioManager } from './audio.js';

class GameController {
  constructor(player, enemyManager, collisionManager, bulletManager) {
    this.player = player;
    this.enemyManager = enemyManager;
    this.collisionManager = collisionManager;
    this.bulletManager = bulletManager;
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
      this.player.vx || 0,
      this.player.vy || -1,
      currentTime
    );
    if (bullet) {
      // audioManager.playShoot(); // Placeholder for future audio
    }
  }

  // Orchestrates the core game loop logic
  update(deltaTime, currentTime) {
    if (this.isGameOver) return;

    // 1. Audio: Update engine pitch based on player speed
    const speedRatio = Math.min(this.player.speed / (this.player.maxSpeed || 500), 1);
    audioManager.setEnginePitch(speedRatio);

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
      audioManager.playWaveComplete();
    }

    // 6. Game Over conditions
    if (this.lives <= 0) {
      this.isGameOver = true;
      audioManager.playGameOver();
    }
  }

  // Resolves interaction between entities
  handleCollision(a, b) {
    // Identify bullet-enemy collisions
    const bullet = (a.vx !== undefined) ? a : (b.vx !== undefined) ? b : null;
    const enemy = (a.type !== undefined) ? a : (b.type !== undefined) ? b : null;
    
    // Identify player-enemy collisions
    const player = (a === this.player) ? a : (b === this.player) ? b : null;

    if (bullet && enemy && !bullet.markedForRemoval && !enemy.markedForRemoval) {
      // Bullet hits enemy
      bullet.markedForRemoval = true;
      enemy.health -= bullet.damage;
      if (enemy.health <= 0) {
        enemy.markedForRemoval = true;
        this.score += enemy.scoreValue;
        audioManager.playScore(enemy.scoreValue);
        audioManager.playEnemyDestroyed(enemy.type);
      }
    } else if (player && enemy && !enemy.markedForRemoval) {
      // Player hits enemy
      this.lives--;
      audioManager.playPlayerHit();
      enemy.markedForRemoval = true;
    }
  }

  // Returns current game state
  getState() {
    return {
      score: this.score,
      lives: this.lives,
      wave: this.wave,
      isGameOver: this.isGameOver
    };
  }
}

export { GameController };

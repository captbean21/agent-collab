/**
 * GameController - Integration Layer
 * Integrates Player, EnemyManager, and CollisionManager into the main game loop.
 */
class GameController {
  constructor(player, enemyManager, collisionManager) {
    this.player = player;
    this.enemyManager = enemyManager;
    this.collisionManager = collisionManager;
    this.score = 0;
    this.lives = 3;
    this.wave = 1;
    this.isGameOver = false;
  }

  // Orchestrates the core game loop logic
  update(deltaTime) {
    if (this.isGameOver) return;

    // 1. Update enemies
    this.enemyManager.update(deltaTime, this.player.x, this.player.y);

    // 2. Detect collisions
    this.collisionManager.colliders = [this.player, ...this.enemyManager.getEnemies()];
    const collisions = this.collisionManager.update();
    
    for (const [a, b] of collisions) {
      this.handleCollision(a, b);
    }

    // 3. Cleanup destroyed/inactive entities
    this.enemyManager.cleanup();

    // 4. Wave management
    if (this.enemyManager.getEnemies().length === 0) {
      this.wave++;
      this.enemyManager.spawnWave(this.wave * 2, 'basic', 400, 300);
    }

    // 5. Game Over conditions
    if (this.lives <= 0) {
      this.isGameOver = true;
    }
  }

  // Resolves interaction between entities
  handleCollision(a, b) {
    const player = (a === this.player) ? a : (b === this.player) ? b : null;
    const enemy = (a !== this.player) ? a : (b !== this.player) ? b : null;

    if (player && enemy) {
      this.lives--;
      enemy.markedForRemoval = true; // Enemy destroyed on impact
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

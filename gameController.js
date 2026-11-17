/**
 * GameController interface
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

    // 1. Update player physics (assumed to be handled by player instance)
    
    // 2. Update enemies
    this.enemyManager.update(deltaTime, this.player.x, this.player.y);

    // 3. Detect collisions
    // Clear colliders and re-register
    this.collisionManager.colliders = [];
    this.collisionManager.addCollider(this.player);
    this.enemyManager.getEnemies().forEach(e => this.collisionManager.addCollider(e));

    const collisions = this.collisionManager.update();
    for (const [a, b] of collisions) {
      this.handleCollision(a, b);
    }

    // 4. Cleanup destroyed entities
    this.enemyManager.cleanup();

    // 5. Check win/loss conditions
    if (this.lives <= 0) {
      this.isGameOver = true;
    }
  }

  // Resolves interaction between entities
  handleCollision(a, b) {
    // Logic for player vs enemy or enemy vs enemy
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

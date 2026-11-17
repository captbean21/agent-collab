/**
 * EnemyManager interface
 * Responsible for managing enemy entities, spawning, and basic movement.
 */
class EnemyManager {
  constructor() {
    this.enemies = [];
  }

  // Spawns a new enemy at the specified position
  spawnEnemy(x, y, type) {
    // To be implemented: entity creation
  }

  // Updates enemy positions and AI state
  update(deltaTime) {
    // To be implemented: movement logic and AI behaviors
  }

  // Removes destroyed enemies
  cleanup() {
    // To be implemented: filtering out inactive enemies
  }
}

export { EnemyManager };

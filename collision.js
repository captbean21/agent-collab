/**
 * CollisionManager interface
 * Responsible for detecting interactions between game entities.
 */
class CollisionManager {
  constructor() {
    this.colliders = [];
  }

  // Register an entity to check against
  addCollider(entity) {
    this.colliders.push(entity);
  }

  // Interface for detecting if two entities overlap
  // To be implemented: circle-circle or AABB logic
  checkCollision(entityA, entityB) {
    return false; // Stub
  }

  // Update loop for collision checking
  update() {
    // To be implemented: sweep through colliders and report intersections
  }
}

export { CollisionManager };

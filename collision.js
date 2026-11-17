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

  // Detects if two entities overlap based on shape
  checkCollision(entityA, entityB) {
    // Circle-Circle collision
    if (entityA.shape === 'circle' && entityB.shape === 'circle') {
      const dx = entityA.x - entityB.x;
      const dy = entityA.y - entityB.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      return distance < (entityA.radius + entityB.radius);
    }
    
    // AABB-AABB collision
    if (entityA.shape === 'rect' && entityB.shape === 'rect') {
      return (
        entityA.x < entityB.x + entityB.width &&
        entityA.x + entityA.width > entityB.x &&
        entityA.y < entityB.y + entityB.height &&
        entityA.y + entityA.height > entityB.y
      );
    }

    // Circle-AABB collision
    if (entityA.shape === 'circle' && entityB.shape === 'rect') {
      const closestX = Math.max(entityB.x, Math.min(entityA.x, entityB.x + entityB.width));
      const closestY = Math.max(entityB.y, Math.min(entityA.y, entityB.y + entityB.height));
      const dx = entityA.x - closestX;
      const dy = entityA.y - closestY;
      return (dx * dx + dy * dy) < (entityA.radius * entityA.radius);
    }
    
    return false;
  }

  // Update loop for collision checking
  update() {
    const collisions = [];
    for (let i = 0; i < this.colliders.length; i++) {
      for (let j = i + 1; j < this.colliders.length; j++) {
        if (this.checkCollision(this.colliders[i], this.colliders[j])) {
          collisions.push([this.colliders[i], this.colliders[j]]);
        }
      }
    }
    return collisions;
  }
}

export { CollisionManager };

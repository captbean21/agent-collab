/**
 * BulletManager - Handles player projectiles
 */
class BulletManager {
  constructor(config = {}) {
    this.bullets = [];
    this.config = {
      speed: config.speed || 500,
      radius: config.radius || 3,
      lifetime: config.lifetime || 2000, // ms
      cooldown: config.cooldown || 150, // ms
      damage: config.damage || 1
    };
    this.lastShotTime = 0;
  }

  // Fires a bullet from the player's position
  fire(playerX, playerY, playerVx, playerVy, currentTime) {
    if (currentTime - this.lastShotTime < this.config.cooldown) {
      return null;
    }

    // Normalize velocity to bullet speed
    const mag = Math.sqrt(playerVx * playerVx + playerVy * playerVy) || 1;
    const vx = (playerVx / mag) * this.config.speed;
    const vy = (playerVy / mag) * this.config.speed;

    const bullet = {
      id: Math.random().toString(36).substr(2, 9),
      x: playerX,
      y: playerY,
      vx,
      vy,
      radius: this.config.radius,
      damage: this.config.damage,
      lifetime: this.config.lifetime,
      createdAt: currentTime,
      markedForRemoval: false
    };

    this.bullets.push(bullet);
    this.lastShotTime = currentTime;
    return bullet;
  }

  // Updates bullet positions and handles expiry
  update(deltaTime, currentTime) {
    for (const bullet of this.bullets) {
      bullet.x += bullet.vx * deltaTime;
      bullet.y += bullet.vy * deltaTime;

      if (currentTime - bullet.createdAt > bullet.lifetime) {
        bullet.markedForRemoval = true;
      }
    }
  }

  // Removes expired or collided bullets
  cleanup() {
    this.bullets = this.bullets.filter(b => !b.markedForRemoval);
  }

  getBullets() {
    return this.bullets;
  }
}

export { BulletManager };

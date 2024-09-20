import random
import math

# Constants
NUM_PARTICLES = 100
MAX_INT = 10**6  # The maximum integer (computational limit)
MAX_MASS = 1000  # Maximum mass of a particle
MAX_POSITION = 1000  # Maximum position value
TIME_STEPS = 100  # Number of time steps for simulation

# Particle Class Definition
class Particle:
    def __init__(self, mass, position):
        self.mass = min(mass, MAX_MASS)  # Ensure mass is constrained by MAX_MASS
        self.position = position  # Position is a 2D tuple (x, y)
        self.velocity = (0, 0)  # Initial velocity is (0, 0)
    
    def apply_force(self, force):
        """ Update the velocity based on a force. """
        # Simplified force application (ignores directionality for simplicity)
        fx, fy = force
        ax = fx / self.mass
        ay = fy / self.mass
        vx, vy = self.velocity
        self.velocity = (vx + ax, vy + ay)
    
    def update_position(self):
        """ Update position based on velocity and respect the computational limit. """
        x, y = self.position
        vx, vy = self.velocity
        # Update position while respecting computational limits
        new_x = min(x + vx, MAX_POSITION)
        new_y = min(y + vy, MAX_POSITION)
        self.position = (new_x, new_y)

# Gravitational-like force calculation
def gravitational_force(p1, p2):
    """ Simplified gravity-like force between two particles. """
    G = 1  # Gravitational constant (simplified)
    x1, y1 = p1.position
    x2, y2 = p2.position
    dx = x2 - x1
    dy = y2 - y1
    distance = math.sqrt(dx**2 + dy**2)
    
    if distance == 0:
        return (0, 0)  # No force if particles overlap
    
    force_magnitude = G * p1.mass * p2.mass / (distance**2 + 1)  # Avoid division by zero
    fx = force_magnitude * (dx / distance)
    fy = force_magnitude * (dy / distance)
    return (fx, fy)

# Universe State Initialization
particles = []
for _ in range(NUM_PARTICLES):
    mass = random.randint(1, MAX_MASS)
    position = (random.randint(0, MAX_POSITION), random.randint(0, MAX_POSITION))
    particles.append(Particle(mass, position))

# Time Evolution Simulation
for t in range(TIME_STEPS):
    print(f"Time step {t}:")
    
    # Compute interactions between particles
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            p1 = particles[i]
            p2 = particles[j]
            
            # Calculate the gravitational force between p1 and p2
            force = gravitational_force(p1, p2)
            
            # Apply the force to both particles (Newton's third law)
            p1.apply_force(force)
            p2.apply_force((-force[0], -force[1]))  # Opposite force on p2
    
    # Update particle positions
    for particle in particles:
        particle.update_position()
    
    # Print particle states (for simplicity, printing only positions)
    for idx, particle in enumerate(particles):
        print(f"Particle {idx}: Position {particle.position}, Mass {particle.mass}")
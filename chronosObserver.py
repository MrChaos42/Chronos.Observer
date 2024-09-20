import random
import math

# Constants
NUM_PARTICLES = 42
MAX_INT = 10**6  # The maximum integer (computational limit)
MAX_MASS = 42  # Maximum mass of a particle
MAX_POSITION = 42  # Maximum position value
TIME_STEPS = 42  # Number of time steps for simulation

# Particle Class Definition
class Particle:
    def __init__(self, mass, position, charge):
        self.mass = min(mass, MAX_MASS)  # Ensure mass is constrained by MAX_MASS
        self.position = position  # Position is a 2D tuple (x, y)
        self.velocity = (0, 0)  # Initial velocity is (0, 0)
        self.charge = charge  # Charge: +1, -1, or 0 for simplicity

    def apply_force(self, force):
        """ Update the velocity based on a force. """
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
        new_x = min(max(x + vx, 0), MAX_POSITION)
        new_y = min(max(y + vy, 0), MAX_POSITION)
        self.position = (new_x, new_y)

# Force calculation functions
def gravitational_force(p1, p2):
    """ Simplified gravity-like force between two particles. """
    G = 1  # Gravitational constant (simplified)
    x1, y1 = p1.position
    x2, y2 = p2.position
    dx = x2 - x1
    dy = y2 - y1
    distance_sq = dx**2 + dy**2
    distance = math.sqrt(distance_sq)

    if distance == 0:
        return (0, 0)  # No force if particles overlap

    force_magnitude = G * p1.mass * p2.mass / (distance_sq + 1)  # Avoid division by zero
    fx = force_magnitude * (dx / distance)
    fy = force_magnitude * (dy / distance)
    return (fx, fy)

def electromagnetic_force(p1, p2):
    """ Simplified electromagnetic force between two particles. """
    k = 8.9875517923e9  # Coulomb's constant in N·m²/C²
    q1, q2 = p1.charge, p2.charge
    if q1 == 0 or q2 == 0:
        return (0, 0)  # No electromagnetic force if either charge is zero

    x1, y1 = p1.position
    x2, y2 = p2.position
    dx = x2 - x1
    dy = y2 - y1
    distance_sq = dx**2 + dy**2
    distance = math.sqrt(distance_sq)

    if distance == 0:
        return (0, 0)  # No force if particles overlap

    force_magnitude = k * q1 * q2 / (distance_sq + 1)  # Avoid division by zero
    fx = force_magnitude * (dx / distance)
    fy = force_magnitude * (dy / distance)
    return (fx, fy)

# Universe State Initialization
particles = []
for _ in range(NUM_PARTICLES):
    mass = random.randint(1, MAX_MASS)
    position = (random.randint(0, MAX_POSITION), random.randint(0, MAX_POSITION))
    charge = random.choice([-1, 0, 1])  # Simplified charge assignment
    particles.append(Particle(mass, position, charge))

# Time Evolution Simulation
for t in range(TIME_STEPS):
    print(f"\nTime step {t}:")
    
    # Compute interactions between particles
    for i in range(NUM_PARTICLES):
        for j in range(i + 1, NUM_PARTICLES):
            p1 = particles[i]
            p2 = particles[j]
            
            # Calculate the gravitational force between p1 and p2
            grav_force = gravitational_force(p1, p2)
            # Calculate the electromagnetic force between p1 and p2
            em_force = electromagnetic_force(p1, p2)
            
            # Total force is the sum of gravitational and electromagnetic forces
            total_force = (grav_force[0] + em_force[0], grav_force[1] + em_force[1])
            
            # Apply the force to both particles (Newton's third law)
            p1.apply_force(total_force)
            p2.apply_force((-total_force[0], -total_force[1]))  # Opposite force on p2
    
    # Update particle positions
    for particle in particles:
        particle.update_position()
    
    # Print particle states (for simplicity, printing only positions and charges)
    for idx, particle in enumerate(particles):
        print(f"Particle {idx}: Position {particle.position}, Mass {particle.mass}, Charge {particle.charge}")

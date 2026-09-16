

import pygame
import math
import random

class Heart:
    def __init__(self, x, y, grid_size):
        self.x = x
        self.y = y
        self.grid_size = grid_size
        self.size = grid_size
        self.beat_phase = 0
        self.beat_speed = 0.08
        self.max_scale = 1.3
        self.min_scale = 0.9
        self.color = (255, 50, 80)  # Deep red
        self.glow_color = (255, 100, 150)  # Pink glow
        self.particles = []
        
    def update(self):
        """Update heart beat animation"""
        self.beat_phase += self.beat_speed
        if self.beat_phase > math.pi * 2:
            self.beat_phase = 0
            
        # Calculate beat scale (pulsing effect)
        # Uses sine wave with sharp peak for "beat" effect
        beat_value = math.sin(self.beat_phase)
        # Make the beat more dramatic
        if beat_value > 0.8:
            scale = self.max_scale
        else:
            scale = self.min_scale + (beat_value + 1) * 0.2
        
        # Update particles
        for particle in self.particles[:]:
            particle['life'] -= 0.02
            particle['y'] -= 1
            particle['x'] += particle['vx']
            if particle['life'] <= 0:
                self.particles.remove(particle)
        
        # Spawn particles on strong beats
        if beat_value > 0.9:
            for _ in range(3):
                self.particles.append({
                    'x': self.x + self.grid_size // 2,
                    'y': self.y + self.grid_size // 2,
                    'vx': random.uniform(-2, 2),
                    'life': 1.0,
                    'size': random.randint(2, 4)
                })
        
        return scale
    
    def draw(self, screen, offset_x=0, offset_y=0):
        """Draw the beating heart with glow effect"""
        scale = self.update()
        
        # Calculate center position
        center_x = self.x + self.grid_size // 2 + offset_x
        center_y = self.y + self.grid_size // 2 + offset_y
        size = int(self.grid_size * scale * 0.6)
        
        # Draw glow
        for i in range(3, 0, -1):
            glow_alpha = 30 - i * 8
            glow_size = size + i * 8
            glow_surface = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.glow_color, glow_alpha), 
                             (glow_size, glow_size), glow_size)
            screen.blit(glow_surface, (center_x - glow_size, center_y - glow_size))
        
        # Draw the heart using polygon
        heart_points = self.get_heart_points(center_x, center_y, size)
        pygame.draw.polygon(screen, self.color, heart_points)
        
        # Draw highlight
        highlight_points = self.get_heart_points(center_x - 2, center_y - 2, size * 0.7)
        for i, point in enumerate(highlight_points):
            highlight_points[i] = (point[0] + 2, point[1] + 2)
        pygame.draw.polygon(screen, (255, 150, 180), highlight_points, 1)
        
        # Draw particles
        for particle in self.particles:
            alpha = int(particle['life'] * 200)
            particle_surface = pygame.Surface((particle['size'] * 2, particle['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(particle_surface, (*self.glow_color, alpha), 
                             (particle['size'], particle['size']), particle['size'])
            screen.blit(particle_surface, (particle['x'] - particle['size'], particle['y'] - particle['size']))
    
    def get_heart_points(self, cx, cy, size):
        """Generate heart shape points"""
        points = []
        # Heart curve using parametric equations
        for t in range(0, 360, 5):
            rad = math.radians(t)
            # Heart formula: x = 16*sin³(t), y = 13*cos(t) - 5*cos(2t) - 2*cos(3t) - cos(4t)
            x = 16 * math.pow(math.sin(rad), 3)
            y = 13 * math.cos(rad) - 5 * math.cos(2*rad) - 2 * math.cos(3*rad) - math.cos(4*rad)
            # Scale and position
            scale_factor = size / 16
            points.append((cx + x * scale_factor, cy - y * scale_factor))
        return points
    
    def get_rect(self):
        """Get the collision rectangle"""
        return pygame.Rect(self.x, self.y, self.grid_size, self.grid_size)
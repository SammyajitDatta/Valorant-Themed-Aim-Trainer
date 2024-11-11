import pygame
import random
import time

while True:
    try:
        numberOfTargets = int(input("How many targets do you want to practice with? Enter it here: "))
        if numberOfTargets>0:
            break
        else:
            print("The number of targets has to be a positive amount.")
    except ValueError:
        print("Invalid input. Please enter a valid positive integer.")

# Initialize pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 1920, 1080

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Different valorant character head models, can add more to increase 
potentialTargetFaces = ["Omen.png", "Sage.png", "Skye.png"]

# Load and scale the background image
ValorantWallpaper = pygame.image.load("AscentMid.png")
ValorantWallpaper = pygame.transform.scale(ValorantWallpaper, (WIDTH, HEIGHT))


targetSize = 50  # Set a size for positioning
# Choose a random valorant character, loads that image which creates a surface object and scale the surface to a desired size.
targetPicture = pygame.transform.scale(pygame.image.load(potentialTargetFaces[random.randint(0, len(potentialTargetFaces)-1)]), (targetSize * 2, targetSize * 2))

# Game variables
score = 0
timerStart = time.time()

# Creates font object with default style and 36 size font.
font = pygame.font.Font(None, 100)

# Function to spawn a new target at random position
def targetGeneration():
    x = random.randint(targetSize, WIDTH - targetSize)
    y = random.randint(targetSize, HEIGHT - targetSize)
    # Creates a rect object cemtered at (x,y) with the dimensions replicating a square with length twice of the target size
    # Returns a tuple of the target and it's position
    return pygame.Rect(x - targetSize, y - targetSize, targetSize * 2, targetSize * 2), (x, y)

# Initial target
# Appropriately deconstructs the tuple
target, targetPos = targetGeneration()

# Counter with the purpose to keep target image the same until the image is hit, before randomly generating a new image
counter = 1

# Game loop
while True:
    # Draw the background image starting at the top left 
    screen.blit(ValorantWallpaper, (0, 0))

    # Check events
    for event in pygame.event.get():
        # Checks to see if the user wants to quit
        if event.type == pygame.QUIT:
            break
        # Checks for mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Checks to see if the click is within the target bounds
            if target.collidepoint(event.pos):
                # Increment score, adjust counter to notify random image selector that its time to change and generate new target
                score += 1
                counter-=1 
                target, targetPos = targetGeneration() 

    # End game condition
    if score == numberOfTargets:
        break

    # Draw the target image
    if target :
        # Randomly reload the image if previous character was hit
        if (not counter):
            targetPicture = pygame.transform.scale(pygame.image.load(potentialTargetFaces[random.randint(0, len(potentialTargetFaces)-1)]), (targetSize * 2, targetSize * 2))
            counter = 1
        # Print image onto the target location
        screen.blit(targetPicture, (targetPos[0] - targetSize, targetPos[1] - targetSize))

    # Show score
    # Set True to enable Anti-Aliasing meaning the render will be cleaner and less pixalated
    scoreText = font.render("Score: " + str(score), True, (255,255,255))
    screen.blit(scoreText, (50, 50))

    # Changes are made to a buffer, flipping this make us able to see the new changes
    pygame.display.flip()

# Calculate average time to hit a target
averageTimeToHitTarget = (time.time()-timerStart)/numberOfTargets

# Display Results on black screen 
screen.fill((0,0,0))
results = font.render("Game Over! Average Time: " + str(round(averageTimeToHitTarget,2)) +  "sec", True, (255,255,255))
screen.blit(results, (400, 540))

# Buffer flip
pygame.display.flip()

# Wait 3 seconds before closing the game, giving users enough time to see results
pygame.time.delay(2000)
pygame.quit()

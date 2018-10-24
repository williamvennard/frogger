var ctlKey;
var collision = 50; 
var score = 0;

// Enemies our player must avoid
var Enemy = function() {
    // Variables applied to each of our instances go here,
    // we've provided one for you to get started
    // The image/sprite for our enemies, this uses
    // a helper we've provided to easily load images
    esprite = 'images/enemy-bug.png';
    this.x = -100;
    this.y = 234;
    //variable speeds
    this.speed = 100 + Math.random()*(200);
    //random location for enemy
    enemyRand = Math.random();
    if (enemyRand < 0.33) {
        this.y = this.y; 
    }else if (enemyRand < 0.66) {
        this.y = this.y - 83;
    }else {
        this.y = this.y - 83*2;
    }
};
// Update the enemy's position, required method for game
// Parameter: dt, a time delta between ticks
Enemy.prototype.update = function(dt) {  
    this.x += (this.speed * dt);
    if (this.x > 500) {
        this.x = -100;
        this.y = 234;
        //variable speeds
        this.speed = 100 + Math.random()*(200);
        //random location for enemy
        enemyRand = Math.random();
        if (enemyRand < 0.33) {
            this.y = this.y; 
        }else if (enemyRand < 0.66) {
            this.y = this.y - 83;
        }else {
            this.y = this.y - 83*2;
        }
    }

    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
    // Collision logic
    triggerXCollision = Math.abs(this.x-x) <= collision;
    triggerYCollision = Math.abs(this.y-y) <= collision;
    if ((triggerYCollision && triggerXCollision) === true) {
        alert("LOSER!!");
        score = 0;
        document.getElementById("score").innerHTML = score;
        player.reset();
    }
};

// Draw the enemy on the screen, required method for game
Enemy.prototype.render = function() {
    ctx.drawImage(Resources.get(esprite), this.x, this.y);
};

// Now write your own player class
// This class requires an update(), render() and
// a handleInput() method.
var player = function() {
    x = 200;
    y = 400;
    sprite = 'images/char-boy.png';  
};

// Draw the player on the screen, required method for game
player.render = function() {
    ctx.drawImage(Resources.get(sprite), x, y);
};

player.handleInput = function(allowedKeys) {
    ctlKey = allowedKeys;
};

// Update the player's position, required method for game
// Parameter: dt, a time delta between ticks
player.update = function() {
    if (ctlKey === 'left' && x > 0){ 
        x = x - 100;
    } else if (ctlKey === 'right' && x != 400){
        x = x + 100;
    } else if (ctlKey === 'up'){
        y = y - 83;
    } else if (ctlKey === 'down' && y != 400){
        y = y + 83;
    }
    ctlKey = null;

    if (y < 60){
        //alert("WINNER!!");
        score++;
        player.reset();
        console.log(score);
        document.getElementById("score").innerHTML = score;
    }
    // You should multiply any movement by the dt parameter
    // which will ensure the game runs at the same speed for
    // all computers.
};

player.reset = function() {   
      x = 200;
      y = 400;
};

// Now instantiate your objects.
var enemy1 = new Enemy();
var enemy2 = new Enemy();
var enemy3 = new Enemy();
// Place all enemy objects in an array called allEnemies
var allEnemies = [enemy1, enemy2, enemy3];

// Place the player object in a variable called player
var Player = new player();

// This listens for key presses and sends the keys to your
// Player.handleInput() method. You don't need to modify this.
document.addEventListener('keyup', function(e) {
    var allowedKeys = {
        37: 'left',
        38: 'up',
        39: 'right',
        40: 'down'
    };
    player.handleInput(allowedKeys[e.keyCode]);
});
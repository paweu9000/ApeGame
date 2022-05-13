var moves = JSON.parse('{{ move_list | safe }}');
var combat_div = document.getElementById("combat_div");
var gorilla_hp_list = JSON.parse('{{gorilla_hp_list}}');
var enemy_hp_list = JSON.parse('{{enemy_hp_list}}');


function next_move(){
    
    var timer = 0;

    for (let i=0; i<moves.length; i++){
        
        setTimeout(() => {
            var ptag = document.createElement('p');
            ptag.className = "line";
            ptag.innerHTML = moves[i];
            combat_div.appendChild(ptag);
        }, timer);
        
        timer = timer + 500;
    }
}

function gorillahealth(){
    
    var timer = 0;

    for (let i=0; i<gorilla_hp_list.length; i++){
        
        setTimeout(() => {
            document.getElementById("gorilla_health").innerHTML = gorilla_hp_list[i] +' HP';
        }, timer);
        if (i>0){
            timer = timer + 1000;
        }
        else{
            timer = timer + 500;
        }
    }
}
function enemyhealth(){
    
    var timer = 0;

    for (let i=0; i<gorilla_hp_list.length; i++){
        
        setTimeout(() => {
            document.getElementById("enemy_health").innerHTML = enemy_hp_list[i] +' HP';
        }, timer);
        timer = timer + 500;
    }
}

next_move();
gorillahealth();
enemyhealth();
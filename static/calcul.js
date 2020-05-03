console.log("Rechargement de la page");
msg11 = document.getElementById("msg11").value;
msg22 = document.getElementById("msg22").value;
/*console.log(msg11);
console.log(msg22);*/
/*ajax au chargement de la page*/
$.ajax({
    url: "/api/calculette/"+msg22+"+"+msg22,
    success: somme
});

/*Uniquement sur un evenement*/
$("#submit2").click(function(event){
    console.log("Event sur click 1");      
    event.preventDefault();  // Empêcher le rechargement de la page.
    msg11 = document.getElementById("msg11").value;
    msg22 = document.getElementById("msg22").value;
    operateur2 = document.getElementById("operateur2").value;
    urlEnvoye = "/api/calculette/"+parseFloat(msg11)+";"+operateur2+";"+parseFloat(msg22)
    /*alert ("Quelqu'un a cliqué sur le bouton c !")*/
    console.log(urlEnvoye);  
    $.ajax({
    url: urlEnvoye,
    success: somme
});
});



function somme(result){
    console.log("Nous allons afficher le resultat du calcul");
    console.log("Résultat de la requête :", result);
    document.getElementById("resultatBis").value=result;
}


console.log("Au revoir");


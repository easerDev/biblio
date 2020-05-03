console.log("Rechargement de la page");


/*Uniquement sur un evenement*/
$("#submitParAJax").click(function(event){
    event.preventDefault();  // Empêcher le rechargement de la page.
    console.log("Event sur click 1");   
     /*alert ("Quelqu'un a cliqué sur le bouton c !")*/   
    
    /*console.log(document.getElementById("msg2ParAjax").value);  
    console.log($("#msg2ParAjax").val());      
    console.log(document.getElementById("resultatParAjax").value); //$("#resultatParAjax").val()     
    console.log(document.getElementById("modifAjax").innerText);  
    console.log('$("#modifAjax").text() : ' + $("#modifAjax").text());  */
    
    /*pour tester une api pour exemple*/
    urlEnvoye = "/api/calculette/"+parseFloat(5)+";"+"+"+";"+parseFloat(5)
   	console.log(urlEnvoye);  
    $.ajax({
    url: urlEnvoye,
    success: ifSuccess
});
});

function ifSuccess(result){
    console.log("Nous allons afficher le resultat du calcul");
    console.log("Résultat de la requête :", result);
    //Modification des champs pas jquery
	$("#modifAjax").text("Modification du champ par ajax : " + $("#msgParAjax").val() + " " + $("#msg2ParAjax").val());
	$("#resultatParAjax").val( $("#msg2ParAjax").val());


}


console.log("Au revoir");
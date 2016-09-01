/*
 A função Mascara tera como valores no argumento os dados inseridos no input (ou no evento onkeypress)
 onkeypress="mascara(this, '## ####-####')"
 onkeypress = chama uma função quando uma tecla é pressionada, no exemplo acima, chama a função mascara e define os valores do argumento na função
 O primeiro valor é o this, é o Apontador/Indicador da Mascara, o '## ####-####' é o modelo / formato da mascara
 no exemplo acima o # indica os números, e o - (hifen) o caracter que será inserido entre os números, ou seja, no exemplo acima o telefone ficara assim: 11-4000-3562
 para o celular de são paulo o modelo deverá ser assim: '## #####-####' [11 98563-1254]
 para o RG '##.###.###.# [40.123.456.7]
 para o CPF '###.###.###.##' [789.456.123.10]
 Ou seja esta mascara tem como objetivo inserir o hifen ou espaço automáticamente quando o usuário inserir o número do celular, cpf, rg, etc

 lembrando que o hifen ou qualquer outro caracter é contado tambem, como: 11-4561-6543 temos 10 números e 2 hifens, por isso o valor de maxlength será 12
 <input type="text" name="telefone" onkeypress="mascara(this, '## ####-####')" maxlength="12">
 neste código não é possivel inserir () ou [], apenas . (ponto), - (hifén) ou espaço
 */

 function mascara(t, mask){
     var i = t.value.length;
     var saida = mask.substring(1,0);
     var texto = mask.substring(i)
     if (texto.substring(0,1) != saida){
         t.value += texto.substring(0,1);
     }
 }

 /*
 function makeDate(id){
     obj = document.getElementById(id);
     vl = obj.value;
     l = vl.toString().length;
     switch(l){
         case 2:
             obj.value = vl + "/";
         break;
         case 5:
             obj.value = vl + "/";
         break;
     }
 }
 */

 function busca(pos) {
   // Declare variables
   var input, filter, table, tr, td, i;
   input = document.getElementById("myInput");
   filter = input.value.toUpperCase();
   table = document.getElementById("myTable");
   tr = table.getElementsByTagName("tr");

   // Loop through all table rows, and hide those who don't match the search query
   for (i = 0; i < tr.length; i++) {
     td = tr[i].getElementsByTagName("td")[pos];
     if (td) {
       if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
         tr[i].style.display = "";
       } else {
         tr[i].style.display = "none";
       }
     }
   }
 }

  function buscaCheckbox(campo) {
    // Declare variables
    var input, filter, table, tr, td, i;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById(campo);
    li = table.getElementsByTagName("li");

    // Loop through all table rows, and hide those who don't match the search query
    for (i = 0; i < li.length; i++) {
      label = li[i].getElementsByTagName("label");
      if (label) {
        valor = label[0].innerText.toUpperCase();
        if (valor.indexOf(filter) > -1) {
          li[i].style.display = "";
        } else {
          li[i].style.display = "none";
        }
      }
    }
  }

 function ativoInativo(){
     var valor;
     var params = window.location.search.substr(1).split('&');

     document.getElementById("t").checked = true;
     for (var i = 0; i < params.length; i++) {
       var p=params[i].split('=');
       if (p[0] == "filtro") {
         valor = decodeURIComponent(p[1]);
         if (valor == "ativo"){
             document.getElementById("a").checked = true;
         }
         else{
             if (valor == "inativo"){
                 document.getElementById("i").checked = true;
             }
         }
       }
     }
 }
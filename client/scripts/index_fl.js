function update(p=""){
        if (p==""){
        const imie = document.getElementById('imieupd');
        const nazwisko = document.getElementById('nazwiskoupd');
        const pesel = document.getElementById('peselupd');
        const stanowisko = document.getElementById('stanowiskoupd');
        const dataUrodzenia = document.getElementById('data_urodzeniaupd');
        const dataZatrudnienia = document.getElementById('data_zatrudnieniaupd');
    var url = 'http://127.0.0.1:5000/person'
    if (pesel.value.trim() !== ''){
       url+=('?pesel='+ pesel.value.trim());
        if (imie.value.trim() !== '') url+=('&imie='+ imie.value.trim());
        if (nazwisko.value.trim() !== '') url+=('&nazwisko='+ nazwisko.value.trim());
        
        if (stanowisko.value.trim() !== '') url+=('&stanowisko='+ stanowisko.value.trim());
        if (dataUrodzenia.value !== '') url+=('&data_urodzenia='+ dataUrodzenia.value);
        if (dataZatrudnienia.value !== '') url+=('&data_zatrudnienia='+ dataZatrudnienia.value);
    }
    } 
    else{
        const imie = document.getElementById('uname');
        const nazwisko = document.getElementById('usurname');
        const stanowisko = document.getElementById('ujob');
        const dataUrodzenia = document.getElementById('udob');
        const dataZatrudnienia = document.getElementById('uhired');
    var url = 'http://127.0.0.1:5000/person'
    console.log(p)
       url+='?pesel='+p.toString();
        if (imie.value.trim() !== '') url+=('&imie='+ imie.value.trim());
        if (nazwisko.value.trim() !== '') url+=('&nazwisko='+ nazwisko.value.trim());
        
        if (stanowisko.value.trim() !== '') url+=('&stanowisko='+ stanowisko.value.trim());
        if (dataUrodzenia.value !== '') url+=('&data_urodzenia='+ dataUrodzenia.value);
        if (dataZatrudnienia.value !== '') url+=('&data_zatrudnienia='+ dataZatrudnienia.value);
    
    }
            console.log(url);  
            fetch(url, {method:'PATCH'})
                //.then(response=>response.json())
                
                .then(response => response.json())
                .then(data => {
  updresponse.innerHTML = 'Person updated:'+data
})
.then(() => getallpersons())
     }
        


        function getallpersons(edit = ""){
            res="<table><tr>"
            res+="<th>lp.</th>"
            res+="<th>Imie</th>"
            res+="<th>Nazwisko</th>"
            res+="<th>Stanowisko</th>"
            res+="<th>Pesel</th>"
            res+="<th>Data Urodzenia</th>"
            res+="<th>Data Zatrudnienia</th>"
            res+="<th>Usuń</th>"
            res+="<th>Edytuj</th>"


            res+="</tr>"
            fetch("http://127.0.0.1:5000/persons")
                .then(response=>response.json())
                .then(response=>{
                console.log(response)
                let i=0
                    for (const person of response){
                        res+="<tr>"
                            if(edit!=person["pesel"]){
                            res+="<th>"+(++i)+"</th>"
                            res+="<td>"+person["imie"]+"</td>"
                            res+="<td>"+person["nazwisko"]+"</td>"
                            res+="<td>"+person["stanowisko"]+"</td>"
                            res+="<td>"+person["pesel"]+"</td>"
                            res+="<td>"+person["data_urodzenia"].substring(0, 10)+"</td>"
                            res+="<td>"+person["data_zatrudnienia"].substring(0, 10)+"</td>"
                            res+="<td><button onclick='deleteperson("+person.pesel+")'>X</button></td>"
                            res+="<td><button onclick='getallpersons("+person.pesel+")'>/</button></td>"
                            }
                            else{
                                res+="<th>"+(++i)+"</th>"
                            res+="<td><input type='text' value='"+person["imie"]+"' id='uname'></td>"
                            res+="<td><input type='text' value='"+person["nazwisko"]+"' id='usurname'></td>"
                        res+="<td><input type='text' value='"+person["stanowisko"]+"' id='ujob'></td>"
                            
                            res+="<td>"+person["pesel"]+"</td>"
                             res+="<td><input type='date' value='"+person["data_urodzenia"].substring(0, 10)+"' id='udob'></td>"
                              res+="<td><input type='date' value='"+person["data_zatrudnienia"].substring(0, 10)+"' id='uhired'></td>"

                            res+="<td>-</td>"
                            res+="<td><button onclick='update("+person.pesel+")'>OK</button></td>"
                            }
                        res+="</tr>"
                    }
                    
                    res+="</table>" 
                getallresponse.innerHTML = res
        })
    }
    getallpersons()
    function deleteperson(pesel){
            if(confirm("remove person with pesel "+pesel+"?")){

            a="http://127.0.0.1:5000/person?pesel="+pesel
            console.log(a)
                fetch(a, {method:'DELETE'})
                //.then(response=>response.json())
                .then(() => getallpersons())
            }
    }
    function getCookie(name) {
                return document.cookie
                .split('; ')
                .find(row => row.startsWith(name + '='))
                ?.split('=')[1];
            }
           if (getCookie("darkmode") === "true") {
        document.body.setAttribute("class", "darkmode");
    }
           function show(name) {
                const divs = document.querySelectorAll("div");
                divs.forEach(div => {
                div.style.display = "none";
            });
            document.querySelector(name).style.display = "block";
            }
            color.onclick=()=>{
                if(document.body.getAttribute("class")=="darkmode"){
                    document.body.setAttribute("class", "") 
                    document.cookie = "darkmode=false"
                }
                else{
                    document.body.setAttribute("class", "darkmode") 
                    document.cookie = "darkmode=true"
                }
                           
            }
                    add.onclick=()=>{
        fetch('http://127.0.0.1:5000/person', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    imie: imie.value,
    nazwisko: nazwisko.value,
    pesel: pesel.value,
    stanowisko: stanowisko.value,
    data_urodzenia: data_urodzenia.value,
    data_zatrudnienia: data_zatrudnienia.value
  })
})
.then(response => response.json())
.then(data => {
  addresponse.innerHTML = 'Person added:'+data
})
.then(() => getallpersons())
.catch(error => {
  console.error('Error:', error);
});

        }
get1.onclick=()=>{
            
            a="http://127.0.0.1:5000/person?pesel="+getpesel.value
            console.log(a)
                fetch(a)
                .then(response=>response.json())
                .then(response=>{
                    res="<table>"
                console.log(response)
                   if (response!=null){
                        res+="<tr>"
                            for(const key in response){
                                if (response.hasOwnProperty(key)) {
                                res+="<td>"+response[key]+"</td>"
                                }
                            }
                        res+="</tr>"
                    
                    res+="</table>" 
                get1response.innerHTML = res}
                else{
                    get1response.innerHTML = "person not found"
                }

                })
        }
         del.onclick=()=>{
            a="http://127.0.0.1:5000/person?pesel="+delpesel.value
            console.log(a)
                fetch(a, {method:'DELETE'})
                //.then(response=>response.json())
                
                .then(response => response.json())
                .then(data => {
  delresponse.innerHTML = 'Person deleted:'+data
})
.then(() => getallpersons())
     }
      show("#addperson")
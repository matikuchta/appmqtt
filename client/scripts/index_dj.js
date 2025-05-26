
         function getpersonid(pesel){
        return fetch("http://127.0.0.1:8000/person/pesel/"+pesel, {
             method: "GET",
    headers: {
      "Authorization": "Token eeb754bf3c0696c9f785e82c54c9721995c3825b",
      "Content-Type": "application/json"
    }
        })
                .then(response=>response.json())
                .then(response=>{
                    console.log(response);
                return response["id"]})
     }
     jobs={}
        fetch("http://127.0.0.1:8000/jobs/")
                .then(response=>response.json())
                .then(response=>{
                    jobdict={}
                    response.forEach(e => {
                        jobdict[e["id"]]=e["nazwa"]
                    });
                    console.log(jobdict)
                    jobs = jobdict
                    
        stanowisko.innerHTML = "";
        console.log(jobs)
        for (const id in jobs) {
            const name = jobs[id];
            stanowisko.innerHTML += `<option value="${id}">${name}</option>`;
            stanowiskoupd.innerHTML = stanowisko.innerHTML
        }
                    
            })
    function getjob(id){
        return jobs[id]
    }



        function update(p = "") {
    let peselValue;
    let updatedData = {};

    if (p === "") {
        // Edycja z formularza górnego (np. osobna sekcja aktualizacji)
        const imie = document.getElementById('imieupd');
        const nazwisko = document.getElementById('nazwiskoupd');
        const pesel = document.getElementById('peselupd');
        const stanowisko = document.getElementById('stanowiskoupd');
        const dataUrodzenia = document.getElementById('data_urodzeniaupd');
        const dataZatrudnienia = document.getElementById('data_zatrudnieniaupd');

        peselValue = pesel.value.trim();
        if (peselValue === "") {
            alert("PESEL jest wymagany.");
            return;
        }

 updatedData = {};
if(imie.value.trim() !== '') updatedData.imie = imie.value.trim();
if(nazwisko.value.trim() !== '') updatedData.nazwisko = nazwisko.value.trim();
if(stanowisko.value.trim() !== '') updatedData.stanowisko = stanowisko.value.trim();
if(dataUrodzenia.value !== '') updatedData.data_urodzenia = dataUrodzenia.value;
if(dataZatrudnienia.value !== '') updatedData.data_zatrudnienia = dataZatrudnienia.value;

    } else {
        // Edycja z tabeli (kliknięcie na / przy osobie)
        const imie = document.getElementById('uname');
        const nazwisko = document.getElementById('usurname');
        const stanowisko = document.getElementById('ujob');
        const dataUrodzenia = document.getElementById('udob');
        const dataZatrudnienia = document.getElementById('uhired');

        peselValue = p.toString();

        updatedData = {
            imie: imie.value.trim(),
            nazwisko: nazwisko.value.trim(),
            stanowisko: stanowisko.value.trim(),
            data_urodzenia: dataUrodzenia.value,
            data_zatrudnienia: dataZatrudnienia.value
        };
    }

    // Uzyskanie ID po PESELu, potem wysłanie PATCH
    getpersonid(peselValue)
        .then(id => {
            if (!id) {
                throw new Error("Nie znaleziono osoby o podanym PESELu.");
            }
            console.log(updatedData)
            const url = `http://127.0.0.1:8000/persons/${id}/`;
            console.log(url)
            return fetch(url, {
                method: 'PATCH',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Token eeb754bf3c0696c9f785e82c54c9721995c3825b'
                },
                body: JSON.stringify(updatedData)
            });
        })
        .then(response => {
            if (!response.ok) {
                return response.text().then(text => { throw new Error(text); });
            }
            return response.json();
        })
        .then(data => {
            console.log("Zaktualizowano:", data);
            //alert("Dane zostały zaktualizowane.");
            getallpersons();
        })
        .catch(error => {
            console.error("Błąd:", error.message);
            //alert("Błąd aktualizacji: " + error.message);
        });
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
            fetch("http://127.0.0.1:8000/persons")
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
                            res+="<td>"+getjob(person["stanowisko"])+"</td>"
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
                            res+="<td><select value='"+person["stanowisko"]+"' id='ujob'>"+stanowisko.innerHTML+"</select></td>"
                            
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
            add.onclick = () => {
         let data = new Date()
         data = data.toISOString().split('T')[0]
    fetch('http://127.0.0.1:8000/persons/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Token eeb754bf3c0696c9f785e82c54c9721995c3825b'
        },
        body: JSON.stringify({
            imie: imie.value,
            nazwisko: nazwisko.value,
            pesel: pesel.value,
            stanowisko: stanowisko.value,
            data_urodzenia: data_urodzenia.value,
            data_zatrudnienia: data_zatrudnienia.value,
            data_utworzenia: data,
            data_modyfikacji: data
        })
    })
    .then(response => {
        console.log(response)
        if (!response.ok) {
            addresponse.innerHTML= "Błąd: nie dodano osoby"
            return response.text();  // Jeśli odpowiedź ma błąd, nie próbujemy jej parsować jako JSON
        }
        response.json();  // Jeśli odpowiedź jest poprawna, parsujemy ją jako JSON
        console.log('Osoba dodana:', response);  // Możesz sprawdzić dane odpowiedzi
        addresponse.innerHTML= "Sukces: dodano osobę"
        return getallpersons();  // Zaktualizowanie listy osób po dodaniu nowej
    })

    .catch(error => {
        console.error('Błąd:', error);  // Obsługa błędów
    });
};
get1.onclick=()=>{
            
            a="http://127.0.0.1:8000/person/pesel/"+getpesel.value
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
         del.onclick = () => {
    getpersonid(delpesel.value)
        .then(res => {
            let id = res;  // Zmienna id z odpowiedzi
            console.log(id)
            let a = "http://127.0.0.1:8000/persons/" + id+"/";  // Budowanie URL

            console.log(a);  // Możesz sprawdzić wynik URL w konsoli

            // Wykonaj zapytanie DELETE
            return fetch(a, { method: 'DELETE' , headers:{'Authorization': 'Token eeb754bf3c0696c9f785e82c54c9721995c3825b'}});
        })
        .then(() => getallpersons())  // Po usunięciu, zaktualizuj listę osób
        
};
function deleteperson(pesel){
    getpersonid(pesel)
        .then(res => {
            let id = res;  // Zmienna id z odpowiedzi
            console.log(id)
            let a = "http://127.0.0.1:8000/persons/" + id+"/";  // Budowanie URL

            console.log(a);  // Możesz sprawdzić wynik URL w konsoli

            // Wykonaj zapytanie DELETE
            if(confirm(`usunąć osobę z peselem :${pesel}?`)){
            return fetch(a, { method: 'DELETE', headers:{'Authorization': 'Token eeb754bf3c0696c9f785e82c54c9721995c3825b'} });
            }
            
        })
        .then(() => getallpersons())  // Po usunięciu, zaktualizuj listę osób
        
};

     show("#addperson")
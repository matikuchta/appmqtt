let config = {
  server: "http://127.0.0.1",
  port: "8000"
}
let path = config.server + ":" + config.port

var token = localStorage.getItem('access_token');
 function refreshAccessToken() {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) {
    return Promise.reject('No refresh token found');
  }

  return fetch(path+'/api/token/refresh/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ refresh: refreshToken })
  })
  .then(response => response.json().then(data => ({ status: response.status, body: data })))
  .then(({ status, body }) => {
    if (status === 200) {
    
      localStorage.setItem('access_token', body.access);
      token = body.access
      console.log('Access token refreshed!');
      return body.access; 
    } else {
      console.error('Failed to refresh token:', body);
      return Promise.reject(body);
    }
  })
  .catch(error => {
    console.error('Refresh token error:', error);
    return Promise.reject(error);
  });
}
refreshAccessToken()

         function getpersonid(pesel){
        return fetch(path+"/person/pesel/"+pesel, {
             method: "GET",
    headers: {
      "Authorization": 'Bearer ' + token,
      "Content-Type": "application/json"
    }
        })
                .then(response=>response.json())
                .then(response=>{
                    console.log(response);
                return response["id"]})
     }
     jobs={}
        fetch(path+"/jobs/")
                .then(response=>response.json())
                .then(response=>{
                    jobdict={}
                    response.forEach(e => {
                        jobdict[e["id"]]=e["nazwa"]
                    });
                    //console.log(jobdict)
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
                    'Authorization': 'Bearer ' + token
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
            fetch(path+"/persons", {headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + token
                },})
                .then(response => {
                    if (response.status === 403) {
                    throw new Error("Access denied");
                }
                    if (!response.ok) {
                        throw response; 
                    }
                    return response.json(); })
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
        .catch(error=>{
            console.error("error: "+error)
            getallresponse.innerHTML=error
        })
    }
    refreshAccessToken()
    .then(getallpersons())
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
    fetch(path+'/persons/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + token
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
            
            a=path+"/person/pesel/"+getpesel.value
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
            let a = path+"/persons/" + id+"/";  // Budowanie URL

            console.log(a);  // Możesz sprawdzić wynik URL w konsoli

            // Wykonaj zapytanie DELETE
            return fetch(a, { method: 'DELETE' , headers:{'Authorization': 'Bearer ' + token}});
        })
        .then(() => getallpersons())  // Po usunięciu, zaktualizuj listę osób
        
};
function deleteperson(pesel){
    getpersonid(pesel)
        .then(res => {
            let id = res;  // Zmienna id z odpowiedzi
            console.log(id)
            let a = path+"/persons/" + id+"/";  // Budowanie URL

            console.log(a);  // Możesz sprawdzić wynik URL w konsoli

            // Wykonaj zapytanie DELETE
            if(confirm(`usunąć osobę z peselem :${pesel}?`)){
            return fetch(a, { method: 'DELETE', headers:{'Authorization': 'Bearer ' + token} });
            }
            
        })
        .then(() => getallpersons())  // Po usunięciu, zaktualizuj listę osób
        
};
loginbtn.onclick=()=>{
    const uname = username.value;
    const pass = password.value;

    fetch(path+'/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'username':uname, 'password':pass })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
      if (status === 200) {
        localStorage.setItem('access_token', body.access);
        localStorage.setItem('refresh_token', body.refresh);
        loginresponse.innerHTML = ("Login successful!");
        loginmenubtn.style.display = "none"
        logout.style.display = "block"
        refreshAccessToken()
        .then(() => getallpersons())
        setTimeout(() => {
show("#addperson")
}, 2000);
        
      } else {
        loginresponse.innerHTML = ("Login failed: " + (body.detail || 'Unknown error'));
      }
    })
    .catch(error => {
      console.error('Login error:', error);
      loginresponse.innerHTML = ("Something went wrong. Check the console.");
    });
}
regbtn.onclick=()=>{
    const uname = regname.value;
    const pass = regpass.value;
    const mail = regmail.value;
    fetch(path+"/users/", {
        method: "POST",
        headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'username':uname, 'password':pass, 'email':mail})

    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
      if (status === 201) {
        signupresponse.innerHTML = ("Sign up successful!");

        fetch(path+'/api/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ 'username':uname, 'password':pass })
    })
    .then(response => response.json().then(data => ({ status: response.status, body: data })))
    .then(({ status, body }) => {
      if (status === 200) {
        localStorage.setItem('access_token', body.access);
        localStorage.setItem('refresh_token', body.refresh);
        signupresponse.innerHTML += ("<br>Login successful!");
        loginmenubtn.style.display = "none"
        logout.style.display = "block"
        refreshAccessToken()
        .then(() => getallpersons())
         setTimeout(() => {
show("#addperson")
}, 2000);

      } else {
        signupresponse.innerHTML += ("<br>Login failed: " + (body.detail || 'Unknown error'));
      }
    })
      } else {
        signupresponse.innerHTML = ("Sign up failed: " + (body.detail || 'Unknown error'));
      }
    })
    .catch(error => {
      console.error('Login error:', error);
      signupresponse.innerHTML = ("Something went wrong. Check the console.");
    });

}
logout.onclick=()=>{
    localStorage.removeItem("access_token")
    localStorage.removeItem("refresh_token")
    loginmenubtn.style.display = "block"
    logout.style.display = "none"
    loginresponse.innerHTML = ("");
    signupresponse.innerHTML = ("");
    token = null
}
if(localStorage.getItem("access_token")!=null){
            loginmenubtn.style.display = "none"
        logout.style.display = "block"
        show("#addperson")
}
else show("#login")

function sendPasswordResetEmail() {
  const email = document.getElementById('resetEmail').value.trim();
  const resetResponse = document.getElementById('resetResponse');

  if (!email) {
    resetResponse.innerText = 'Proszę wpisać adres e-mail.';
    return;
  }

  fetch(path+'/auth/users/reset_password/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ email: email })
  })
  .then(response => {
    if (response.status === 204) {
      resetResponse.innerText = 'E-mail do resetu hasła został wysłany, sprawdź swoją skrzynkę.';
    } else {
      return response.json().then(data => {
        resetResponse.innerText = data.email ? data.email.join(' ') : 'Coś poszło nie tak.';
      });
    }
  })
  .catch(error => {
    resetResponse.innerText = 'Błąd połączenia z serwerem.';
    console.error(error);
  });
}


    
chrome.runtime.onInstalled.addListener(function () {
    // Kada se ekstenzija instalira, pokreni autentifikaciju
    fetch('http://localhost:8000/api/user/token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'user@example.com',
        password: 'string'  // Korisnički podaci (ili neka druga autentifikacija)
      })
    })
    .then(response => response.json())
    .then(data => {
      // Sačuvaj token u chrome.storage
      chrome.storage.local.set({ auth_token: data.token }, function() {
        console.log("Token saved");
      });
    })
    .catch(error => console.log('Login failed:', error));
  });
  
  // Kreiraj context menu za selektovani tekst
  chrome.contextMenus.create({
    title: "Save as Task", // Ovo je tekst koji će biti prikazan u desnom meniju
    contexts: ["selection"], // Ova opcija će biti dostupna samo kada selektujete tekst
    onclick: function (info, tab) {
      // Uzmi selektovani tekst
      const taskText = info.selectionText;
  
      // Proveri da li je tekst selektovan
      if (taskText) {
        // Dobij autentifikacijski token sa chrome storage
        chrome.storage.local.get('auth_token', function(result) {
          const authToken = result.auth_token;
  
          if (authToken) {
            // Pošaljite zadatak na backend
            fetch('http://localhost:8000/api/tasks/task/', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                'Authorization': 'Token ' + authToken // Koristimo token za autentifikaciju
              },
              body: JSON.stringify({
                title: taskText // Tekst koji je selektovan na stranici
              })
            })
            .then(response => response.json())
            .then(data => {
              console.log("Task created successfully", data); // Logovanje uspeha
            })
            .catch(error => {
              console.error("Error creating task:", error); // Logovanje greške
            });
          } else {
            console.log("User is not authenticated.");
          }
        });
      } else {
        console.log("No text selected!");
      }
    }
  });
  
document.addEventListener('DOMContentLoaded', function () {
  // Sada kada je DOM učitan, možemo bezbedno da dodamo event listener
  document.getElementById('save-task').addEventListener('click', function () {
    // Prvo uzmi selektovani tekst na stranici
    chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
      // Uzmi selektovani tekst sa stranice
      chrome.tabs.executeScript(tabs[0].id, {
        code: "window.getSelection().toString();"
      }, function(selection) {
        const taskText = selection[0];  // selektovani tekst

        if (taskText) {
          chrome.storage.local.get('auth_token', function(result) {
            const authToken = result.auth_token;

            if (authToken) {
              fetch('http://localhost:8000/api/tasks/task/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Authorization': 'Token ' + authToken
                },
                body: JSON.stringify({
                  title: taskText
                })
              })
              .then(response => response.json())
              .then(data => {
                console.log("Task created successfully", data);
                // Prikazivanje zelene poruke o uspehu
                const message = document.getElementById('message');
                message.style.color = '#4CAF50'; // Zelena boja
                message.textContent = "Task added successfully!";
                message.style.display = 'block'; // Prikazivanje poruke
                setTimeout(function() {
                  message.style.display = 'none'; // Sakrij poruku nakon 5 sekundi
                }, 5000);
              })
              .catch(error => {
                console.error("Error creating task:", error);
                // Prikazivanje crvene poruke o grešci
                const message = document.getElementById('message');
                message.style.color = '#ff5722'; // Crvena boja
                message.textContent = "Failed to create task!";
                message.style.display = 'block'; // Prikazivanje poruke
                setTimeout(function() {
                  message.style.display = 'none'; // Sakrij poruku nakon 5 sekundi
                }, 5000);
              });
            }
          });
        } else {
          console.log("No text selected!");
        }
      });
    });
  });
});

const loggedUser = document.querySelector(".loggedUser");
    auth.onAuthStateChanged(user => {
    if (user)
     {
        fs.collection('users').doc(user.uid).get().then((snapshot) => {
            loggedUser.innerText = snapshot.data().Name;
        })
    }
    else {
        console.log('user is not signedIn...');
    }
})

let result = [];

auth.onAuthStateChanged(user => {
    // ... retrieve data from Firestore ...
    if (user){
        snapshot.forEach(doc => {
            // ... insert rows and cells into the HTML table ...

            // get the percentage value from the HTML table
            let percentage = doc.data().percentage;

            // add the percentage value to the result array
            result.push(percentage);
                // log the length of the result array
            console.log("Number of percentage values:", result.length);

            // log the result array to the console
            console.log("Percentage values:", result);
        });

    }


});
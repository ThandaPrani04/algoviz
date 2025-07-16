document.getElementById("generate").addEventListener("click", () => {
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        let url = tabs[0].url;
        console.log("Original URL:", url);

        // Remove `/description` and trailing slashes
        url = url.replace(/\/description\/?$/, "");  
        url = url.replace(/\/$/, "");  

        console.log("Normalized URL:", url);

        fetch("http://localhost:5000/generate", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url })
        })
        .then(res => res.json())
        .then(data => {
            document.getElementById("status").innerText = data.message;
        })
        .catch(err => {
            document.getElementById("status").innerText = "❌ Error: " + err.message;
        });
    });
});

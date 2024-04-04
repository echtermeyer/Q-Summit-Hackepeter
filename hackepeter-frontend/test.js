fetch("http://127.0.0.1:8000/converse/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    "science": "Sample Item",
    "sources": ["https://www.example.com"],
    "history": [{"user": "hi"}, {"model": "fuck you"}, {"user": "fuck you too"}]
  })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));

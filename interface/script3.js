
async function fetchText() {
    // Get the input value
   // const searchButton = document.getElementById('searchButton'); // No need to get the button here
   var x = document.getElementById("mySearch");
   var defaultVal = x.defaultValue;
   var searchInput = x.value;
   // Set up the headers and options for the fetch request
   var myHeaders = new Headers();
   myHeaders.append("Content-Type", "application/json");

   var requestOptions = {
       method: 'POST',
       headers: myHeaders,
       redirect: 'follow',
       mode:'cors'
   };

   try {
       // Use a try-catch block to handle errors during the fetch
       let response = await fetch("http://localhost:9200/flickrdata/_search?q=" + searchInput, requestOptions);

       console.log(response.status); // Check the response status
       console.log(response.statusText); // Check the response statusText

       if (response.status === 200) {
           let data = await response.json();
           let images = [];
           for (let hit of data.hits.hits) { // Add "let" to define the variable
               let image_index = hit["_source"];
               let flickr_farm = image_index["flickr_farm"];
               let flickr_server = image_index["flickr_server"];
               let id = image_index["id"];
               let flickr_secret = image_index["flickr_secret"];
               let url = "https://farm" + flickr_farm + ".staticflickr.com/" + flickr_server + "/" + id + "_" + flickr_secret + ".jpg";
               images.push(url);
           }
           return images ;
          
       } else {
           console.error('Error:', response.statusText);
       }
   } catch (error) {
       console.error('Error:', error);
   }
}
async function fetchImage() {
    // Get the input value
   // const searchButton = document.getElementById('searchButton'); // No need to get the button here
   
   var x = document.getElementById("mySearch");
   var defaultVal = x.defaultValue;
   var searchInput = x.value;
   
   var requestOptions = {
     method: 'POST',
     body: formData,
     redirect: 'follow',
   };

   try {
       // Use a try-catch block to handle errors during the fetch
       let response = await fetch("http://localhost:5000/upload", requestOptions);

       console.log(response.status); // Check the response status
       console.log(response.statusText); // Check the response statusText

       if (response.status === 200) {
           let data = await response.json();
           let images = [];
           for (let result of data.result) { 
               let url =result["fields"]["url"][0];
               images.push(url);
           }
           
           return images ;
           
       } else {
           console.error('Error:', response.statusText);
       }
   } catch (error) {
       console.error('Error:', error);
   }
}

async  function renderImages() {
    
    const container = document.getElementById('imageContainer');
    container.innerHTML = ''; // Clear previous images
    var x = document.getElementById("mySearch");
    
   let imageUrls
   if(x && !formData){
    imageUrls=await fetchText();
  
}else if( formData && x.value==x.defaultValue ){
      imageUrls=await fetchImage();
     
}
else if( formData && x.value!=x.defaultValue ){
const array1 = await fetchText();
const array2 = await fetchImage();

imageUrls = array1.filter(value => array2.includes(value));
console.log(imageUrls)
console.log(array1)
console.log(array2)



//imageUrls = array1.filter(value => array2.includes(value));

}

imageUrls.forEach((imageUrl) => {
    const img = document.createElement('img');
    img.src = imageUrl;
    container.appendChild(img);
});

 imageUrls=[]
}
var formData ;
document.getElementById('files').addEventListener('change', function(event) {
    formData = new FormData()
    const selectedFile = event.target.files[0];
    formData.append('photo', selectedFile);
    console.log(formData)

  });
const searchButton = document.getElementById('searchButton');
searchButton.addEventListener('click', renderImages);

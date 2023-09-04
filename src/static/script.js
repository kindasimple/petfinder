// const apiUrl = "https://api.petfinder.com/v2/types/dog/breeds?exclude_breeds=26,23";
const apiUrl = "http://127.0.0.1:8000/";

// const url = `${apiUrl}animals?type=dog&breed=${breed.id}&location=YOUR_LOCATION&limit=3`;
const disalloweds = [
    "Boxer",
    "Boston Terrier",
    "Pit Bull Terrier",
    "American Bulldog",
    "Husky",
    "Affenpinscher",
    "Alaskan Malamute",
    "Akita",
    "American Bully",
    "Chihuahua",
    "Border Terrier",
    "Bichon Frise",
    "Cairn Terrier",
    "Cane Corso",
    "Cavalier King Charles Spaniel",
    "Cocker Spaniel",
    "Dachshund",
    "English Bulldog",
    "French Bulldog",
    "Brussels Griffon",
    "Bull Terrier",
    "Greyhound",
    "Jack Russell Terrier",
    "Lhasa Apso",
    "Maltese",
    "Mastiff",
    "Miniature Pinscher",
    "Miniature Poodle",
    "Norfolk Terrier",
    "Norwich Terrier",
    "Pomeranian",
    "Poodle",
    "Rat Terrier",
    "Rottweiler",
    "Shih Tzu",
    "Smooth Fox Terrier",
    "Saint Bernard",
    "Standard Poodle",
    "Staffordshire Bull Terrier",
    "Terrier",
    "Toy Fox Terrier",
    "Welsh Terrier",
    "Yorkshire Terrier"
]

// Define the mapping of dog breeds to IDs
const breedIds = {
    "Affenpinscher": 424,
    "Afghan Hound": 2,
    "Airedale Terrier": 3,
    "Akita": 4,
    "Alaskan Klee Kai": 428,
    "Alaskan Malamute": 5,
    "American Bulldog": 6,
    "American Eskimo Dog": 7,
    "American Foxhound": 8,
    "American Hairless Terrier": 429,
    "American Staffordshire Terrier": 9,
    "American Water Spaniel": 10,
    "Anatolian Shepherd Dog": 11,
    "Appenzeller Sennenhunde": 430,
    "Australian Cattle Dog / Blue Heeler": 12,
    "Australian Kelpie": 431,
    "Australian Shepherd": 13,
    "Australian Terrier": 14,
    "Basenji": 15,
    "Basset Hound": 16,
    "Beagle": 17,
    "Bearded Collie": 18,
    "Beauceron": 432,
    "Bedlington Terrier": 19,
    "Belgian Shepherd / Laekenois": 434,
    "Belgian Shepherd / Malinois": 20,
    "Belgian Shepherd / Sheepdog": 21,
    "Belgian Shepherd / Tervuren": 22,
    "Bernedoodle": 523,
    "Bernese Mountain Dog": 23,
    "Bichon Frise": 24,
    "Black and Tan Coonhound": 25,
    "Black Labrador Retriever": 435,
    "Black Mouth Cur": 436,
    "Black Russian Terrier": 26,
    "Bloodhound": 27,
    "Blue Lacy": 437,
    "Bluetick Coonhound": 28,
    "Boerboel": 438,
    "Bolognese": 439,
    "Border Collie": 29,
    "Border Terrier": 30,
    "Borzoi": 31,
    "Boston Terrier": 32,
    "Bouvier des Flandres": 33,
    "Boxer": 34,
    "Boykin Spaniel": 440,
    "Briard": 35,
    "Brittany Spaniel": 36,
    "Brussels Griffon": 37,
    "Bull Terrier": 38,
    "Bulldog": 39,
    "Bullmastiff": 40,
    "Cairn Terrier": 41,
    "Canaan Dog": 42,
    "Cane Corso Mastiff": 43,
    "Carolina Dog": 441,
    "Catahoula Leopard Dog": 44,
    "Cattle Dog": 445,
    "Caucasian Shepherd / Ovcharka": 442,
    "Cavachon": 523,
    "Cavalier King Charles Spaniel": 45,
    "Cavapoo": 523,
    "Chesapeake Bay Retriever": 46,
    "Chihuahua": 47,
    "Chinese Crested Dog": 48,
    "Chinese Foo Dog": 449,
    "Chinese Shar-Pei": 49,
    "Chinook": 450,
    "Chow Chow": 451,
    "Cirneco dell'Etna": 452,
    "Clumber Spaniel": 50,
    "Cockapoo": 523,
    "Cocker Spaniel": 51,
    "Collie": 52,
    "Coonhound": 453,
    "Corgi": 454,
    "Coton de Tulear": 55,
    "Curly-Coated Retriever": 56,
    "Dachshund": 57,
    "Dalmatian": 58,
    "Dandi Dinmont Terrier": 59,
    "Doberman Pinscher": 60,
    "Dogo Argentino": 457,
    "Dogue de Bordeaux": 61,
    "Dutch Shepherd": 461,
    "English Bulldog": 62,
    "English Cocker Spaniel": 63,
    "English Coonhound": 464,
    "English Foxhound": 65,
    "English Pointer": 66,
    "English Setter": 67,
    "English Shepherd": 68,
    "English Springer Spaniel": 69,
    "English Toy Spaniel": 70,
    "Entlebucher Mountain Dog": 463,
    "Eskimo Dog": 466,
    "Feist": 71,
    "Field Spaniel": 72,
    "Fila Brasileiro": 467,
    "Finnish Lapphund": 465,
    "Finnish Spitz": 73,
    "Flat-Coated Retriever": 74,
    "Fox Terrier": 75,
    "Foxhound": 469,
    "French Bulldog": 76,
    "Galgo Spanish Greyhound": 470,
    "German Pinscher": 79,
    "German Shepherd Dog": 80,
    "German Shorthaired Pointer": 81,
    "German Spitz": 471,
    "German Wirehaired Pointer": 82,
    "Giant Schnauzer": 83,
    "Glen of Imaal Terrier": 84,
    "Golden Retriever": 85,
    "Goldendoodle": 523,
    "Gordon Setter": 86,
    "Great Dane": 87,
    "Great Pyrenees": 88,
    "Greater Swiss Mountain Dog": 89,
    "Greyhound": 90,
    "Hamiltonstovare": 472,
    "Harrier": 91,
    "Havanese": 92,
    "Hound": 473,
    "Hovawart": 94,
    "Husky": 95,
    "Ibizan Hound": 96,
    "Icelandic Sheepdog": 474,
    "Irish Setter": 97,
    "Irish Terrier": 98,
    "Irish Water Spaniel": 99,
    "Irish Wolfhound": 100,
    "Italian Greyhound": 101,
    "Italian Spinone": 102,
    "Jack Russell Terrier": 103,
    "Jack Russell Terrier (Parson Russell Terrier)": 104,
    "Jindo": 475,
    "Kai Dog": 476,
    "Karelian Bear Dog": 105,
    "Keeshond": 106,
    "Kerry Blue Terrier": 107,
    "King Charles Spaniel": 108,
    "Kishu": 477,
    "Klee Kai": 478,
    "Komondor": 109,
    "Kuvasz": 110,
    "Kyrii": 479,
    "Labrador Retriever": 111,
    "Lacy Dog": 480,
    "Lakeland Terrier": 112,
    "Lancashire Heeler": 481,
    "Leonberger": 113,
    "Lhasa Apso": 114,
    "Löwchen": 115,
    "Maltese": 116,
    "Manchester Terrier": 117,
    "Maremma Sheepdog": 482,
    "Mastiff": 118,
    "McNab": 483,
    "Miniature Bull Terrier": 119,
    "Miniature Dachshund": 120,
    "Miniature Pinscher": 121,
    "Miniature Poodle": 122,
    "Miniature Schnauzer": 123,
    "Mixed Breed": 488,
    "Mountain Cur": 484,
    "Mountain Dog": 489,
    "Munsterlander": 125,
    "Neapolitan Mastiff": 126,
    "New Guinea Singing Dog": 491,
    "Newfoundland Dog": 127,
    "Norfolk Terrier": 128,
    "Norwegian Buhund": 129,
    "Norwegian Elkhound": 130,
    "Norwegian Lundehund": 492,
    "Norwich Terrier": 131,
    "Nova Scotia Duck Tolling Retriever": 132,
    "Old English Sheepdog": 133,
    "Otterhound": 134,
    "Papillon": 135,
    "Patterdale Terrier / Fell Terrier": 495,
    "Pekingese": 136,
    "Pembroke Welsh Corgi": 137,
    "Perro de Presa Canario": 496,
    "Peruvian Inca Orchid": 497,
    "Petit Basset Griffon Vendeen": 138,
    "Pharaoh Hound": 139,
    "Pit Bull Terrier": 140,
    "Plott Hound": 141,
    "Pointer": 142,
    "Polish Lowland Sheepdog": 143,
    "Pomeranian": 144,
    "Pomsky": 498,
    "Poodle": 145,
    "Portuguese Podengo": 499,
    "Portuguese Water Dog": 146,
    "Presa Canario": 500,
    "Pug": 147,
    "Puggle": 501,
    "Puli": 148,
    "Pumi": 149,
    "Pyrenean Mastiff": 502,
    "Pyrenean Mountain Dog": 150,
    "Pyrenean Shepherd": 151,
    "Rat Terrier": 152,
    "Redbone Coonhound": 153,
    "Rhodesian Ridgeback": 154,
    "Rottweiler": 155,
    "Rough Collie": 156,
    "Saint Bernard / St. Bernard": 157,
    "Saluki": 158,
    "Samoyed": 159,
    "Sarplaninac": 503,
    "Schipperke": 160,
    "Schnauzer": 161,
    "Schnoodle": 504,
    "Scottish Deerhound": 162,
    "Scottish Terrier Scottie": 163,
    "Sealyham Terrier": 164,
    "Shar Pei": 165,
    "Sheep Dog": 505,
    "Shelty Dog": 506,
    "Sheltie, Shetland Sheepdog": 166,
    "Shepherd": 508,
    "Shiba Inu": 167,
    "Shih Tzu": 168,
    "Siberian Husky": 169,
    "Silky Terrier": 170,
    "Skye Terrier": 171,
    "Sloughi": 509,
    "Smooth Collie": 172,
    "Smooth Fox Terrier": 173,
    "South Russian Ovtcharka": 510,
    "Spaniel": 513,
    "Spanish Mastiff": 511,
    "Spinone Italiano": 174,
    "Spitz": 512,
    "Staffordshire Bull Terrier": 175,
    "Standard Poodle": 176,
    "Standard Schnauzer": 177,
    "Sussex Spaniel": 178,
    "Swedish Vallhund": 179,
    "Tennessee Treeing Brindle": 515,
    "Terrier": 514,
    "Thai Ridgeback": 516,
    "Tibetan Mastiff": 181,
    "Tibetan Spaniel": 182,
    "Tibetan Terrier": 183,
    "Tosa Inu": 517,
    "Toy Fox Terrier": 184,
    "Toy Poodle": 185,
    "Treeing Tennessee Brindle": 518,
    "Treeing Walker Coonhound": 186,
    "Vizsla": 187,
    "Weimaraner": 188,
    "Welsh Corgi": 519,
    "Welsh Springer Spaniel": 190,
    "Welsh Terrier": 191,
    "West Highland White Terrier Westie": 192,
    "Wheaten Terrier": 193,
    "Whippet": 194,
    "White German Shepherd": 520,
    "Wire Fox Terrier": 195,
    "Wirehaired Dachshund": 196,
    "Wirehaired Pointing Griffon": 197,
    "Wirehaired Terrier": 521,
    "Xoloitzcuintle / Mexican Hairless": 198,
    "Yellow Labrador Retriever": 522,
    "Yorkshire Terrier Yorkie": 199
};

const disallowed_ids = disalloweds.map((item, index) => { return breedIds[item]; });
const urlParams = new URLSearchParams(window.location.search);
const includeBreeds = urlParams.get('include_breeds');
var url = `${apiUrl}types/dog/breeds?exclude_breeds=${encodeURIComponent(disalloweds)}`;
if (includeBreeds) {
    url += `&include_breeds=${encodeURIComponent(includeBreeds)}`
}
console.log(url)
fetch(url, {})
.then(response => response.json())
.then(data => {
  const breedsList = document.getElementById("breeds-list");
  const animalsList = document.getElementById("animals-list");

  data.breeds.forEach(breed => {
    // get animals for this breed
    const url = `${apiUrl}updates?type=dog&breed=${breed.name}&location=San Francisco, CA&limit=100`;
    fetch(url, {})
    .then(response => response.json())
    .then(data => {
      if (data.animals.length > 0) {
          const breedPanel = document.createElement("div");
        const breedHeading = document.createElement("h3");
        breedHeading.textContent = breed.name; // + " " + breed.id;
        breedPanel.appendChild(breedHeading);
        animalsList.appendChild(breedPanel);

        const breedList = document.createElement("ul");
        breedList.classList.add("horizontal-list");

        data.animals.forEach(animal => {
            const animalItem = document.createElement("li");
            const animalImage = document.createElement("img");
            // Add a link to the animal's page
            const animalLink = document.createElement("a");
            animalLink.href = animal.url;
            animalLink.target = "_blank";
            animalItem.appendChild(animalLink);

            animalImage.src = animal.photos.length > 0 ? animal.photos[0].medium : "placeholder.png";
            animalImage.alt = animal.name;
            animalLink.appendChild(animalImage);

            const animalName = document.createElement("span");
            animalName.classList.add("animal-name");
            animalName.textContent = animal.name;
            animalItem.appendChild(animalName);

            breedList.appendChild(animalItem);
        });

        breedPanel.appendChild(breedList);
        // Add breed to the breed list
        const breedItem = document.createElement("li");
        const breedLink = document.createElement("a");
        breedLink.href = `index.html?include_breeds=${breed.name}`;
        breedLink.textContent = breed.name;
        breedItem.appendChild(breedLink);
        breedsList.appendChild(breedItem);

    }
    })
    .catch(error => console.error(error));
  });
})
.catch(error => console.error(error));



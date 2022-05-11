// theta0 :
// c'est la constante ajouter (par exemple le prix minimum d'une voiture)
// theta1 :
// c'est le taux de progression qui va etre applique lors d'un tour de boucle.
// exemple : 10k euros par an de plus par année d'experience en entreprise : theta1=10k

// ===== Parsing data ===== //
const fs = require('fs');
let read = [];
try {
  read = fs.readFileSync('./data.csv', 'utf8').split('\n');
}
catch (err) {
  console.error('Error trying to read file : ', err);
}

let data = [];

read.forEach((value) => {
    const km = value.split(',')[0];
    const price = value.split(',')[1];
    if (km && price && parseInt(km) > 0)
      data.push({km, price})
});

data.sort((a, b) => {
  return a.km - b.km;
});

console.log(data);


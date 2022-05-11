let ctx = document.getElementById("graph").getContext('2d');

let data = [];
let dataPrint = [];

let theta0 = 0;
let theta1 = 0;

let m = undefined;
const ratioLearning = 0.1;

function prixEstime(kilométrage) {
    return theta0 + (theta1 * kilométrage);
}



async function getSVC(file) {
    let text = await file.text();
    text = text.split('\n');
    text.forEach((value) => {
        const km = value.split(',')[0];
        const price = value.split(',')[1];
        if (km && price && parseInt(km) > 0)
          data.push({km, price})
    });

    data.sort((a, b) => {
      return b.km - a.km;
    });

    dataPrint = data.map((value) => ({x: value.km, y: value.price}));

    m = data.length;

    console.log(dataPrint);
    
    launchGraph();

}

function getSumTheta0() {
    sum = 0;
    for (let i = 0 ; i < m ; i++)
        sum += prixEstime(kilométrage[i]) - prix[i];
    return sum;
}

function getSumTheta1() {
    sum = 0;
    for (let i = 0 ; i < m ; i++)
        sum += (prixEstime(kilométrage[i]) - prix[i]) * kilométrage[i];
    return sum;
}

function linearRegression() {

    some = get
    tmpTheta0 = ratioLearning * 1 / m * some;

}

function launchGraph() {

    return new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'X: Kilometers, Y: Price',
                showLine: true,
                data: dataPrint,
                backgroundColor: 'rgb(255, 99, 132)'
            }]
        },
        options: {
            scales: {
                x: {
                    type: 'linear',
                    position: 'bottom'
                }
            }
        }
    });

}
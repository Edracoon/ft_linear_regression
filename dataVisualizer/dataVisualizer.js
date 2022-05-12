let context1 = document.getElementById("graph1").getContext('2d');
let context2 = document.getElementById("graph2").getContext('2d');
let SVCfile = undefined;

const learningRate = 0.1;
let m = 0.0; // data length

let learningTime = 0;

let data = [];
let dataPrint = [];

let theta0 = 0;
let theta1 = 0;



async function getSVC(file) {
    console.log(file);
    if (data.length || SVCfile !== undefined || file.type !== "text/csv")
        return ;
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
    
    launchGraph();
}

function estimatePrice(kilometters, theta0, theta1) {
    return theta0 + (theta1 * kilometters);
}

function getSumTheta0(kilometters, prices, tmpTheta0, tmpTheta1) {
    sum = 0;
    for (let i = 0 ; i < data.length ; i++)
        sum += estimatePrice(kilometters[i], tmpTheta0, tmpTheta1) - prices[i];
    return sum;
}

function getSumTheta1(kilometters, prices, tmpTheta0, tmpTheta1) {
    sum = 0;
    for (let i = 0 ; i < data.length ; i++)
        sum += (estimatePrice(kilometters[i], tmpTheta0, tmpTheta1) - prices[i]) * kilometters[i];
    return sum;
}

function linearRegression() {
    if (!data.length) {
        console.log("linearRegression: Need data !");
        return ;
    }

    m = data.length;
    console.log("m", m);
    let kilometters = data.map((value) => parseInt(value.km));
    let prices = data.map((value) => parseInt(value.price));

    console.log(`====== learningTime[${++learningTime}] ======\n`);

    // Initialize tmp values
    let tmpTheta0 = theta0;
    let tmpTheta1 = theta1;
    console.log('prev theta0 -> ', theta0, '\nprev theta1 -> ', theta1);

    // Compute theta with tmp values
    let sum0 = getSumTheta0(kilometters, prices, theta0, theta1);
    let sum1 = getSumTheta1(kilometters, prices, theta0, theta1);
    tmpTheta0 = learningRate * (1.0 / m) * sum0;
    tmpTheta1 = learningRate * (1.0 / m) * sum1;

    // Update global theta
    theta0 = tmpTheta0;
    theta1 = tmpTheta1;

    console.log('computed theta0 -> ', tmpTheta0, '\ncomputed theta1 ->', tmpTheta1);

    // console.log(theta0, theta1)

    // return new Chart(context2, {
    //     type: 'scatter',
    //     data: {
    //         datasets: [{
    //             label: 'X: Kilometers, Y: Price',
    //             showLine: true,
    //             data: dataPrint,
    //             backgroundColor: 'rgb(255, 99, 132)'
    //         }]
    //     },
    //     options: {
    //         scales: {
    //             x: {
    //                 type: 'linear',
    //                 position: 'bottom'
    //             }
    //         }
    //     }
    // });
}

function launchGraph() {

    return new Chart(context1, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'X: Kilometers, Y: Price',
                showLine: true,
                data: dataPrint,
                backgroundColor: 'rgb(255, 0, 0)'
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
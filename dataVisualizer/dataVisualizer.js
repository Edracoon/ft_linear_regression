let context1 = document.getElementById("graph1").getContext('2d');
let context2 = document.getElementById("graph2").getContext('2d');
let SVCfile = undefined;

const learningRate = 0.1;

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

function estimatePrice(kilometters, paramTheta0, paramTheta1) {
    return (paramTheta1 * kilometters) + paramTheta0;
}

function getMSE1(kilometters, prices, paramTheta0, paramTheta1) {
    sosr = 0;
    for (let i = 0 ; i < data.length ; i++) {
        let residual = estimatePrice(kilometters[i], paramTheta0, paramTheta1) - prices[i];
        sosr += Math.pow(residual, 2); // Sum with power 2
    }
    return (sosr / data.length);
}

function getMSE2(kilometters, prices, tmpTheta0, tmpTheta1) {
    sosr = 0;
    for (let i = 0 ; i < data.length ; i++) {
        let residual = (estimatePrice(kilometters[i], tmpTheta0, tmpTheta1) - prices[i]) * kilometters[i];
        sosr += Math.pow(residual, 2); // Sum with power 2
    }
    return(sosr / data.length); // Faire la moyenne des résiduts
}

function linearRegression() {
    if (!data.length) {
        console.log("linearRegression: Need data !");
        return ;
    }
    let kilometters = data.map((value) => parseInt(value.km));
    let prices = data.map((value) => parseInt(value.price));

    console.log(`====== learningTime[${++learningTime}] ======\n`);

    // Initialize tmp values
    let tmpTheta0 = theta0;
    let tmpTheta1 = theta1;
    console.log('prev theta0 -> ', theta0, '\nprev theta1 -> ', theta1);

    // Compute MSE with previous theta values
    let MSE1 = getMSE1(kilometters, prices, theta0, theta1); // Sum Of Squared Residual divided by the length of the data
    let MSE2 = getMSE2(kilometters, prices, theta0, theta1); // Sum Of Squared Residual divided by the length of the data

    console.log('MSE1 -> ', Math.sqrt(MSE1), '\MSE2 -> ',  MSE2);

    //            ( 0.1 ?)
    tmpTheta0 = learningRate * Math.sqrt(MSE1);
    // Not working (insanely huge values going fast into Infinity)
    // tmpTheta1 = learningRate * Math.sqrt(MSE2);

    // Update global theta
    theta0 = tmpTheta0;
    theta1 = tmpTheta1;

    console.log('computed theta0 -> ', theta0, '\ncomputed theta1 ->', theta1);


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

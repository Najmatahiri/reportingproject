let list_couleur = ['green', 'red']


let nb_pathed_v6 = data.filter(machine => machine.os.startsWith("Redhat 6.") && machine.critical === 0).length;
let nb_pathed_v7 = data.filter(machine => machine.os.startsWith("Redhat 7.") && machine.critical === 0).length;
let nb_pathed_v8 = data.filter(machine => machine.os.startsWith("Redhat 8.") && machine.critical === 0).length;
let nb_pathed_v9 = data.filter(machine => machine.os.startsWith("Redhat 9.") && machine.critical === 0).length;
let nb_not_pathed_v6 = data.filter(machine => machine.os.startsWith("Redhat 6.") && machine.critical > 0).length;
let nb_not_pathed_v7 = data.filter(machine => machine.os.startsWith("Redhat 7.") && machine.critical > 0).length;
let nb_not_pathed_v8 = data.filter(machine => machine.os.startsWith("Redhat 8.") && machine.critical > 0).length;
let nb_not_pathed_v9 = data.filter(machine => machine.os.startsWith("Redhat 9.") && machine.critical > 0).length;

let tab_os_patded = []
let trace_patched = {
    x: ['RedHat 6',',RedHat 7', 'RedHat 8', 'RedHat 9'],
    y:  tab_os_patched,
    name: 'Patched',
    type: 'bar',
    marker: {
        color: 'green',
    }


};

let trace_not_patched = {
    x:  ['RedHat 6',',RedHat 7', 'RedHat 8', 'RedHat 9'],
    y:  tab_os_not_patched,
    name: 'Not Pathed',
    type: 'bar',
    marker: {
        color: 'red',
    }

};


let date_os = [trace_patched, trace_not_patched];

var layout_os = {
    scattermode: 'group',
    title: 'Patch selon les versions de RH',
    xaxis: {title: 'Version de RH'},
    yaxis: {title: 'Patch'},
    barcornerradius: 15,

};

let config = {displayModeBar: false, responsive: true}

Plotly.newPlot('graph-patch-os',date_os , layout_os, config);


var allLabels = ['Patched', 'Not Pathed'];

var allValues = [
    [80, 20],
    [60, 40],
    [140, 60],
];


var data = [{
    values: allValues[0],
    labels: allLabels,
    type: 'pie',
    name: 'PROD',
    hole: .6,
    marker: {
        colors: list_couleur
    },
    domain: {
        row: 0,
        column: 0
    },
    hoverinfo: 'label+percent+name',
 textinfo: 'percent'
}, {
    values: allValues[1],
    labels: allLabels,
    type: 'pie',
    name: 'HORS-PROD',
    hole: .6,
    marker: {
        colors: list_couleur
    },
    domain: {
        row: 0,
        column: 1
    },
    hoverinfo: 'label+percent+name',
    textinfo: 'percent+label'
}, {
    values: allValues[2],
    labels: allLabels,
    type: 'pie',
    name: 'TOTAL',
    marker: {
        colors: list_couleur
    },
    domain: {
        row: 0,
        column: 2
    },
    hoverinfo: 'label+percent+name',

}];

var layout = {
    height: 400,
    /* width: 900, */
    grid: {rows: 1, columns: 3}
};

Plotly.newPlot('graph-all', data, layout, config);
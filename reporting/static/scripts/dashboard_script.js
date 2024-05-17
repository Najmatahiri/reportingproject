
/* CURRENT DATE */
const monthInput = document.getElementById('monthInput');
const currentDate = new Date();
const currentMonth = currentDate.getMonth() + 1; // Mois commence à 0
const currentYear = currentDate.getFullYear()
const formattedMonth = `${currentYear}-${currentMonth < 10 ? '0' : ''}${currentMonth}`;
monthInput.value = formattedMonth;

 let total_count_hs_dom = document.getElementById("totalCountBadge")

let parts = monthInput.value.split("-")
let mois = parts[1];
let annee = parts[0];

let total_crit = document.getElementById("total_critical")
let total_imp = document.getElementById("total_important")
let total_mod = document.getElementById("total_moderate")
let total_lw = document.getElementById("total_low")


function myFunction(val) {
    annee = monthInput.value.split('-')[0]
    mois = monthInput.value.split('-')[1]
    setTimeout(refreshData, 100)

}



/**
 * Compte le nombre d'éléments égaux à zéro et différents de zéro dans un tableau.
 * @param {number[]} tab - Le tableau d'entiers à analyser.
 * @returns {number[]} Un tableau contenant deux valeurs : le nombre d'éléments égaux à zéro et le nombre d'éléments différents de zéro.
 */
function patched_tab(tab) {
    let patched = 0; // Compteur pour les éléments égaux à zéro
    let not_patched = 0; // Compteur pour les éléments différents de zéro
    let tab_two_values = []; // Tableau pour stocker les deux compteurs

    // Parcours de chaque valeur dans le tableau
    tab.forEach((val) => {
        if (val === 0) {
            ++patched; // Incrémente le compteur si la valeur est égale à zéro
        } else {
            ++not_patched; // Incrémente le compteur si la valeur est différente de zéro
        }
    });

    // Ajoute les compteurs au tableau
    tab_two_values.push(patched, not_patched);

    // Retourne le tableau contenant les compteurs
    return tab_two_values;
}

function somme_tab(tab) {
    let somme = 0
    tab.forEach(value => {
        somme += value
    });
    return somme
}

function fetchData() {
    fetch(`http://127.0.0.1:8000/api/machines/?year=${annee}&month=${mois}`) // Effectue une requête à l'API
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            updatePlot(data); // Appelle la fonction pour mettre à jour les graphiques avec les données récupérées
            // console.log(data); affiche les données récupérées dans la console
        })
        .catch(error => console.error('Erreur lors de la récupération des données :', error)); // Affiche une erreur en cas de problème de récupération des données
}

function updatePlot(data) {

    // Extraction des données critiques pour chaque groupe
    let total_critical = data.map(item => item.critical);
    let total_important = data.map(item => item.important);
    let total_moderate = data.map(item => item.moderate);
    let total_low = data.map(item => item.low);

    let critical_tab_prod = data.filter(machine => machine.group === "PROD").map(item => item.critical);
    let critical_tab_hors_prod = data.filter(machine => machine.group === "Hors-Prod").map(item => item.critical);
    let critical_tab_total = data.filter(machine => machine.group === "PROD" || machine.group === "Hors-Prod").map(item => item.critical);


    let nb_prod_patched = data.filter(machine => machine.group === "PROD" && machine.critical === 0).length



    console.log("le nombre critical " + nb_prod_patched)

    total_crit.innerText = somme_tab(total_critical)
    total_imp.innerText = somme_tab(total_important)
    total_mod.innerText = somme_tab(total_moderate)
    total_lw.innerText = somme_tab(total_low)

   

    // Appel de la fonction patched_tab pour obtenir les données sur les machines patchées et non patchées
    let total_tab = patched_tab(critical_tab_total);
    let tab_prod = patched_tab(critical_tab_prod);
    let tab_hors_prod = patched_tab(critical_tab_hors_prod);


    let config = {displayModeBar: false, responsive: true}

    /* GLOBAL GRAHPIC */
    
    let list_couleur = ['#37b24d', '#f03e3e']
    let allLabels = ['Patched', 'Not Pathed'];
    let alldata = [{
        values: tab_prod,
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
        textinfo: 'percent',
        title: {
            text: 'PROD', // Titre pour le graphe PROD
            font: {
                size: 18 // Taille de la police du titre
            }
        }
    }, {
        values: tab_hors_prod,
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
        textinfo: 'percent',
        title: {
            text: 'HORS-PROD', // Titre pour le graphe Hors prod
            font: {
                size: 18 // Taille de la police du titre
            }
        }
    }, {
        values: total_tab,
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
        textinfo: 'percent',
        title: {
            text: 'TOTAL', // Titre pour le graphe PROD
            font: {
                size: 18 // Taille de la police du titre
            }
        }

    }];

    let layout = {
        /* height: 400, */
        title: 'Statistique des patchs',
        /* width: 900, */
        grid: {rows: 1, columns: 3}
    };

    Plotly.newPlot('graph-all', alldata, layout, config);





      // par verions
    // Tableau de versions de RedHat


    let nb_pathed_v7 = data.filter(machine => machine.os.startsWith("RedHat 7.") && machine.critical === 0).length;
    let nb_pathed_v8 = data.filter(machine => machine.os.startsWith("RedHat 8.") && machine.critical === 0).length;
    let nb_pathed_v9 = data.filter(machine => machine.os.startsWith("RedHat 9.") && machine.critical === 0).length;
    let nb_not_pathed_v7 = data.filter(machine => machine.os.startsWith("RedHat 7.") && machine.critical > 0).length;
    let nb_not_pathed_v8 = data.filter(machine => machine.os.startsWith("RedHat 8.") && machine.critical > 0).length;
    let nb_not_pathed_v9 = data.filter(machine => machine.os.startsWith("RedHat 9.") && machine.critical > 0).length;

    let tab_os_patched = [nb_pathed_v7, nb_pathed_v8, nb_pathed_v9]
    let tab_os_not_patched = [nb_not_pathed_v7, nb_not_pathed_v8, nb_not_pathed_v9]

    let total_hs = data.filter(machine => machine.os.startsWith("RedHat 6.")).length;
    console.log("total hs"+total_hs)
    total_count_hs_dom.innerText = total_hs.toString()

    console.log(tab_os_patched)
    console.log(tab_os_not_patched)

    let trace_patched = {
        x: ['RedHat 7', 'RedHat 8', 'RedHat 9'],
        y: tab_os_patched,
        name: 'Patched',
        type: 'bar',
        marker: {
            color: 'green',
        }


    };

    let trace_not_patched = {
        x: ['RedHat 7', 'RedHat 8', 'RedHat 9'],
        y: tab_os_not_patched,
        name: 'Not Pathed',
        type: 'bar',
        marker: {
            color: 'red',
        }

    };


    let date_os = [trace_patched, trace_not_patched];

    let layout_os = {
        scattermode: 'group',
        // barmode: 'stack',
        title: 'Patchs selon les versions de RedHat',
        xaxis: {title: 'Version de RedHat'},
        yaxis: {title: 'Number Patched'},
        barcornerradius: 15

    };

    Plotly.newPlot('graph-patch-os', date_os, layout_os, config);
}


function refreshData() {
    fetchData(); // Appelle la fonction pour récupérer les données
    setTimeout(refreshData, 5000); // Programme l'appel de la fonction de rafraîchissement toutes les 5 secondes
}

// Appelle la fonction de rafraîchissement des données pour la première fois.
refreshData();



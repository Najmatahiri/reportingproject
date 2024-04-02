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

/**
 * Effectue une requête à une API pour récupérer des données, puis appelle la fonction updatePlot pour mettre à jour les graphiques.
 */
function fetchData() {
    fetch("http://127.0.0.1:8000/api/machines/") // Effectue une requête à l'API
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            updatePlot(data); // Appelle la fonction pour mettre à jour les graphiques avec les données récupérées
            console.log(data); // Affiche les données récupérées dans la console
        })
        .catch(error => console.error('Erreur lors de la récupération des données :', error)); // Affiche une erreur en cas de problème de récupération des données
}

/**
 * Met à jour les graphiques avec les données fournies.
 * @param {object[]} data - Les données à utiliser pour mettre à jour les graphiques.
 */
function updatePlot(data) {
    // Définition des étiquettes et des groupes pour les graphiques
    let label_graph = ["PROD", "HORS-PROD", "TOTAL"];
    let group = ["Patched", "Not Patched"];
    let couleur = ['green', 'red']; // Couleurs pour les graphiques

    // Extraction des données critiques pour chaque groupe
    let total_critical = data.map(item => item.critical);
    let critical_tab_prod = data.filter(machine => machine.group === "PROD").map(item => item.critical);
    let critical_tab_hors_prod = data.filter(machine => machine.group === "Hors-Prod").map(item => item.critical);

    // Appel de la fonction patched_tab pour obtenir les données sur les machines patchées et non patchées
    let total_tab = patched_tab(total_critical);
    let tab_prod = patched_tab(critical_tab_prod);
    let tab_hors_prod = patched_tab(critical_tab_hors_prod);

    // Création des mises en page pour les graphiques
    let width = 350;
    let height = 300;
    let layout1 = { height: height, width: width, title: label_graph[0] };
    let layout2 = { height: height, width: width, title: label_graph[1] };
    let layout3 = { height: height, width: width, title: label_graph[2] };

    // Création des graphiques avec Plotly
    Plotly.newPlot('prod-plot', [{
        values: tab_prod,
        labels: group,
        type: 'pie',
        hole: .6,
        marker: {
            colors: couleur
        },
    }], layout1);

    Plotly.newPlot('hors_prod-plot', [{
        values: tab_hors_prod,
        labels: group,
        type: 'pie',
        hole: .6,
        marker: {
            colors: couleur
        },
    }], layout2);

    Plotly.newPlot('total-plot', [{
        values: total_tab,
        labels: group,
        type: 'pie',
        marker: {
            colors: couleur
        },
    }], layout3);
}

/**
 * Actualise les données périodiquement en appelant fetchData toutes les 5 secondes.
 */
function refreshData() {
    fetchData(); // Appelle la fonction pour récupérer les données
    setTimeout(refreshData, 5000); // Programme l'appel de la fonction de rafraîchissement toutes les 5 secondes
}

// Appelle la fonction de rafraîchissement des données pour la première fois.
refreshData();

// fetch()
// .then(res => res.json())
// .then(tab => {
//     console.log(tab)
// })

// Fonction pour récupérer les données de l'API
function fetchData() {
// Faire une requête à votre API
fetch("http://127.0.0.1:8000/api/machines/")
.then(response => response.json())
.then(data => {
// Mettre à jour le graphique avec les nouvelles données
updatePlot(data);
console.log(data)
})
.catch(error => console.error('Erreur lors de la récupération des données :', error));
}

// Fonction pour mettre à jour le graphique avec de nouvelles données
function updatePlot(data) {
// Extraire les données pour Plotly
// Exemple de données :
var group = data.map(item => item["group"]);
var critical = data.map(item => item.critical);
console.log(critical)

// Mise à jour du graphique
Plotly.newPlot('plot', [{
values: critical,
labels: group,
type: 'pie',

}]);
}

// Fonction pour rafraîchir périodiquement les données
function refreshData() {
fetchData(); // Récupérer les données à intervalles réguliers
// setTimeout(refreshData, 5000); // Répéter toutes les 5 secondes (5000 millisecondes)
}
// Démarrer le rafraîchissement des données
refreshData();
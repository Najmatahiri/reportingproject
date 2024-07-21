// LES VARIABLES ET CONSTANTES

/** @type {Array} */
let unsupported_versions = [];
/** @type {Array} */
let data_tab_patch_os = [];
/** @type {Set<any>} */
let redhat_major_version = new Set();
/** @type {Array} */
let vm_supported_list = [];
/** @const {Object} */

const host = {
  dev: "127.0.0.1",
  test: "192.168.220.134",
  prod: "10.173.185.247",
};
const port = {
  dev: 8000,
  prod: 8443,
  test: 8443
};
/** @const {Array} */
const list_couleur = ["#37b24d", "#f03e3e"];
/** @const {Array} */
const allLabels = ["Patched", "Not Patched"];
/** @const {Object} */
const config = {
  displayModeBar: true,
  responsive: true,
  toImageButtonOptions: {
    format: "png", // one of png, svg, jpeg, webp
    filename: "custom_image",
    height: 500,
    width: 700,
    scale: 1,
  },
  displaylogo: false,
};

/** CURRENT DATE */
const monthInput = document.getElementById("monthInput");
console.log(monthInput);
monthInput.classList.add("dark-month");
const currentDate = new Date();
const currentMonth = currentDate.getMonth() + 1;
const currentYear = currentDate.getFullYear();
const formattedMonth = `${currentYear}-${
  currentMonth < 10 ? "0" : ""
}${currentMonth}`;
monthInput.value = formattedMonth;

let parts = monthInput.value.split("-");
let mois = parts[1];
let annee = parts[0];

let total_crit = document.getElementById("total_critical");
let total_imp = document.getElementById("total_important");
let total_mod = document.getElementById("total_moderate");
let total_lw = document.getElementById("total_low");

/**
 * Calcule la somme des valeurs d'un tableau.
 * @param {Array<number>} tab - Tableau des valeurs.
 * @returns {number} - La somme des valeurs.
 */
function somme_tab(tab) {
  let somme = 0;
  tab.forEach((value) => {
    somme += value;
  });
  return somme;
}

/**
 * Gère le changement de date.
 * @param {string} val - La nouvelle valeur de date.
 */
function handleDateChange(val) {
  annee = monthInput.value.split("-")[0];
  mois = monthInput.value.split("-")[1];

  setTimeout(refreshData, 100);
}

/**
 * Crée un tableau de données patchées et non patchées pour un groupe donné.
 * @param {Array<Object>} data - Tableau des machines.
 * @param {string} group - Groupe de machines (PROD, Hors-Prod, etc.).
 * @returns {Array<number>} - Tableau avec le nombre de machines patchées et non patchées.
 */
function create_data_tab(data, group) {
  let nb_patched = data.filter(
    (vm) => vm.group === group && vm.critical === 0
  ).length;
  let nb_not_patched = data.filter(
    (vm) => vm.group === group && vm.critical > 0
  ).length;
  return [nb_patched, nb_not_patched];
}

/**
 * Additionne les valeurs de deux tableaux de même taille.
 * @param {Array<number>} tab1 - Premier tableau de valeurs.
 * @param {Array<number>} tab2 - Deuxième tableau de valeurs.
 * @returns {Array<number>} - Tableau résultant de l'addition.
 * @throws {Error} - Si les tableaux n'ont pas la même taille.
 */
function additionnerTableaux(tab1, tab2) {
  if (tab1.length !== tab2.length) {
    throw new Error("Les tableaux doivent avoir la même taille");
  }

  const resultat = [];

  for (let i = 0; i < tab1.length; i++) {
    resultat.push(tab1[i] + tab2[i]);
  }

  return resultat;
}

/**
 * Crée un graphique en secteurs.
 * @param {string} id - ID de l'élément HTML où le graphique sera rendu.
 * @param {Array<number>} values - Valeurs des segments.
 * @param {string} title - Titre du graphique.
 * @param {boolean} [hole=true] - Si true, crée un graphique en anneau.
 */
function create_pie_chart(id, values, title, hole = true) {
  let data = [
    {
      values: values,
      labels: allLabels,
      type: "pie",
      hole: hole && 0.6,
      marker: {
        colors: list_couleur,
      },
      textinfo: "percent+value",
    },
  ];

  let layout = {
    title: title.concat(" : ").concat(values.reduce((acc, x) => acc + x, 0)),
  };

  Plotly.newPlot(id, data, layout, config);
}

/**
 * Crée un graphique en barres.
 * @param {string} id - ID de l'élément HTML où le graphique sera rendu.
 * @param {Array<number>} data1 - Données pour les machines patchées.
 * @param {Array<number>} data2 - Données pour les machines non patchées.
 */
function create_bar_chart(id, data1, data2) {
  let trace_patched = {
    x: redhat_major_version,
    y: data1,
    name: "Patched",
    type: "bar",
    marker: {
      color: list_couleur[0],
    },
    text: data1.map(String),
    textposition: "auto",
    textfont: {
      family: "Arial, sans-serif",
      size: 18,
      color: "black",
    },
  };

  let trace_not_patched = {
    x: redhat_major_version,
    y: data2,
    name: "Not Patched",
    type: "bar",
    marker: {
      color: list_couleur[1],
    },
    text: data2.map(String),
    textposition: "auto",
    textfont: {
      family: "Arial, sans-serif",
      size: 18,
      color: "black",
    },
  };

  let date_os = [trace_patched, trace_not_patched];

  let layout_os = {
    scattermode: "group",
    title: "Patchs selon les versions de RedHat",
    xaxis: { title: "Version de RedHat" },
    yaxis: { title: "Nombre Patché" },
    barcornerradius: 15,
    autosize: true,
  };

  Plotly.newPlot(id, date_os, layout_os, config);
}

/**
 * Fonction de callback pour sommer les criticités.
 * @param {number} a - Première valeur.
 * @param {number} b - Deuxième valeur.
 * @returns {number} - La somme des deux valeurs.
 */
function call_back_sum_criticality(a, b) {
  return a + b;
}

/**
 * Récupère la configuration des données depuis une API.
 */
function fetchDataConfig() {
  fetch(`http://${host.dev}:${port.dev}/api/config/`)
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      unsupported_versions = data.map((version) => {
        return version.unsupported_versions;
      });
    })
    .catch((error) =>
      console.error("Erreur lors de la récupération des données :", error)
    );
}

/**
 * Récupère les versions majeures de RedHat des données.
 * @param {Array<Object>} data - Données des machines.
 * @returns {Array<string>} - Versions majeures de RedHat.
 */
function getRedHatMajorVersions(data) {
  const redhatVersions = new Set();

  for (const machine of data) {
    const osVersion = machine.os;

    if (osVersion.includes("RedHat")) {
      const versionMajor = osVersion.split(" ")[1].split(".")[0];
      redhatVersions.add(`RedHat ${versionMajor}`);
    }
  }

  for (const version of unsupported_versions) {
    redhatVersions.delete(version);
  }

  return Array.from(redhatVersions).sort();
}

/**
 * Récupère les statistiques de patchs des systèmes d'exploitation.
 * @param {Array<Object>} data - Données des machines.
 * @returns {Object} - Statistiques des patchs des systèmes d'exploitation.
 */
function getStatPatchOS(data) {
  const statPatchsOS = {};
  const dataTabStatOS = [];

  for (const version of redhat_major_version) {
    const nbPatched = data.filter(
      (machine) => machine.os.startsWith(version) && machine.critical === 0
    ).length;
    const nbNotPatched = data.filter(
      (machine) => machine.os.startsWith(version) && machine.critical > 0
    ).length;
    dataTabStatOS.push([nbPatched, nbNotPatched]);
  }

  const reorganizedData = dataTabStatOS.reduce(
    (acc, val) => {
      acc[0].push(val[0]);
      acc[1].push(val[1]);
      return acc;
    },
    [[], []]
  );

  statPatchsOS["tab_os__patched"] = reorganizedData[0];
  statPatchsOS["tab_os_not_patched"] = reorganizedData[1];

  return statPatchsOS;
}

/**
 * Filtre et trie la liste des machines selon les versions supportées et un champ de tri.
 * @param {Array<Object>} data - Données des machines.
 * @param {string} orderField - Champ de tri.
 * @returns {Array<Object>} - Liste des machines supportées et triées.
 */
function getListInSupport(data, orderField) {
  const versionSupported = redhat_major_version;
  let machinesSupported = [];

  for (let version of versionSupported) {
    machinesSupported = machinesSupported.concat(
      data.filter((machine) => machine.os.startsWith(`${version}.`))
    );
  }

  machinesSupported.sort((a, b) => {
    if (orderField.startsWith("-")) {
      let field = orderField.slice(1);
      return b[field] - a[field];
    } else {
      return a[orderField] - b[orderField];
    }
  });

  return machinesSupported;
}

/**
 * Récupère les données des machines depuis une API et met à jour les graphiques.
 */
function fetchData() {
  fetch(
    `http://${host.dev}:${port.dev}/api/machines/?year=${annee}&month=${mois}`
  )
    .then((response) => response.json())
    .then((data) => {
      redhat_major_version = getRedHatMajorVersions(data);
      data_tab_patch_os = getStatPatchOS(data);
      vm_supported_list = getListInSupport(data, "nom_machine");
      console.log(vm_supported_list);
      updatePlot(data);
    })
    .catch((error) =>
      console.error("Erreur lors de la récupération des données :", error)
    );
}

/**
 * Met à jour les graphiques avec les nouvelles données.
 * @param {Array<Object>} data - Données des machines.
 */
function updatePlot(data) {
  let total_critical = vm_supported_list
    .map((item) => item.critical)
    .reduce(call_back_sum_criticality, 0);
  let total_important = vm_supported_list
    .map((item) => item.important)
    .reduce(call_back_sum_criticality, 0);
  let total_moderate = vm_supported_list
    .map((item) => item.moderate)
    .reduce(call_back_sum_criticality, 0);
  let total_low = vm_supported_list
    .map((item) => item.low)
    .reduce(call_back_sum_criticality, 0);
  total_crit.innerText = total_critical;
  total_imp.innerText = total_important;
  total_mod.innerText = total_moderate;
  total_lw.innerText = total_low;

  let tab_prod = create_data_tab(vm_supported_list, "PROD");
  let tab_hors_prod = create_data_tab(vm_supported_list, "Hors-Prod");
  let total_tab = additionnerTableaux(tab_prod, tab_hors_prod);

  create_pie_chart("graph_prod", tab_prod, "PROD");
  create_pie_chart("graph_hors_prod", tab_hors_prod, "HORS- PROD");
  create_pie_chart("graph_total", total_tab, "TOTAL", false);
  create_bar_chart(
    "graph-patch-os",
    data_tab_patch_os.tab_os__patched,
    data_tab_patch_os.tab_os_not_patched
  );
}

/**
 * Rafraîchit les données périodiquement.
 */
function refreshData() {
  fetchDataConfig();
  fetchData();
  setTimeout(refreshData, 4000);
}

// Appelle la fonction de rafraîchissement des données pour la première fois.
refreshData();

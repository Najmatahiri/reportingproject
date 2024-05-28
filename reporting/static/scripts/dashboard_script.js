// LES VARIABLES ET CONSTANTE

let  unsupported_versions = []
let data_tab_patch_os = []
let redhat_major_version =  new Set()

let vm_supported_list = []
const host = {
    dev: "127.0.0.1",
    test: "192.168.220.134",
    prod: "10.173.185.242"
}
const list_couleur = ['#37b24d', '#f03e3e']


const allLabels = ['Patched', 'Not Pathed'];
const config = {displayModeBar: false, responsive: true}


/* CURRENT DATE */
const monthInput = document.getElementById('monthInput');
const currentDate = new Date();
const currentMonth = currentDate.getMonth() + 1; //
const currentYear = currentDate.getFullYear()
const formattedMonth = `${currentYear}-${currentMonth < 10 ? '0' : ''}${currentMonth}`;
monthInput.value = formattedMonth;

// let total_count_hs_dom = document.getElementById("totalCountBadge")

let parts = monthInput.value.split("-")
let mois = parts[1];
let annee = parts[0];

let total_crit = document.getElementById("total_critical")
let total_imp = document.getElementById("total_important")
let total_mod = document.getElementById("total_moderate")
let total_lw = document.getElementById("total_low")





// LES FONCTIONS

function somme_tab(tab) {
    let somme = 0
    tab.forEach(value => {
        somme += value
    });
    return somme
}
function handleDateChange(val) {
    annee = monthInput.value.split('-')[0]
    mois = monthInput.value.split('-')[1]
    setTimeout(refreshData, 100)

}

function create_data_tab(data, group) {
    let nb_patched = data.filter(vm => vm.group === group && vm.critical === 0).length
    let nb_not_patched = data.filter(vm => vm.group === group && vm.critical > 0).length
    return [nb_patched, nb_not_patched]

}

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

function create_pie_chart(id, values, title, hole = true) {
    let data = [{
        values: values,
        labels: allLabels,
        type: 'pie',

        hole: hole && .6,
        marker: {
            colors: list_couleur
        },

    }];

    let layout = {
        title: title,
        // height: 400,
        // width: 500
    };

    Plotly.newPlot(id, data, layout, config);


}
function  call_back_sum_criticality(a,b) {
    return a+b
}





function fetchDataConfig() {
    fetch('http://127.0.0.1:8000/api/config/') // Effectue une requête à l'API
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
            console.log(data);
            unsupported_versions = data.map(version => {
                return version.unsupported_versions

            })

        })
        .catch(error => console.error('Erreur lors de la récupération des données :', error)); // Affiche une erreur en cas de problème de récupération des données
}

function getRedHatMajorVersions(data){
     const redhatVersions = new Set();


    for (const machine of data) {
        const osVersion = machine.os;

        if (osVersion.includes("RedHat")) {
            const versionMajor = osVersion.split(' ')[1].split('.')[0];
            redhatVersions.add(`RedHat ${versionMajor}`);
        }
    }

     for (const version of unsupported_versions) {
        redhatVersions.delete(version);
    }

    return Array.from(redhatVersions).sort();



}

function getStatPatchOS(data){
    const statPatchsOS = {};
    const dataTabStatOS = [];
    for (const version of redhat_major_version) {
        const nbPatched = data.filter(machine => machine.os.startsWith(version) && machine.critical === 0).length
        const nbNotPatched = data.filter(machine => machine.os.startsWith(version) && machine.critical > 0).length
        dataTabStatOS.push([nbPatched, nbNotPatched]);
    }

    const reorganizedData = dataTabStatOS.reduce((acc, val) => {
        acc[0].push(val[0]);
        acc[1].push(val[1]);
        return acc;
    }, [[], []]);

    statPatchsOS["tab_os__patched"] = reorganizedData[0];
     statPatchsOS["tab_os_not_patched"] =  reorganizedData[1];

    return statPatchsOS;
}
function getListInSupport(data, orderField) {
    const versionSupported = redhat_major_version;
    let machinesSupported = [];

    for (let version of versionSupported) {
        machinesSupported = machinesSupported.concat(
            data.filter(machine => machine.os.startsWith(`${version}.`))
        );
    }

    machinesSupported.sort((a, b) => {
        if (orderField.startsWith('-')) {
            let field = orderField.slice(1);
            return b[field] - a[field];
        } else {
            return a[orderField] - b[orderField];
        }
    });

    return machinesSupported;
}


function fetchData() {
    fetch(`http://${host.dev}:8000/api/machines/?year=${annee}&month=${mois}`) // Effectue une requête à l'API
        .then(response => response.json()) // Convertit la réponse en JSON
        .then(data => {
             redhat_major_version = getRedHatMajorVersions(data)
            data_tab_patch_os = getStatPatchOS(data)
            vm_supported_list = getListInSupport(data, "nom_machine")
            console.log(vm_supported_list)
            updatePlot(data);

            // console.log(data_tab_patch_os)
            // console.log(data);
        })
        .catch(error => console.error('Erreur lors de la récupération des données :', error));
}



function updatePlot(data) {
    // Extraction des données critiques pour chaque groupe
    let total_critical =data.map(item => item.critical).reduce(call_back_sum_criticality, 0)
    let total_important = data.map(item => item.important).reduce(call_back_sum_criticality, 0);
    let total_moderate = data.map(item => item.moderate).reduce(call_back_sum_criticality, 0);
    let total_low = data.map(item => item.low).reduce(call_back_sum_criticality, 0);
    total_crit.innerText = total_critical
    total_imp.innerText = total_important
    total_mod.innerText = total_moderate
    total_lw.innerText = total_low


    let tab_prod = create_data_tab(vm_supported_list, "PROD");
    let tab_hors_prod = create_data_tab(vm_supported_list, "Hors-Prod");
    let total_tab = additionnerTableaux(tab_prod, tab_hors_prod);

    /* GLOBAL GRAHPIC */
    create_pie_chart("graph_prod", tab_prod, "PROD")
    create_pie_chart("graph_hors_prod", tab_hors_prod, "HORS- PROD")
    create_pie_chart("graph_total", total_tab, "TOTAL", false)


    // par verions
    // Tableau de versions de RedHat


    // let total_hs = data.filter(machine => machine.os.startsWith("RedHat 6.")).length;
    // total_count_hs_dom.innerText = total_hs.toString()


    let trace_patched = {
        x: redhat_major_version,
        y: data_tab_patch_os.tab_os__patched,
        name: 'Patched',
        type: 'bar',
        marker: {
            color: 'green',
        }


    };

    let trace_not_patched = {
        x: redhat_major_version,
        y: data_tab_patch_os.tab_os_not_patched,
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
    fetchData();
    fetchDataConfig()
    // Appelle la fonction pour récupérer les données
    setTimeout(refreshData, 5000); // Programme l'appel de la fonction de rafraîchissement toutes les 5 secondes
}


// Appelle la fonction de rafraîchissement des données pour la première fois.
refreshData();


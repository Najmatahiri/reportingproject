// let table = $('#myTable').DataTable()


$(document).ready(function () {

    /** CURRENT DATE */

    const currentDate = new Date();
    const currentMonth = currentDate.getMonth() + 1;
    const currentYear = currentDate.getFullYear();
    const formattedMonth = `${currentYear}-${currentMonth < 10 ? '0' : ''}${currentMonth}`;


    let parts = formattedMonth.split("-");
    let mois = parts[1];
    let annee = parts[0];

    console.log(mois)
    console.log(annee)

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


    // let apiUrl = `http://${host.dev}:${port.dev}/api/machines/?format=json&month=${mois}&year=${annee}`
    let apiUrl = `http://${host.test}:${port.test}/api/machines/?format=json&month=${mois}&year=${annee}`
    console.log(apiUrl)


    $('#myTable').DataTable({
        "ajax": {
            "url": apiUrl,
            "dataSrc": ""
        },
        "columns": [
            {"data": "nom_machine"},
            {"data": "ip"},
            {"data": "group"},
            {"data": "os"},
            {"data": "critical"},
            {"data": "important"},
            {"data": "moderate"},
            {"data": "low"},


        ]
    });
});
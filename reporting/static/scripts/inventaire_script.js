

$('#myTable').DataTable( {
    ajax: {url : "http://127.0.0.1:8000/api/machines/", dataSrc: ""},
    columns: [
        { data: 'nom_machine' },
        { data: 'ip' },
        { data: 'group' },
        { data: 'os' },
        { data: 'critical' },
        { data: 'important' },
        { data: 'moderate' },
        { data: 'low' },


    ]
} );
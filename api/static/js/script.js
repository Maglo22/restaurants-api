$(document).ready(() => {
    // initialize table
    $('#restaurantes').DataTable({
        ajax: {
            url: '/api/restaurants',
            dataSrc: ''
        },
        columns: [
            { data: 'name' },
            { data: 'site' },
            { data: 'rating' },
            {
                data: null,
                defaultContent: '<button class="btn blue-gradient btn-sm">Edit</button>',
                targets: -1
            }
        ]
    });
});
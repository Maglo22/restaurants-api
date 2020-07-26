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
                defaultContent: '<button class="btn blue-gradient btn-sm">Details</button>'
                                + '<button class="btn aqua-gradient btn-sm">Edit</button>'
                                + '<button class="btn peach-gradient btn-sm" data-toggle="modal" data-target="#modalDelete">Delete</button>',
                targets: -1
            }
        ]
    });
});

$('#btnCreate').click((e) => {
    e.preventDefault();

    let url = '/api/restaurants/create';
    let data = {
        name: $('#name').val(),
        phone: $('#phone').val(),
        email: $('#email').val(),
        street: $('#street').val(),
        city: $('#city').val(),
        state: $('#state').val(),
        lat: $('#lat').val(),
        lng: $('#lng').val(),
        site: $('#site').val()    
    };

    apiCall(url, data);
});

function format(d) {
    return 'ID: '+ d.id;
}

function apiCall(url, data) {
    $.ajax({
        type : 'POST',
        url : url,
        data: JSON.stringify(data, null, '\t'),
        contentType: 'application/json;charset=UTF-8',
        success: (res) => {
            $('#toastMsg').text(res.message);
            $('#notify').toast('show');
        },
        error: (err) => {
            console.error(err);
        }
    });
}
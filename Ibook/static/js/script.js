
function Book_checkbox() {
    window.search_input={'type':'','notes':''}

    $('.select-book').change(function() {

        // Gather selected checkboxes
        const selected = [];
        $('.select-book:checked').each(function() {
            selected.push($(this).attr('id'));
        });
        // Update the selected options list
        // updateSelectedList(selected);
        $('.selectedList').empty();
        selected.forEach(function(item) {
            $('.selectedList').append( "<li>" + item + "</li>");
        });
    });
}
$(document).ready(Book_checkbox)

function select_all() {
    console.log($(this).prop('checked'));
    let select_book = $('.select-book:visible');
    let checked = $(this).prop('checked');
    if (checked) {select_book.prop('checked',true);} else {select_book.prop('checked',false);}
    // Book_checkbox();
    $('.select-book').trigger('change');
}

$(document).on('click', '#select-all', select_all)

function searchbar(){
    // console.log('searchbar');
    let value_name = ''
    if ($('#searchInput').val().indexOf(': ') > -1) {
        value_name = $('#searchInput').val().split(': ')[1].toLowerCase();
    }else{
        value_name = $('#searchInput').val().toLowerCase();
    }
    console.log(value_name)
    let booktype = search_input['type'].toLowerCase()
    console.log(booktype);
    let booknote = search_input['notes'].toLowerCase()
    if (booknote.toLowerCase() === 'have notes') {
        booknote = 0
    }

    $('#sync-book-table tbody tr').filter(function () {
        // filter the book name
        const namerow = $(this).children('.book-name-row');
        const typerow = $(this).children('.book-type-row');
        const noterow = $(this).children('.book-note-row');
        $(this).toggle(
            namerow.text().toLowerCase().indexOf(value_name) > -1 &&
            typerow.text().toLowerCase().indexOf(booktype) > -1
            && noterow.text() > booknote
        );
    })
}

$(document).on('keyup', '#searchInput', searchbar)

function type_filter(){
    // console.log();
    const book_type = $(this).attr('value').toLowerCase();
    const type_filter_check = $('#type-filter-icon').attr('value')
    const notes_filter_check = $('#notes-filter-icon').attr('value')

    $('#sync-book-table tbody tr').filter(function () {
        // filter the book name
        const typerow = $(this).children('.book-type-row');
        $(this).toggle(book_type.indexOf(typerow.text().toLowerCase()) > -1);
    })
}

// $(document).on('click', '.type-filter', type_filter)



function change_filter_color() {
    let filter_value = $(this).attr('value').toUpperCase()
    let change_color = $()
    if ($(this).attr('class').indexOf('type-filter') > -1) {
        search_input['type']=filter_value;
        change_color = $('#type_filter-icon')
    }else{
        search_input['notes']=filter_value;
        change_color = $('#note_filter-icon')
    }
    if (filter_value === ''){
        change_color.css('color','black');
    }else{
        change_color.css('color','dodgerblue');
    }

    if (search_input['type']===''||search_input['notes']===''){
        if(search_input['type']===''&& search_input['notes']===''){
            let search_input_str = search_input['type']+search_input['notes']
            // $('#searchInput').attr('value', search_input_str)
            $('#searchInput').val(search_input_str)
        }else{
            let search_input_str = search_input['type']+search_input['notes']+': '
            // $('#searchInput').attr('value', search_input_str)
            $('#searchInput').val(search_input_str)
        }
    } else{
        let search_input_str = search_input['type']+','+search_input['notes']+': '
        // $('#searchInput').attr('value', search_input_str)
        $('#searchInput').val(search_input_str)
    }


    // if (filter_value === '') {
    //     $(this).css('color', 'black');
    // }else {
    //     $(this).css('color', 'dodgerblue');
    // }

    searchbar()
}

$(document).on('click', '.dropdown-item', change_filter_color)


// $(document).on('c', '.book-type-row', selectall);

// ==================

function note_filtericon(){
    // console.log();
    const note_num = $(this).attr('value').toLowerCase();
    if (note_num === 'have') {
        $('#sync-book-table tbody tr').filter(function () {
            const noterow = $(this).children('.book-note-row');
            $(this).toggle(noterow.text() !== '-');
        })
    }else if (note_num === 'no'){
         $('#sync-book-table tbody tr').filter(function () {
            const noterow = $(this).children('.book-note-row');
            $(this).toggle(noterow.text() === '-');
        })
    }else if (note_num === 'haveno'){
        $('#sync-book-table tbody tr').filter(function () {
            const noterow = $(this).children('.book-note-row');
            $(this).show();
        })
    }

}
// $(document).on('click', '.note-filter', note_filtericon)

function note_change_filter_color() {
    const book_type = $(this).attr('value');
    // console.log(book_type)
    if (book_type === 'haveno') {
        // console.log(book_type)
        $('#type-filter-icon').css('color', 'black');
    }else {
        $('#type-filter-icon').css('color', 'dodgerblue');
    }
}

// $(document).on('click', '.note-filter', note_change_filter_color)



function filter(){
    // get the conditions of two filters
    // const type_filter_check = $('#type-filter-icon').attr('value')
    // console.log(type_filter_check)
    // const notes_filter_check = $('#notes-filter-icon').attr('value')
    // console.log(notes_filter_check)
    $('#sync-book-table tbody tr').filter(function () {
        // get the value of two attributes of each record
        const typerow = $(this).children('.book-type-row');
        const notesrow = $(this).children('.book-note-row');
        $(this).toggle(type_filter_check.indexOf(typerow.text().toLowerCase()) > -1 &&
            notes_filter_check.indexOf(notesrow.text().toLowerCase()) > -1);
    })
}

// $(document).on('click', '.filter-icon', filter)
$(document).ready(function () {
    $("#Input").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#DocsTable tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});

$('#select_all').click(function() {
    var checkboxes = $('input[type=checkbox]');
    checkboxes.prop('checked', true);
})

$(document).ready(function () {
    var fname;
    $("#send").click(function () {
        var checked = $("input[type=checkbox]:checked");
        var resultArray = [];
        for (v of checked) {
            console.log(v)
            var next_input = $(v).closest("tr");
            next_input = next_input.find("input[type=text]")

            resultArray.push(next_input.val())
        }

        $.ajax({
            type: 'POST',
            url: "/check_option",
            data: { 'data': resultArray },
            success: function (response) {
                if (response.length === 0) {
                    $('#dataIsSafe').removeClass('hidden');
                    $('#dataAtRisk').addClass('hidden');
                    $('#exampleModal').modal('show');
                } else {
                    $('#dataAtRisk').removeClass('hidden');
                    $('#dataIsSafe').addClass('hidden');
                    $('#list').html(response);
                    $('#exampleModal').modal('show');
                }
                console.log(response);
            },
        });
    });
});

$(document).ready(function () {
    var fname;
    $("#delete").click(function () {
        var checked = $("input[type=checkbox]:checked");
        var resultArray = [];
        var rows_list = [];
        for (v of checked) {
            console.log(v)
            var next_input = $(v).closest("tr");
            var row_for_del = $(v).closest("tr");
            next_input = next_input.find("input[type=text]");
            resultArray.push(next_input.val());
            rows_list.push(row_for_del);
        console.log(rows_list)
        }
        $.ajax({
            type: 'POST',
            url: "/delete_option",
            data: { 'data': resultArray },
            success: function (response) {
                if (response.length != 0) {
                    $(rows_list).each(function(index, value){
                        $(value).remove();
                    });
                    $('#DocsTable label').each(function(i) {
                        number = (i + 1).toString();
                        $(this).text(number);
                    });
                    $('#dataIsSafe').addClass('hidden');
                    $('#dataAtRisk').addClass('hidden');
                    $('#dataDeleted').removeClass('hidden');
                    $('#delList').html(response);
                    $('#exampleModal').modal('show');
                }
                console.log(response);
            },
        });
    });
});
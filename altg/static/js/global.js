$(document).ready(function() {
    console.log("Jquery is working....");

    $("#lecturer_filter").change(function(el) {
        el.preventDefault();
        var lecturerVal = $(this).val();
        console.log(lecturerVal);
        $.ajax({
            type: "GET",
            url: "/lecturerFilter",
            data: { lecturerVal: lecturerVal },
            success: function(data) {
                $("#subject-table tbody").html(data);
                data.forEach(function(sub) {
                    $("#subject-table tbody").append(
                        "<tr><td>" +
                        sub.fields.subject_code +
                        "</td>" +
                        "<td>" +
                        sub.fields.subject_name +
                        "</td>" +
                        '<td class="text-center">' +
                        sub.fields.related_batch +
                        "</td>" +
                        '<td class="text-center">' +
                        sub.fields.semester +
                        "</td>" +
                        "<td>" +
                        sub.fields.related_lecturer +
                        "</td>" +
                        '<td class="text-center">' +
                        '<div class="row justify-content-center">' +
                        '<div class="col-md-4 custom-left-padding-cols">' +
                        '<button type="button" class="btn btn-sm btn-outline-primary" data-toggle="modal" data-target="#subjectEditModal' +
                        sub.fields.subject_code +
                        '" style="font-size: 12px;">' +
                        '<i class="fad fa-marker fa-lg"></i></button></div>' +
                        '<div class="col-md-4 custom-right-padding-cols">' +
                        '<form action="." method="GET">' +
                        '<input type="hidden" name="subject_code" value="' +
                        sub.fields.subject_code +
                        '">' +
                        '<button type="submit" class="btn btn-sm btn-outline-danger" name="subject_delete_btn" title="Delete subject" style="font-size: 12px;" onclick="return confirm(' +
                        "'Are you sure to delete this subject?'" +
                        ');">' +
                        '<i class="fad fa-trash-alt fa-lg"></i></button></form></div></div</td></tr>'
                    );
                });
            }
        });
    });

    $("#subject_filter").change(function(e) {
        e.preventDefault();
        var filterVal = $(this).val();
        console.log(filterVal);
        $.ajax({
            type: "GET",
            url: "/subjectFilter",
            data: { filterVal: filterVal },
            success: function(data) {
                $("#subject-table tbody").html(data);
                data.forEach(function(sub) {
                    $("#subject-table tbody").append(
                        "<tr><td>" +
                        sub.fields.subject_code +
                        "</td>" +
                        "<td>" +
                        sub.fields.subject_name +
                        "</td>" +
                        '<td class="text-center">' +
                        sub.fields.related_batch +
                        "</td>" +
                        '<td class="text-center">' +
                        sub.fields.semester +
                        "</td>" +
                        "<td>" +
                        sub.fields.related_lecturer +
                        "</td>" +
                        '<td class="text-center">' +
                        '<div class="row justify-content-center">' +
                        '<div class="col-md-4 custom-left-padding-cols">' +
                        '<button type="button" class="btn btn-sm btn-outline-primary" data-toggle="modal" data-target="#subjectEditModal' +
                        sub.fields.subject_code +
                        '" style="font-size: 12px;">' +
                        '<i class="fad fa-marker fa-lg"></i></button></div>' +
                        '<div class="col-md-4 custom-right-padding-cols">' +
                        '<form action="." method="GET">' +
                        '<input type="hidden" name="subject_code" value="' +
                        sub.fields.subject_code +
                        '">' +
                        '<button type="submit" class="btn btn-sm btn-outline-danger" name="subject_delete_btn" title="Delete subject" style="font-size: 12px;" onclick="return confirm(' +
                        "'Are you sure to delete this subject?'" +
                        ');">' +
                        '<i class="fad fa-trash-alt fa-lg"></i></button></form></div></div</td></tr>'
                    );
                });
            }
        });
    });
});

window.addEventListener("load", function() {
    var loader = document.getElementById("se-pre-con");
    loader.style.display = "none";
});

(function($) {
    'use strict';
    /*==================================================================
        [ Daterangepicker ]*/
    try {
        $('.js-datepicker').daterangepicker({
            "singleDatePicker": true,
            "showDropdowns": true,
            "autoUpdateInput": false,
            locale: {
                format: 'DD/MM/YYYY'
            },
        });

        var myCalendar = $('.js-datepicker');
        var isClick = 0;

        $(window).on('click', function() {
            isClick = 0;
        });

        $(myCalendar).on('apply.daterangepicker', function(ev, picker) {
            isClick = 0;
            $(this).val(picker.startDate.format('DD/MM/YYYY'));

        });

        $('.js-btn-calendar').on('click', function(e) {
            e.stopPropagation();

            if (isClick === 1) isClick = 0;
            else if (isClick === 0) isClick = 1;

            if (isClick === 1) {
                myCalendar.focus();
            }
        });

        $(myCalendar).on('click', function(e) {
            e.stopPropagation();
            isClick = 1;
        });

        $('.daterangepicker').on('click', function(e) {
            e.stopPropagation();
        });


    } catch (er) { console.log(er); }
    /*[ Select 2 Config ]
        ===========================================================*/

    try {
        var selectSimple = $('.js-select-simple');

        selectSimple.each(function() {
            var that = $(this);
            var selectBox = that.find('select');
            var selectDropdown = that.find('.select-dropdown');
            selectBox.select2({
                dropdownParent: selectDropdown
            });
        });

    } catch (err) {
        console.log(err);
    }


})(jQuery);
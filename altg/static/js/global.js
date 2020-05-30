window.addEventListener("load", function() {
    var loader = document.getElementById("se-pre-con");
    loader.style.display = "none";

    // Copyright div positioning
    var mp_h = $("#main-panel").innerHeight();
    var mp_t_h = $(".main-panel-title").innerHeight();
    var mp_c_h = $(".main-panel-content").innerHeight();
    var scroll_active_height = mp_h - mp_t_h;
    if (scroll_active_height <= mp_c_h) {
        $(".copyright-div").removeClass("copyright-div-scroll-position");
    } else {
        $(".copyright-div").addClass("copyright-div-scroll-position");
    }
});

$(document).ready(function() {
    console.log("Jquery is working....");

    $(".dropdown-btn").click(function() {
        $(".dropdown-div").slideToggle('fast');
        $(".dropdown-btn span i").toggleClass("fa-chevron-down fa-chevron-up");
    });
    // Morning, afternoon & evenning visualizing function
    var thehours = new Date().getHours();
    var themessage, climateIcon, subGreeting;
    var morning = "Good Morning";
    var afternoon = "Good Afternoon";
    var evening = "Good Evening";
    var morningSubGreeting = "Have a great day.";
    var afternoonSubGreeting = "Be happy and enjoy the day.";
    var eveningSubGreeting = "Wishing you a wonderful evening.";
    var nightSubGreeting = "How was today? Get ready for tomorrow.";
    var morningIcon = "/static/images/sunrise.png";
    var afternoonIcon = "/static/images/sunshine.png";
    var eveningIcon = "/static/images/sunset.png";
    var nightIcon = "/static/images/night.png";

    if (thehours >= 0 && thehours < 5) {
        themessage = morning;
        climateIcon = nightIcon;
        subGreeting = morningSubGreeting;
    } else if (thehours >= 5 && thehours < 12) {
        themessage = morning;
        climateIcon = morningIcon;
        subGreeting = morningSubGreeting;
    } else if (thehours >= 12 && thehours < 14) {
        themessage = afternoon;
        climateIcon = afternoonIcon;
        subGreeting = afternoonSubGreeting;
    } else if (thehours >= 14 && thehours < 19) {
        themessage = evening;
        climateIcon = eveningIcon;
        subGreeting = eveningSubGreeting;
    } else if (thehours >= 19 && thehours < 24) {
        themessage = evening;
        climateIcon = nightIcon;
        subGreeting = nightSubGreeting;
    }
    $(".greeting").append(themessage);
    $(".climate-icon").attr("src", climateIcon);
    $(".sub-greeting").append(subGreeting);

    // Lecturers filter function
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

    // Subject filter function
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

    // Generated schedule save to databse function
    $("#table-save-form").on("submit", function(e2) {
        e2.preventDefault();
        var lecturer_name = $("#lecturer_name").val();
        var semester = $("#semester").val();
        var hall_n_time = $("#hall_n_time").val();
        var data_str = $("#data_str").val();
        $.ajax({
            type: "GET",
            url: "/scheduleSave",
            data: {
                lecturer_name: lecturer_name,
                semester: semester,
                hall_n_time: hall_n_time,
                data_str: data_str
            },
            success: function(success) {
                $("#save-success-msg").css('display', 'block');
                $("#save-success-msg").html(save);
            },
            error: function(error) {
                $("#save-error-msg").css('display', 'block');
                $("#save-error-msg").html(save);
            }
        });
    });

    // Lecture schedule download button function
    $("#schedule_download_btn").click(function() {
        var name = $("#schedule_owner_name").val();

        var doc = new jsPDF("l", "pt", "a4");
        var elem = $("#schedule-table-div table").clone();
        var res = doc.autoTableHtmlToJson(elem.get(0));
        doc.setFontSize(18);
        doc.text("Department of Computing & Information Systems", 225, 40);
        doc.setFontSize(15.5);
        doc.text("Faculty of Applied Sciences, SUSL", 303, 65);
        doc.setFontSize(13.5);
        doc.text("Lecture Schedule", 370, 90);

        doc.setFontSize(11);
        doc.text("Lecturer : " + name, 25, 140);

        doc.autoTable(res.columns, res.data, {
            theme: "grid",
            margin: { top: 160, right: 25, bottom: 30, left: 25 },
            bodyStyles: { rowHeight: 20, halign: "left" },
            styles: {
                tableWidth: "auto",
                cellWidth: "wrap",
                font: "helvetica",
                fontSize: 10.5,
                overflow: "linebreak",
                halign: "center",
                valign: "middle",
            },
            columnStyles: {
                0: { halign: "center" },
                1: { halign: "center" },
                2: { halign: "center" },
                3: { halign: "center" },
            },
        });
        doc.save("Lecture_Schedule.pdf");
    });

    $(".advanced-option-link").click(function() {
        $(".advanced-option-div-content").slideToggle();
        $(".span1 .span1-text").text(
            $(".span1 .span1-text").text() == "Show more options" ?
            "Hide more options" :
            "Show more options"
        );
        $(".span2 i").toggleClass("fa-chevron-down fa-chevron-up");
    });

    $("#change-passwords-show").click(function() {
        $(this).is(":checked") ?
            $(".change-passwords").attr("type", "text") :
            $(".change-passwords").attr("type", "password");
    });

});

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
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

// $(function() {

// });
$(document).ready(function() {
    console.log("Jquery is working....");

    // Default visibilities
    $("#external-color-circle1").addClass("active-color-circle");

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

    // Chart generating function
    var labels = [];
    var data_set = [];
    $.ajax({
        method: "GET",
        url: "/dashChart",
        success: function(data) {
            labels = data.labels;
            data_set = data.data_values;
            var customColors = [];
            for (let i = 0; i < 14; i++) {
                customColors.push(
                    "rgba(" +
                    Math.floor(Math.random() * 256 + 1).toString() +
                    "," +
                    Math.floor(Math.random() * 256 + 1).toString() +
                    "," +
                    Math.floor(Math.random() * 256 + 1).toString() +
                    ",0.7)"
                );
            }
            var ctx = $("#myChart");
            var myChart = new Chart(ctx, {
                type: "doughnut",
                data: {
                    labels: labels,
                    datasets: [{
                        label: "# of Votes",
                        data: data_set,
                        backgroundColor: customColors,
                        borderWidth: 1,
                    }, ],
                },
                options: {
                    legend: {
                        display: false,
                    },
                    tooltips: {
                        bodyFontSize: 14,
                        callbacks: {
                            title: function(tooltipItem, data) {
                                return data["labels"][tooltipItem[0]["index"]];
                            },
                            label: function(tooltipItem, data) {
                                return (
                                    " Subjects : " +
                                    data["datasets"][0]["data"][tooltipItem["index"]]
                                );
                            },
                        },
                        titleFontSize: 15,
                    },
                },
            });
            console.log("Chart generated successfully!");
        },
        error: function(error_data) {
            console.log("Error has been occured!");
            console.log(error_data);
        }
    });

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
});

$(function() {
    $('[data-toggle="tooltip"]').tooltip();
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

// $(function() {

// });
function togglePassword(e) {
    const password = document.querySelector('#id_password');
    const type = password.getAttribute('type') === 'password' ? 'text' : 'password';
    const classValue = e.className == 'fa-solid fa-eye-low-vision' ? 'fa-regular fa-eye' : 'fa-solid fa-eye-low-vision';
    password.setAttribute('type', type);
    e.setAttribute('class', classValue);
}
function allnumeric(e) {
    var numbers = /^[0-9]+$/;
    if (e.value.match(numbers)) {
        document.getElementById('show-error').innerHTML = '';
        return true;
    }
    else {
        // alert('Please input numeric characters only');
        document.getElementById('show-error').innerHTML = 'Please input numeric characters only';
        e.focus();
        return false;
    }
}
function validate(e) {
    if (allnumeric(document.getElementById('mobileno'))) {
        document.my_form.submit();
    }
}
var callAutoFillMethod = function (e) {

    let filter = e.value;

    if (filter && filter.length >= 2) {
        $.ajax({
            type: "GET",
            url: "/auto-fill?input=" + filter,
            dataType: "JSON",
            cache: false,
            async: false,
            error: function (err) {
                alert('Error occured see console to check more');
                console.log(err);
            },
            success: function (data) {
                console.log(data);
                data = JSON.parse(JSON.stringify(data));
                recordAutoFill(data);
            },
        });
    }
}
function recordAutoFill(data) {
    $("#filter-input").autocomplete({
        source: data,
        select: callAfterAutoSelection,
    });
}
function callAfterAutoSelection(event, ui) {
    console.log(event.target);
    console.log(ui.item.value);
    afterautofill(event.target, ui.item.value);
}
function afterautofill(event, value){
    console.log(event,value);
    $.ajax({
        type: "GET",
        url: "/from-account-getuserdetails?input=" + value,
        dataType: "JSON",
        cache: false,
        async: false,
        error: function (err) {
            alert('Error occured see console to check more');
            console.log(err);
        },
        success: function (data) {
            $('#user_details').hide();
            console.log(data);
            data = JSON.parse(JSON.stringify(data));
            $('#name').val("");
            $('#email').val("");
            $('#address').val("");
            $('#pincode').val("");
            $('#mobile_no').val("");
            $('#account_number').val("");
            $('#ifsc').val("");
            $('#state').val("");

            $('#name').val(data.name);
            $('#email').val(data.email);
            $('#address').val(data.address);
            $('#pincode').val(data.pincode);
            $('#mobile_no').val(data.mobile_no);
            $('#account_number').val(data.account_number);
            $('#ifsc').val(data.ifsc);
            $('#state').val(data.state);
            $('#user_details').show("slow");
            $('#to').val(data.user_id);
        },
    });
}

function toggleModel(flag){
    if(flag){
        $('#exampleModalCenteredScrollable').hide();
    }
    else{
        //not sure toggle case
        if($('#exampleModalCenteredScrollable').is(':visible')){
            $('#exampleModalCenteredScrollable').hide();
        }else{
            $('#exampleModalCenteredScrollable').css('display','block');
        }
    }
}
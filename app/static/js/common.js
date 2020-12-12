//Show password (input)
function toggleVisibility(eleId) {
  var x = eleId;
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
//Bootstrap tooltip
$(function () {
    $('[data-toggle="tooltip"]').tooltip()
    })

//Notification settings
toastr.options.closeButton = true;
toastr.options.progressBar = true;
toastr.options.positionClass = "toast-bottom-center"

function getNotifications() {
      var numberOfNotifications = 0
      var notification_divs = document.getElementsByClassName("notify")
      for(numberOfNotifications=0;numberOfNotifications<notification_divs.length;numberOfNotifications++){
          if(notification_divs[numberOfNotifications].id == "error")
              toastr.error(notification_divs[numberOfNotifications].innerHTML)
          else if(notification_divs[numberOfNotifications].id == "info")
              toastr.info(notification_divs[numberOfNotifications].innerHTML)
          else if(notification_divs[numberOfNotifications].id == "success")
              toastr.success(notification_divs[numberOfNotifications].innerHTML)

      }
}


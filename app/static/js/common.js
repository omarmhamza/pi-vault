function toggleVisibility(eleId) {
  var x = eleId;
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}
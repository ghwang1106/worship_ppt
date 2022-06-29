$(document).ready(function () {
  $("#add").click(function () {
    console.log("Hi");
    $("#hymns").append('<div><input type="text" name="input[]"><button class="delete">X</button></div>');
  });
})

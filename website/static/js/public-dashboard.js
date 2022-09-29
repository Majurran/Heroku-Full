$(function () {
  $('#myCarousel').carousel({
      interval:12000,
      pause: "false"
  });
  
  $('#playButton').click(function () {
      $('#myCarousel').carousel('cycle');
  });
  $('#pauseButton').click(function () {
      $('#myCarousel').carousel('pause');
  });
});

// function produce_messages() {

//     var element = document.createElement("div");
//     element.appendChild(document.createTextNode('The man who mistook his wife for a hat'));
//     document.getElementById('lc').appendChild(element);

// }
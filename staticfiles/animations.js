// Drop down menu
const dropDown = () =>{
  const user_holder = document.querySelector('.user-holder');
  const my_dropdown = document.querySelector('.dropdown-content');

  // Ako postoji user_holder element
  if(user_holder) {
    // Ako je user kliknut
    user_holder.addEventListener('click', ()=>{
      // Dodaj ovu klasu ili je ukloni
      my_dropdown.classList.toggle('show');
    });

    document.addEventListener('click', function(event){
      // if user clicks on element do nothing
      if (event.target.closest('.user-holder')) return
      // if user clicks outside an element, remove this class
      my_dropdown.classList.remove('show');

    });
   }
}

dropDown();


// Responsive navigation bar
const slideIn = () =>{
  const burger = document.querySelector('.burger');
  const close = document.querySelector('.close');
  const navbar = document.querySelector('.nav-links');
  const navLinks = document.querySelectorAll(".nav-links li");
  // Ako je burger kliknut
burger.addEventListener('click', ()=>{

  burger.classList.toggle('close');
  // Dodaj ovu klasu ili je ukloni
  navbar.classList.toggle('nav-active');


});

}

slideIn();

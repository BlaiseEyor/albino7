// Ajoute un gestionnaire d'événement pour chaque lien
document.addEventListener("DOMContentLoaded", () => {
  const links = document.querySelectorAll('a[href^="#"]');

  links.forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault(); // Empêche le comportement par défaut du lien

      const targetId = link.getAttribute("href"); // Récupère l'ID de la cible
      const targetSection = document.querySelector(targetId); // Sélectionne la section cible

      // Calcule la position de défilement
      const offset = 130; // Ajuste cette valeur selon la hauteur de ta barre de navigation
      const targetPosition =
        targetSection.getBoundingClientRect().top + window.scrollY - offset;

      // Défilement vers la section cible
      window.scrollTo({
        top: targetPosition,
        behavior: "smooth" // Défilement en douceur
      });
    });
  });
});

// code pour gerer les acction d'ouverture et de fermement du menu

document.addEventListener("DOMContentLoaded", () => {
  const toggleButton = document.querySelector(
    '[data-collapse-toggle="navbar-sticky"]'
  );
  const navMenu = document.getElementById("navbar-sticky");

  if (toggleButton && navMenu) {
    // Fonction pour ouvrir/fermer le menu
    const toggleMenu = () => {
      const isExpanded = toggleButton.getAttribute("aria-expanded") === "true";
      toggleButton.setAttribute("aria-expanded", !isExpanded);
      navMenu.classList.toggle("hidden"); // ✅ Correction ici
    };

    // Gestion du clic sur le bouton de basculement
    toggleButton.addEventListener("click", toggleMenu);

    // Gestion des clics sur les liens du menu
    const menuLinks = navMenu.querySelectorAll(".nav-link");
    menuLinks.forEach((link) => {
      link.addEventListener("click", () => {
        navMenu.classList.add("hidden");
        toggleButton.setAttribute("aria-expanded", "false");
      });
    });

    // Fermer le menu si on clique ailleurs
    document.addEventListener("click", (event) => {
      if (
        !navMenu.contains(event.target) &&
        !toggleButton.contains(event.target)
      ) {
        navMenu.classList.add("hidden");
        toggleButton.setAttribute("aria-expanded", "false");
      }
    });
  }
});

/* Gestion du bouton de défilement*/
const scrollToTopBtn = document.getElementById("scrollToTopBtn");

// Afficher le bouton quand on défile vers le bas de la page
window.onscroll = function () {
  if (
    document.body.scrollTop > 100 ||
    document.documentElement.scrollTop > 100
  ) {
    scrollToTopBtn.classList.add("show");
  } else {
    scrollToTopBtn.classList.remove("show");
  }
};

// Lorsque l'utilisateur clique sur le bouton, faire défiler vers le haut
scrollToTopBtn.addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth" // Défilement en douceur
  });
});

// Sélectionner tous les liens de navigation
const navLinks = document.querySelectorAll(".nav-link");

// Fonction pour supprimer la classe active des autres liens et l'ajouter à l'élément cliqué
navLinks.forEach((link) => {
  link.addEventListener("click", function () {
    // Supprimer la classe active de tous les liens
    navLinks.forEach((nav) => {
      nav.classList.remove(
        "bg-yellow-300",
        "text-white",
        "md:text-yellow-300",
        "active"
      );
    });

    // Ajouter la classe active au lien cliqué
    this.classList.add(
      "bg-yellow-300",
      "text-white",
      "md:text-yellow-300",
      "active"
    );
  });
});


var swiper = new Swiper(".mySwip", {
  slidesPerView: 3, // Nombre d'images visibles par défaut
  spaceBetween: 30, // Espace entre les images
  freeMode: true,
  pagination: {
    el: ".swiper-pagination",
    type: "fraction",
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
    
  },
  breakpoints: {
    320: { // Taille des écrans mobiles
      slidesPerView: 1, // Affiche une image à la fois
      spaceBetween: 10,
    },
    640: { // Tablettes
      slidesPerView: 2,
      spaceBetween: 20,
    },
    1024: { // Écrans plus grands
      slidesPerView: 3,
      spaceBetween: 30,
    },
  },
});

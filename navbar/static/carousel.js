// // Wait until the DOM is fully loaded
// document.addEventListener("DOMContentLoaded", function() {
//     let currentIndex = 0;

//     const carousel = document.getElementById("mainCarousel");
//     const slides = carousel.querySelectorAll(".slide");
//     const carouselInner = carousel.querySelector(".carousel-inner");
//     const prevButton = carousel.querySelector(".prev");
//     const nextButton = carousel.querySelector(".next");

//     function showSlide(index) {
//         const totalSlides = slides.length;

//         if (index >= totalSlides) {
//             currentIndex = 0;
//         } else if (index < 0) {
//             currentIndex = totalSlides - 1;
//         } else {
//             currentIndex = index;
//         }

//         carouselInner.style.transition = "transform 0.5s ease-in-out";
//         carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;
//     }

//     prevButton.addEventListener("click", () => {
//         showSlide(currentIndex - 1);
//     });
//     nextButton.addEventListener("click", () => {
//         showSlide(currentIndex + 1);
//     });

//     // Auto-slide every 2 seconds
//     setInterval(() => {
//         showSlide(currentIndex + 1);
//     }, 5000);

//     // Initialize
//     showSlide(currentIndex);
// });


document.addEventListener("DOMContentLoaded", function() {
    const carousel = document.getElementById("mainCarousel");
    const carouselInner = carousel.querySelector(".carousel-inner");
    const slides = carousel.querySelectorAll(".slide");
    const prevButton = carousel.querySelector(".prev");
    const nextButton = carousel.querySelector(".next");

    let currentIndex = 0;

    // ✅ Clone first slide and append to end
    const firstSlideClone = slides[0].cloneNode(true);
    carouselInner.appendChild(firstSlideClone);

    const totalSlides = slides.length;

    function moveToIndex(index) {
        carouselInner.style.transition = "transform 0.5s ease-in-out";
        carouselInner.style.transform = `translateX(-${index * 100}%)`;
    }

    function showSlide(index) {
        currentIndex = index;
        moveToIndex(currentIndex);
    }

    nextButton.addEventListener("click", () => {
        if (currentIndex >= totalSlides) return;

        currentIndex++;
        moveToIndex(currentIndex);

        if (currentIndex === totalSlides) {
            // ✅ Reset position instantly after animation
            setTimeout(() => {
                carouselInner.style.transition = "none"; 
                carouselInner.style.transform = "translateX(0)";
                currentIndex = 0;
            }, 500);
        }
    });

    prevButton.addEventListener("click", () => {
        if (currentIndex <= 0) {
            // Jump to cloned slide
            currentIndex = totalSlides;
            carouselInner.style.transition = "none"; 
            carouselInner.style.transform = `translateX(-${currentIndex * 100}%)`;

            requestAnimationFrame(() => {
                // Now move backward
                carouselInner.style.transition = "transform 0.5s ease-in-out";
                currentIndex = totalSlides - 1;
                moveToIndex(currentIndex);
            });
        } else {
            currentIndex--;
            moveToIndex(currentIndex);
        }
    });

    // ✅ Auto-slide
    setInterval(() => {
        if (currentIndex >= totalSlides) return;

        currentIndex++;
        moveToIndex(currentIndex);

        if (currentIndex === totalSlides) {
            setTimeout(() => {
                carouselInner.style.transition = "none"; 
                carouselInner.style.transform = "translateX(0)";
                currentIndex = 0;
            }, 500);
        }
    }, 2000);

    // Init
    showSlide(currentIndex);
});
